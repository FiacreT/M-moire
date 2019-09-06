from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from termcolor import cprint
from re import search, findall
from requests.exceptions import HTTPError
import requests
from requests import get
import re
from .link_io import LinkIO


def execute_all(link, *, display_status=False):


    keys = set() # high entropy strings, prolly secret keys
    files = set() # pdf, css, png etc.
    intel = set() # emails, website accounts, aws buckets etc.
    robots = set() # entries of robots.txt
    custom = set() # string extracted by custom regex pattern
    failed = set() # urls that photon failed to crawl
    scripts = set() # javascript files
    external = set() # urls that don't belong to the target i.e. out-of-scope
    fuzzable = set() # urls that have get params in them e.g. example.com/page.php?id=2
    endpoints = set() # urls found from javascript files
    processed = set() # urls that have been crawled

    everything = []
    bad_intel = set() # unclean intel urls
    bad_scripts = set() # unclean javascript file urls
    datasets = [files, intel, robots, custom, failed, scripts, external, fuzzable, endpoints, keys]
    dataset_names = ['files', 'intel', 'robots', 'custom', 'failed', 'scripts', 'external', 'fuzzable', 'endpoints', 'keys']
    page,response = LinkIO.read(link, response=True, show_msg=display_status)
    response = get(link, verify=False).text
    soup = BeautifulSoup(page, 'html.parser')
    validation_functions = [get_robots_txt, get_dot_git, get_dot_svn, get_dot_git, get_intel, get_bitcoin_address]
    for validate_func in validation_functions:
        try:
            validate_func(link,  response)
        except (ConnectionError, HTTPError):
            cprint('Error', 'red')

    display_webpage_description(soup)
    #display_headers(response)


def display_headers(response):
    print('''
          RESPONSE HEADERS
          __________________
          ''')
    for key, val in response.headers.items():
        print('*', key, ':', val)


def get_robots_txt(target,response):
    cprint("[*]Checking for Robots.txt", 'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    requests.get(target+"robots.txt")
    print(target+"robots.txt")
    matches = findall(r'Allow: (.*)|Disallow: (.*)', response)
    if matches:
        for match in matches:
            match = ''.join(match) 
            if '*' not in match:
                    url = main_url + match
                    robots.add(url) 
        cprint("Robots.txt found",'blue')
        print(robots)            


def get_intel(link,response):
    intel=set()
    matches = findall(r'''([\w\.-]+s[\w\.-]+\.amazonaws\.com)|([\w\.-]+@[\w\.-]+\.[\.\w]+)''', response)
    print("Intel\n--------\n\n")
    if matches:
        for match in matches: 
            intel.add(match) 


def get_dot_git(target,response):
    cprint("[*]Checking for .git folder", 'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    req = requests.get(target+"/.git/")
    status = req.status_code
    if status == 200:
        cprint("Alert!", 'red')
        cprint(".git folder exposed publicly", 'red')
    else:
        cprint("NO .git folder found", 'blue')


def get_bitcoin_address(target, response):
    bitcoins = re.findall(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', response)
    print("BTC FOUND: ", len(bitcoins))
    for bitcoin in bitcoins:
        print("BTC: ", bitcoin)


def get_dot_svn(target,response):
    cprint("[*]Checking for .svn folder", 'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    req = requests.get(target+"/.svn/entries")
    status = req.status_code
    if status == 200:
        cprint("Alert!", 'red')
        cprint(".SVN folder exposed publicly", 'red')
    else:
        cprint("NO .SVN folder found", 'blue')


def get_dot_htaccess(target,response):
    cprint("[*]Checking for .htaccess", 'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    req = requests.get(target+"/.htaccess")
    statcode = req.status_code
    if statcode == 403:
        cprint("403 Forbidden", 'blue')
    elif statcode == 200:
        cprint("Alert!!", 'blue')
        cprint(".htaccess file found!", 'blue')
    else:
        cprint("Status code", 'blue')
        cprint(statcode)


def display_webpage_description(soup):
    cprint("[*]Checking for meta tag", 'yellow')
    metatags = soup.find_all('meta')
    for meta in metatags:
        print("Meta : ",meta)


def writer(datasets, dataset_names, output_dir):
    for dataset, dataset_name in zip(datasets, dataset_names):
        if dataset:
            filepath = output_dir + '/' + dataset_name + '.txt'
            if python3:
                with open(filepath, 'w+', encoding='utf8') as f:
                    f.write(str('\n'.join(dataset)))
                    f.write('\n')
            else:
                with open(filepath, 'w+') as f:
                    joined = '\n'.join(dataset)
                    f.write(str(joined.encode('utf-8')))
                    f.write('\n')                
