#!/usr/bin/env python

from ipwhois import IPWhois
import sys
from termcolor import colored

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '[+] Getting WHOIS Information' + style.END)


def main(ip):
    obj = IPWhois(ip)
    try:
        results = obj.lookup_rdap(depth=1)
    except:
        results = None
    return results


def output(data, ip=""):
    if not data:
        print 'ASN Registry Lookup Failed'
    else:
        print colored(style.BOLD + '--------------- Basic Info ---------------' + style.END, 'blue')
        print 'ASN ID: %s' % data['asn']
        if 'network' in data.keys():
            print 'Org. Name: %s' % data['network']['name']
            print 'CIDR Range: %s' % data['network']['cidr']
            print 'Start Address: %s' % data['network']['start_address']
            print 'Parent Handle: %s' % data['network']['parent_handle']
            print 'Country: %s' % data['network']['country']
        if 'objects' and 'entities' in data.keys():
            print colored(style.BOLD + '\n----------- Per Handle Results -----------' + style.END, 'blue')
            for x in data['entities']:
                print 'Handle: %s' % x
                if 'contact' in data['objects'][x].keys():
                    print '\tKind: %s' % data['objects'][x]['contact']['kind']
                    if data['objects'][x]['contact']['phone'] is not None:
                        for y in data['objects'][x]['contact']['phone']:
                            print '\tPhone: %s' % y['value']
                    if data['objects'][x]['contact']['title'] is not None:
                        print data['objects'][x]['contact']['title']
                    if data['objects'][x]['contact']['role'] is not None:
                        print data['objects'][x]['contact']['role']
                    if data['objects'][x]['contact']['address'] is not None:
                        for y in data['objects'][x]['contact']['address']:
                            print '\tAddress: %s' % y['value'].replace('\n', ',')
                    if data['objects'][x]['contact']['email'] is not None:
                        for y in data['objects'][x]['contact']['email']:
                            print '\tEmail: %s' % y['value']
    print ""


if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        banner()
        result = main(ip)
        output(result, ip)
    except Exception as e:
        print e
        print "Please provide an IP Address as argument"
