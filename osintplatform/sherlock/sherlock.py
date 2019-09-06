#! /usr/bin/env python3

"""
Sherlock: Find Usernames Across Social Networks Module

This module contains the main logic to search for usernames at social
networks.
"""

import csv
import json
import os
import platform
import re
import sys
import random
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from time import time

import requests
from colorama import Fore, Style, init

from requests_futures.sessions import FuturesSession
from torrequest import TorRequest
from load_proxies import load_proxies_from_csv, check_proxy_list

from flask import Flask
from flask_restful import Api, Resource, reqparse



module_name = "Sherlock: Find Usernames Across Social Networks"
__version__ = "0.7.8"
amount = 0


global proxy_list

proxy_list = []

app = Flask(__name__)
api = Api(app)

results = {
            "username": "",
            "url": []
        }


class ElapsedFuturesSession(FuturesSession):
    """
    Extends FutureSession to add a response time metric to each request.

    This is taken (almost) directly from here: https://github.com/ross/requests-futures#working-in-the-background
    """

    def request(self, method, url, hooks={}, *args, **kwargs):
        start = time()

        def timing(r, *args, **kwargs):
            elapsed_sec = time() - start
            r.elapsed = round(elapsed_sec * 1000)

        try:
            if isinstance(hooks['response'], (list, tuple)):
                # needs to be first so we don't time other hooks execution
                hooks['response'].insert(0, timing)
            else:
                hooks['response'] = [timing, hooks['response']]
        except KeyError:
            hooks['response'] = timing

        return super(ElapsedFuturesSession, self).request(method, url, hooks=hooks, *args, **kwargs)


def print_info(title, info):
    print(Style.BRIGHT + Fore.GREEN + "[" +
          Fore.YELLOW + "*" +
          Fore.GREEN + f"] {title}" +
          Fore.WHITE + f" {info}" +
          Fore.GREEN + " on:")

def print_error(err, errstr, var, verbose=False):
    print(Style.BRIGHT + Fore.WHITE + "[" +
          Fore.RED + "-" +
          Fore.WHITE + "]" +
          Fore.RED + f" {errstr}" +
          Fore.YELLOW + f" {err if verbose else var}")


def format_response_time(response_time, verbose):
    return " [{} ms]".format(response_time) if verbose else ""


def print_found(social_network, url, response_time, verbose=False):
    print((Style.BRIGHT + Fore.WHITE + "[" +
           Fore.GREEN + "+" +
           Fore.WHITE + "]" +
           format_response_time(response_time, verbose) +
           Fore.GREEN + f" {social_network}:"), url)

def print_not_found(social_network, response_time, verbose=False):
    print((Style.BRIGHT + Fore.WHITE + "[" +
           Fore.RED + "-" +
           Fore.WHITE + "]" +
           format_response_time(response_time, verbose) +
           Fore.GREEN + f" {social_network}:" +
           Fore.YELLOW + " Not Found!"))

def print_invalid(social_network, msg):
    """Print invalid search result."""
    print((Style.BRIGHT + Fore.WHITE + "[" +
           Fore.RED + "-" +
           Fore.WHITE + "]" +
           Fore.GREEN + f" {social_network}:" +
           Fore.YELLOW + f" {msg}"))


def get_response(request_future, error_type, social_network, verbose=False, retry_no=None):

    global proxy_list

    try:
        rsp = request_future.result()
        if rsp.status_code:
            return rsp, error_type, rsp.elapsed
    except requests.exceptions.HTTPError as errh:
        print_error(errh, "HTTP Error:", social_network, verbose)

    # In case our proxy fails, we retry with another proxy.
    except requests.exceptions.ProxyError as errp:
        if retry_no>0 and len(proxy_list)>0:
            #Selecting the new proxy.
            new_proxy = random.choice(proxy_list)
            new_proxy = f'{new_proxy.protocol}://{new_proxy.ip}:{new_proxy.port}'
            print(f'Retrying with {new_proxy}')
            request_future.proxy = {'http':new_proxy,'https':new_proxy}
            get_response(request_future,error_type, social_network, verbose,retry_no=retry_no-1)
        else:
            print_error(errp, "Proxy error:", social_network, verbose)
    except requests.exceptions.ConnectionError as errc:
        print_error(errc, "Error Connecting:", social_network, verbose)
    except requests.exceptions.Timeout as errt:
        print_error(errt, "Timeout Error:", social_network, verbose)
    except requests.exceptions.RequestException as err:
        print_error(err, "Unknown error:", social_network, verbose)
    return None, "", -1


