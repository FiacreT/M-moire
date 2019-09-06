#!/usr/bin/python3
"""
The Automater.py module defines the main() function for Automater.

Parameter Required is:
target -- List one IP Address (CIDR or dash notation accepted), URL or Hash
to query or pass the filename of a file containing IP Address info, URL or
Hash to query each separated by a newline.

Optional Parameters are:
-o, --output -- This option will output the results to a file.
-b, --bot -- This option will output minimized results for a bot.
-f, --cef -- This option will output the results to a CEF formatted file.
-w, --web -- This option will output the results to an HTML file.
-c, --csv -- This option will output the results to a CSV file.
-d, --delay -- Change the delay to the inputted seconds. Default is 2.
-s, --source -- Will only run the target against a specific source engine
to pull associated domains. Options are defined in the name attribute of
the site element in the XML configuration file. This can be a list of names separated by a semicolon.
--proxy -- This option will set a proxy (eg. proxy.example.com:8080)
-a --useragent -- Will set a user-agent string in the header of a web request.
is set by default to Automater/version#
-V, --vercheck -- This option checks and reports versioning for Automater. Checks each python
module in the Automater scope.  Default, (no -V) is False
-r, --refreshxml -- This option refreshes the tekdefense.xml file from the remote GitHub site.
Default (no -r) is False.
-v, --verbose -- This option prints messages to the screen. Default (no -v) is False.

Class(es):
No classes are defined in this module.

Function(s):
main -- Provides the instantiation point for Automater.

Exception(s):
No exceptions exported.
"""

import sys
from siteinfo import SiteFacade, Site
from utilities import Parser, IPWrapper
from outputs import SiteDetailOutput
from inputs import TargetFile
import urllib3

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
results = []

class Automater(Resource):

    

    def post(self, cible):
        """
        Serves as the instantiation point to start Automater.

        Argument(s):
        No arguments are required.

        Return value(s):
        Nothing is returned from this Method.

        Restriction(s):
        The Method has no restrictions.
        """
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        __VERSION__ = '0.21'
        __GITLOCATION__ = 'https://github.com/1aN0rmus/TekDefense-Automater'
        __GITFILEPREFIX__ = 'https://raw.githubusercontent.com/1aN0rmus/TekDefense-Automater/master/'

        sites = []
        parser = Parser('IP, URL, and Hash Passive Analysis tool', __VERSION__, cible)
        
        # if no target run and print help
        if parser.hasNoTarget():
            print ('[!] No argument given.')
            parser.print_help()  # need to fix this. Will later
            sys.exit()

        if parser.VersionCheck:
            Site.checkmoduleversion(__GITFILEPREFIX__, __GITLOCATION__, parser.Proxy, parser.Verbose)

        # user may only want to run against one source - allsources
        # is the seed used to check if the user did not enter an s tag
        sourcelist = ['allsources']
        if parser.hasSource():
            sourcelist = parser.Source.split(';')

        # a file input capability provides a possibility of
        # multiple lines of targets
        targetlist = []
        if parser.hasInputFile():
            for tgtstr in TargetFile.TargetList(parser.InputFile, parser.Verbose):
                tgtstrstripped = tgtstr.replace('[.]', '.').replace('{.}', '.').replace('(.)', '.')
                if IPWrapper.isIPorIPList(tgtstrstripped):
                    for targ in IPWrapper.getTarget(tgtstrstripped):
                        targetlist.append(targ)
                else:
                    targetlist.append(tgtstrstripped)
        else:  # one target or list of range of targets added on console
            #target = parser.Target
            
            target = cible
            #print("---------------------------------------------------------------------------------------------")
            #print(target)

            tgtstrstripped = target.replace('[.]', '.').replace('{.}', '.').replace('(.)', '.')
            if IPWrapper.isIPorIPList(tgtstrstripped):
                for targ in IPWrapper.getTarget(tgtstrstripped):
                    targetlist.append(targ)
            else:
                targetlist.append(tgtstrstripped)
        #print(targetlist)
        sitefac = SiteFacade(parser.Verbose)
        sitefac.runSiteAutomation(parser.Delay, parser.Proxy, targetlist, sourcelist, parser.UserAgent, parser.hasBotOut,
                                parser.RefreshRemoteXML, __GITLOCATION__)
        sites = sitefac.Sites
        if sites:
            resultTemp = SiteDetailOutput(sites).createOutputInfo(parser)
            #print("---------------------------------------------------------------------------------------------")
            #print(sites)
            #print("---------------------------------------------------------------------------------------------")
            
            #-------------------PARSE RESULT--------------------------------------
            tabTemp = resultTemp.split("\n")
            
            result = {}
            for i in range(len(tabTemp)):
                
                tabTemp[i] =  tabTemp[i].replace("[+]", "")
                tabTemp[i] = tabTemp[i].strip()
                if(":" in tabTemp[i]):
                    tab = tabTemp[i].split(":",1)
                    if (i==1):
                        result["target"] = tab[1].replace("____________________", " ").strip()
                    elif(tab[0] in result):
                        
                        result[tab[0]] = result[tab[0]] + " " +tab[1]
                    else:
                        result[tab[0]] = tab[1]
                
            results.append(result)
            #print(results)

        return result, 201
    
    def get(self, cible):
        
        for result in results:
            if(cible == result["target"]):
                return result, 200
        return "User not found", 404

if __name__ == "__main__":
    
    api.add_resource(Automater, "/automater/<string:cible>")
    app.run(debug=True, port=5001, threaded=True)