def sherlock(username, site_data, verbose=False, tor=False, unique_tor=False, proxy=None, print_found_only=False):
    """Run Sherlock Analysis.

    Checks for existence of username on various social media sites.

    Keyword Arguments:
    username               -- String indicating username that report
                              should be created against.
    site_data              -- Dictionary containing all of the site data.
    verbose                -- Boolean indicating whether to give verbose output.
    tor                    -- Boolean indicating whether to use a tor circuit for the requests.
    unique_tor             -- Boolean indicating whether to use a new tor circuit for each request.
    proxy                  -- String indicating the proxy URL

    Return Value:
    Dictionary containing results from report.  Key of dictionary is the name
    of the social network site, and the value is another dictionary with
    the following keys:
        url_main:      URL of main site.
        url_user:      URL of user on site (if account exists).
        exists:        String indicating results of test for account existence.
        http_status:   HTTP status code of query which checked for existence on
                       site.
        response_text: Text that came back from request.  May be None if
                       there was an HTTP error when checking for existence.
    """
    global amount

    print_info("Checking username", username)

    # A user agent is needed because some sites don't
    # return the correct information since they think that
    # we are bots
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    # Allow 1 thread for each external service, so `len(site_data)` threads total
    executor = ThreadPoolExecutor(max_workers=len(site_data))

    # Create session based on request methodology
    underlying_session = requests.session()
    underlying_request = requests.Request()
    if tor or unique_tor:
        underlying_request = TorRequest()
        underlying_session = underlying_request.session

    # Create multi-threaded session for all requests. Use our custom FuturesSession that exposes response time
    session = ElapsedFuturesSession(
        executor=executor, session=underlying_session)

    # Results from analysis of all sites
    results_total = {}

    # First create futures for all requests. This allows for the requests to run in parallel
    for social_network, net_info in site_data.items():

        # Results from analysis of this specific site
        results_site = {}

        # Record URL of main site
        results_site['url_main'] = net_info.get("urlMain")

        # Don't make request if username is invalid for the site
        regex_check = net_info.get("regexCheck")
        if regex_check and re.search(regex_check, username) is None:
            # No need to do the check at the site: this user name is not allowed.
            print_invalid(social_network, "Illegal Username Format For This Site!")
            results_site["exists"] = "illegal"
            results_site["url_user"] = ""
            results_site['http_status'] = ""
            results_site['response_text'] = ""
            results_site['response_time_ms'] = ""
        else:
            # URL of user on site (if it exists)
            url = net_info["url"].format(username)
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            if url_probe is None:
                #Probe URL is normal one seen by people out on the web.
                url_probe = url
            else:
                #There is a special URL for probing existence separate
                #from where the user profile normally can be found.
                url_probe = url_probe.format(username)

            request_method = session.get
            if social_network != "GitHub":
                # If only the status_code is needed don't download the body
                if net_info["errorType"] == 'status_code':
                    request_method = session.head

            if net_info["errorType"] == "response_url":
                # Site forwards request to a different URL if username not
                # found.  Disallow the redirect so we can capture the
                # http status from the original URL request.
                allow_redirects = False
            else:
                # Allow whatever redirect that the site wants to do.
                # The final result of the request will be what is available.
                allow_redirects = True

            # This future starts running the request in a new thread, doesn't block the main thread
            if proxy != None:
                proxies = {"http": proxy, "https": proxy}
                future = request_method(url=url_probe, headers=headers,
                                        proxies=proxies,
                                        allow_redirects=allow_redirects
                                        )
            else:
                future = request_method(url=url_probe, headers=headers,
                                        allow_redirects=allow_redirects
                                        )

            # Store future in data for access later
            net_info["request_future"] = future

            # Reset identify for tor (if needed)
            if unique_tor:
                underlying_request.reset_identity()

        # Add this site's results into final dictionary with all of the other results.
        results_total[social_network] = results_site

    # Open the file containing account links
    # Core logic: If tor requests, make them here. If multi-threaded requests, wait for responses
    for social_network, net_info in site_data.items():

        # Retrieve results again
        results_site = results_total.get(social_network)

        # Retrieve other site information again
        url = results_site.get("url_user")
        exists = results_site.get("exists")
        if exists is not None:
            # We have already determined the user doesn't exist here
            continue

        # Get the expected error type
        error_type = net_info["errorType"]

        # Default data in case there are any failures in doing a request.
        http_status = "?"
        response_text = ""

        # Retrieve future and ensure it has finished
        future = net_info["request_future"]
        r, error_type, response_time = get_response(request_future=future,
                                                    error_type=error_type,
                                                    social_network=social_network,
                                                    verbose=verbose,
                                                    retry_no=3)

        # Attempt to get request information
        try:
            http_status = r.status_code
        except:
            pass
        try:
            response_text = r.text.encode(r.encoding)
        except:
            pass

        if error_type == "message":
            error = net_info.get("errorMsg")
            # Checks if the error message is in the HTML
            if not error in r.text:
                print_found(social_network, url, response_time, verbose)
                exists = "yes"
                amount = amount+1
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose)
                exists = "no"

        elif error_type == "status_code":
            # Checks if the status code of the response is 2XX
            if not r.status_code >= 300 or r.status_code < 200:
                print_found(social_network, url, response_time, verbose)
                exists = "yes"
                amount = amount+1
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose)
                exists = "no"

        elif error_type == "response_url":
            # For this detection method, we have turned off the redirect.
            # So, there is no need to check the response URL: it will always
            # match the request.  Instead, we will ensure that the response
            # code indicates that the request was successful (i.e. no 404, or
            # forward to some odd redirect).
            if 200 <= r.status_code < 300:
                #
                print_found(social_network, url, response_time, verbose)
                exists = "yes"
                amount = amount+1
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose)
                exists = "no"

        elif error_type == "":
            if not print_found_only:
                print_invalid(social_network, "Error!")
            exists = "error"

        # Save exists flag
        results_site['exists'] = exists

        # Save results from request
        results_site['http_status'] = http_status
        results_site['response_text'] = response_text
        results_site['response_time_ms'] = response_time

        # Add this site's results into final dictionary with all of the other results.
        results_total[social_network] = results_site
    return results_total

class Sherlock_(Resource):
    def post(self, userName):
        # Colorama module's initialization.
        init(autoreset=True)

        version_string = f"%(prog)s {__version__}\n" +  \
                        f"{requests.__description__}:  {requests.__version__}\n" + \
                        f"Python:  {platform.python_version()}"

        parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                                description=f"{module_name} (Version {__version__})"
                                )
        parser.add_argument("--version",
                            action="version",  version=version_string,
                            help="Display version information and dependencies."
                            )
        parser.add_argument("--verbose", "-v", "-d", "--debug",
                            action="store_true",  dest="verbose", default=False,
                            help="Display extra debugging information and metrics."
                            )
        parser.add_argument("--rank", "-r",
                            action="store_true", dest="rank", default=False,
                            help="Present websites ordered by their Alexa.com global rank in popularity.")
        parser.add_argument("--folderoutput", "-fo", dest="folderoutput",
                            help="If using multiple usernames, the output of the results will be saved at this folder."
                            )
        parser.add_argument("--output", "-o", dest="output",
                            help="If using single username, the output of the result will be saved at this file."
                            )
        parser.add_argument("--tor", "-t",
                            action="store_true", dest="tor", default=False,
                            help="Make requests over Tor; increases runtime; requires Tor to be installed and in system path.")
        parser.add_argument("--unique-tor", "-u",
                            action="store_true", dest="unique_tor", default=False,
                            help="Make requests over Tor with new Tor circuit after each request; increases runtime; requires Tor to be installed and in system path.")
        parser.add_argument("--csv",
                            action="store_true",  dest="csv", default=False,
                            help="Create Comma-Separated Values (CSV) File."
                            )
        parser.add_argument("--site",
                            action="append", metavar='SITE_NAME',
                            dest="site_list", default=None,
                            help="Limit analysis to just the listed sites.  Add multiple options to specify more than one site."
                            )
        parser.add_argument("--proxy", "-p", metavar='PROXY_URL',
                            action="store", dest="proxy", default=None,
                            help="Make requests over a proxy. e.g. socks5://127.0.0.1:1080"
                            )
        parser.add_argument("--json", "-j", metavar="JSON_FILE",
                            dest="json_file", default="data.json",
                            help="Load data from a JSON file or an online, valid, JSON file.")
        parser.add_argument("--proxy_list", "-pl", metavar='PROXY_LIST',
                            action="store", dest="proxy_list", default=None,
                            help="Make requests over a proxy randomly chosen from a list generated from a .csv file."
                            )
        parser.add_argument("--check_proxies", "-cp", metavar='CHECK_PROXY',
                            action="store", dest="check_prox", default=None,
                            help="To be used with the '--proxy_list' parameter. "
                                "The script will check if the proxies supplied in the .csv file are working and anonymous."
                                "Put 0 for no limit on successfully checked proxies, or another number to institute a limit."
                            )
        parser.add_argument("--print-found",
                            action="store_true", dest="print_found_only", default=False,
                            help="Do not output sites where the username was not found."
                            )
        '''parser.add_argument("username",
                            nargs='+', metavar='USERNAMES',
                            action="store",
                            help="One or more usernames to check with social networks."
                            )'''

        args = parser.parse_args()
        #args.username = list(userName.split(" "))
        usernames = [userName]
        args.output = "result.txt"
        # Argument check
        # TODO regex check on args.proxy
        if args.tor and (args.proxy != None or args.proxy_list != None):
            raise Exception("Tor and Proxy cannot be set in the meantime.")

        # Proxy argument check.
        # Does not necessarily need to throw an error,
        # since we could join the single proxy with the ones generated from the .csv,
        # but it seems unnecessarily complex at this time.
        if args.proxy != None and args.proxy_list != None:
            raise Exception("A single proxy cannot be used along with proxy list.")

        # Make prompts
        if args.proxy != None:
            print("Using the proxy: " + args.proxy)

        global proxy_list

        if args.proxy_list != None:
            print_info("Loading proxies from", args.proxy_list)

            proxy_list = load_proxies_from_csv(args.proxy_list)

        # Checking if proxies should be checked for anonymity.
        if args.check_prox != None and args.proxy_list != None:
            try:
                limit = int(args.check_prox)
                if limit == 0:
                    proxy_list = check_proxy_list(proxy_list)
                elif limit > 0:
                    proxy_list = check_proxy_list(proxy_list, limit)
                else:
                    raise ValueError
            except ValueError:
                raise Exception("Prameter --check_proxies/-cp must be a positive intiger.")

        if args.tor or args.unique_tor:
            print("Using Tor to make requests")
            print("Warning: some websites might refuse connecting over Tor, so note that using this option might increase connection errors.")

        # Check if both output methods are entered as input.
        if args.output is not None and args.folderoutput is not None:
            print("You can only use one of the output methods.")
            sys.exit(1)

        # Check validity for single username output.
        if args.output is not None and len(usernames) != 1:
            print("You can only use --output with a single username")
            sys.exit(1)

        response_json_online = None
        site_data_all = None

        # Try to load json from website.
        try:
            response_json_online = requests.get(url=args.json_file)
        except requests.exceptions.MissingSchema:  # In case the schema is wrong it's because it may not be a website
            pass

        # Check if the response is appropriate.
        if response_json_online is not None and response_json_online.status_code == 200:
            # Since we got data from a website, try to load json and exit if parsing fails.
            try:
                site_data_all = response_json_online.json()
            except ValueError:
                print("Invalid JSON from website!")
                sys.exit(1)
                pass

        data_file_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), args.json_file)
        # This will be none if the request had a missing schema
        if site_data_all is None:
            # Check if the file exists otherwise exit.
            if not os.path.exists(data_file_path):
                print("JSON file at doesn't exist.")
                print(
                    "If this is not a file but a website, make sure you have appended http:// or https://.")
                sys.exit(1)
            else:
                raw = open(data_file_path, "r", encoding="utf-8")
                try:
                    site_data_all = json.load(raw)
                except:
                    print("Invalid JSON loaded from file.")

        if args.site_list is None:
            # Not desired to look at a sub-set of sites
            site_data = site_data_all
        else:
            # User desires to selectively run queries on a sub-set of the site list.

            # Make sure that the sites are supported & build up pruned site database.
            site_data = {}
            site_missing = []
            for site in args.site_list:
                for existing_site in site_data_all:
                    if site.lower() == existing_site.lower():
                        site_data[existing_site] = site_data_all[existing_site]
                if not site_data:
                    # Build up list of sites not supported for future error message.
                    site_missing.append(f"'{site}'")

            if site_missing:
                print(
                    f"Error: Desired sites not found: {', '.join(site_missing)}.")
                sys.exit(1)

        if args.rank:
            # Sort data by rank
            site_dataCpy = dict(site_data)
            ranked_sites = sorted(site_data, key=lambda k: ("rank" not in k, site_data[k].get("rank", sys.maxsize)))
            site_data = {}
            for site in ranked_sites:
                site_data[site] = site_dataCpy.get(site)

        # Run report on all specified users.
        for username in usernames:
            
            print()

            if args.output:
                file = open(args.output, "w", encoding="utf-8")
            elif args.folderoutput:  # In case we handle multiple usernames at a targetted folder.
                # If the folder doesnt exist, create it first
                if not os.path.isdir(args.folderoutput):
                    os.mkdir(args.folderoutput)
                file = open(os.path.join(args.folderoutput,
                                        username + ".txt"), "w", encoding="utf-8")
            else:
                file = open(username + ".txt", "w", encoding="utf-8")

            # We try to ad a random member of the 'proxy_list' var as the proxy of the request.
            # If we can't access the list or it is empty, we proceed with args.proxy as the proxy.
            try:
                random_proxy = random.choice(proxy_list)
                proxy = f'{random_proxy.protocol}://{random_proxy.ip}:{random_proxy.port}'
            except (NameError, IndexError):
                proxy = args.proxy

            results = {}
            results = sherlock(username, site_data, verbose=args.verbose,
                            tor=args.tor, unique_tor=args.unique_tor, proxy=args.proxy, print_found_only=args.print_found_only)

            exists_counter = 0
            for website_name in results:
                dictionary = results[website_name]
                if dictionary.get("exists") == "yes":
                    exists_counter += 1
                    file.write(dictionary["url_user"] + "\n")
            file.write("Total Websites : {}".format(exists_counter))
            file.close()

            if args.csv == True:
                with open(username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
                    writer = csv.writer(csv_report)
                    writer.writerow(['username',
                                    'name',
                                    'url_main',
                                    'url_user',
                                    'exists',
                                    'http_status',
                                    'response_time_ms'
                                    ]
                                    )
                    for site in results:
                        writer.writerow([username,
                                        site,
                                        results[site]['url_main'],
                                        results[site]['url_user'],
                                        results[site]['exists'],
                                        results[site]['http_status'],
                                        results[site]['response_time_ms']
                                        ]
                                        )
        return userName, 201
    
    def get(self, userName):
        url = []
        with open("result.txt") as f:
            url = f.readlines()

        for i in range(len(url)):
            url[i] = url[i].replace("\n", "")

        results = {
            "username" : userName,
            "url" : url
        }
        return results, 200
    


if __name__ == "__main__":
    #main()
    api.add_resource(Sherlock_, "/sherlock/<string:userName>")
    #api.add_resource(TheHarvester, "/theHarvester/<string:target>")
    app.run(debug=True, port=5009, threaded=True)
