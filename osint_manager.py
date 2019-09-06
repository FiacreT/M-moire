#!/usr/bin/env python3
import requests
import psycopg2
import ast
import json
import re
from flask import Flask, render_template, request

app = Flask(__name__)

class RequestApi:
    url = ''
    def __init__(self, target):
        self.url = 'http://localhost:5000/'+target

    def postApi(self):
        try:
            response = requests.post(self.url)
            result = response.text
        except requests.exceptions.RequestException as e:
            print(e)
            result = 'ERROR'
        return result
    
    def getApi(self):
        response = requests.get(self.url)

        if response:
            print("Success!")
            result = response.content
        else:
            print("Not Found")
            result = 'ERROR'
        return result


def contacts_store(target, first_name, middle_name, last_name, email, title, region, country, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO contacts (target, first_name, middle_name, last_name, email, title, region, country, tool) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, first_name, middle_name, last_name, email, title, region, country, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def hosts_store(target, host, ip_address, type_, region, country, latitude, longitude, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO hosts (target, host, ip_address, type, region, country, latitude, longitude, tool) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, host, ip_address, type_, region, country, latitude, longitude, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def domains_store(target, technologie, address, city, country, registar, other_info, dns_record, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO domains (target, technologie, address, city, country, registar, other_info, dns_record, tool) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, technologie, address, city, country, registar, other_info, dns_record, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def repositories_store(target, name, owner, description, resource, category, url, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO repositories (target, name, owner, description, resource, category, url, tool) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, name, owner, description, resource, category, url, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def profiles_store(target, username, resource, url, category, note, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO profiles (target, username, resource, url, category, note, tool) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, username, resource, url, category, note, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def ips_store(target, ip_whois, ip_shodan, ip_virustotal, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO ips (target, ip_whois, ip_shodan, ip_virustotal, tool) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (target, ip_whois, ip_shodan, ip_virustotal, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def emails_store(target, email_fullcontact, email_pastes, email_clearbit, email_haveibeenpwned, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO emails (target, email_fullcontact, email_pastes, email_clearbit, email_haveibeenpwned, tool) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, email_fullcontact, email_pastes, email_clearbit, email_haveibeenpwned, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def vulnerabilities_store(target, reference, example, publish_date, category, status, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO vulnerabilities (target, reference, example, publish_date, category, status, tool) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, reference, example, publish_date, category, status, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def credentials_store(target, username, password, hash_, type_, leak, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO credentials (target, username, password, hash, type, leak, tool) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, username, password, hash_, type, leak, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def locations_store(target, latitude, longitude, street_address, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO locations (target, latitude, longitude, street_address, tool) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (target, latitude, longitude, street_address, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def ports_store(target, ip_address, host, port, protocol, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO ports (target, ip_address, host, port, protocol, tool) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, ip_address, host, port, protocol, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def companies_store(target, company, description, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO companies (target, company, description, tool) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (target, company, description, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def pushpins_store(target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO pushpins (target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time, tool) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def darksearch_store(target, title, link, description, tool):
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432",
                                        database="osint_data")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO darksearch (target, title, link, description, tool) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (target, title, link, description, tool)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")



def request_theHarvester():
    #request to theHarvester  
    theHarvester = RequestApi('theHarvester/apple.com/bing')
    
    result_harvester = ast.literal_eval(theHarvester.postApi())
    print("----------------------------------------------------------------")
    print(result_harvester)
    #Store emails
    for email in result_harvester["emails"]:
        contacts_store(result_harvester["target"], '','', '', email,'','','','theHarvester')
    #contacts_store('apple.com', '','', '', 'me@yahoo.cm','','','','theHarvester')
    
    #Store hosts
    for host in result_harvester["host"]:
        hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')
    #hosts_store('apple.com', 'apple.com.music', '', '', '', '', '', '', 'theHarvester')

    for host in result_harvester["vhost"]:
        hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')
    
    for host in result_harvester["shodan"]:
        hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')


def request_dnsrecon(target):
    #dnsRecon
    dnsrecon = RequestApi('dnsrecon/'+target)
    result_dnsrecon = dnsrecon.postApi()
    result_dnsrecon = dnsrecon.getApi()
    result_dnsrecon = result_dnsrecon.decode("utf-8")
    result_dnsrecon = json.loads(result_dnsrecon)  
    data = result_dnsrecon["data"]

    host = ""
    ip_address = ""
    type_ = ""
    for i in range(len(data)):
        for key, val in data[i].items():
            if key == "name":
                host = val 
            if key == "target":
                host = host + "   target : "+ val
            if key == "address":
                ip_address = val
            if key == "type":
                type_ = val 
        hosts_store(result_dnsrecon["target"], host, ip_address, type_, "", "", "", "", "dnsrecon")



def request_automater(target):
    #automater
    automater = RequestApi('automater/'+target)
    result_automater = automater.postApi()
    print(result_automater)
    result_automater = automater.getApi()
    result_automater = result_automater.decode("utf-8")
    result_automater = json.loads(result_automater)

    reference = ""
    status = ""
    target = result_automater["target"]
    for key, val in result_automater.items():
        if key == "target":
            target = val 
        else:
            if("No results found" in val):
                reference = "" 
            else:
                reference = key 
                status = val
        if (reference !=""):
            vulnerabilities_store(target, reference, "", "", "", status, "automater")


def request_recon_company(target):
    #recon_company
    recon_company = RequestApi('recon_company/'+target)
    result_recon = recon_company.postApi()
    result_recon = json.loads(result_recon)
    for key, val in result_recon.items():
        if key =='contacts':
            for i in range(len(val)):
                first_name = val[i]["first_name"]
                middle_name = val[i]["middle_name"]
                last_name = val[i]["last_name"]
                email = val[i]["email"]
                title = val[i]["title"]
                region = val[i]["region"]
                country = val[i]["country"]
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")
        if key =='repositories':
            for i in range(len(val)):
                name = val[i]["name"]
                owner = val[i]["owner"]
                description = val[i]["description"]
                resource = val[i]["resource"]
                category = val[i]["category"]
                url = val[i]["url"]
                repositories_store(target, name, owner, description, resource, category, url, "recon-ng")

        if key =='profiles':
            for i in range(len(val)):
                username = val[i]["username"]
                resource = val[i]["resource"]
                url = val[i]["url"]
                category = val[i]["category"]
                note = val[i]["notes"]
                profiles_store(target, username, resource, url, category, note, "recon-ng")


def request_recon_contact(target):
    #recon_contact
    recon_contact = RequestApi('recon_contact/'+target)
    result_recon = recon_contact.postApi()
    result_recon = json.loads(result_recon)
    for key, val in result_recon.items():
        if key =='contacts':
            for i in range(len(val)):
                first_name = val[i]["first_name"]
                middle_name = val[i]["middle_name"]
                last_name = val[i]["last_name"]
                email = val[i]["email"]
                title = val[i]["title"]
                region = val[i]["region"]
                country = val[i]["country"]
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")

        if key =='credentials':
            for i in range(len(val)):
                username = val[i]["username"]
                password = val[i]["password"]
                hash_ = val[i]["hash"]
                type_ = val[i]["type"]
                leak = val[i]["leak"]
                credentials_store(target, username, password, hash_, type_, leak, "recon-ng")

        if key =='profiles':
            for i in range(len(val)):
                username = val[i]["username"]
                resource = val[i]["resource"]
                url = val[i]["url"]
                category = val[i]["category"]
                note = val[i]["notes"]
                profiles_store(target, username, resource, url, category, note, "recon-ng")


def request_recon_host(target):
    #recon_host
    recon_host = RequestApi('recon_host/'+target)
    result_recon = recon_host.postApi()
    result_recon = json.loads(result_recon)
    for key, val in result_recon.items():
        if key =='hosts':
            for i in range(len(val)):
                host = val[i]["host"]
                ip_address = val[i]["ip_address"]
                type_ = ""
                region = val[i]["region"]
                country = val[i]["country"]
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                hosts_store(target, host, ip_address, type_, region, country, latitude, longitude, "recon-ng")

        if key =='locations':
            for i in range(len(val)):
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                street_address = val[i]["street_address"]
                locations_store(target, latitude, longitude, street_address, "recon-ng")

        if key =='ports':
            for i in range(len(val)):
                ip_address = val[i]["ip_address"]
                host = val[i]["host"]
                port = val[i]["port"]
                protocol = val[i]["protocol"]
                ports_store(target, ip_address, host, port, protocol, "recon-ng")



def request_recon_location(target):
    #recon_location
    recon_location = RequestApi('recon_location/'+target)
    result_recon = recon_location.postApi()
    result_recon = json.loads(result_recon)
    for key, val in result_recon.items():
        if key =='locations':
            for i in range(len(val)):
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                street_address = val[i]["street_address"]
                locations_store(target, latitude, longitude, street_address, "recon-ng")

        if key =='pushpins':
            for i in range(len(val)):
                source = val[i]["source"]
                screen_name = val[i]["screen_name"]
                profile_name = val[i]["profile_name"]
                profile_url = val[i]["profile_url"]
                media_url = val[i]["media_url"]
                thumb_url = val[i]["thumb_url"]
                message = val[i]["message"]
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                time = val[i]["time"]
                pushpins_store(target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time, "recon-ng")



def request_recon_profile(target):
    #recon_profile
    recon_profile = RequestApi('recon_profile/'+target)
    result_recon = recon_profile.postApi()
    result_recon = json.loads(result_recon)
    for key, val in result_recon.items():
        if key =='contacts':
            for i in range(len(val)):
                first_name = val[i]["first_name"]
                middle_name = val[i]["middle_name"]
                last_name = val[i]["last_name"]
                email = val[i]["email"]
                title = val[i]["title"]
                region = val[i]["region"]
                country = val[i]["country"]
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")

        if key =='profiles':
            for i in range(len(val)):
                username = val[i]["username"]
                resource = val[i]["resource"]
                url = val[i]["url"]
                category = val[i]["category"]
                note = val[i]["notes"]
                profiles_store(target, username, resource, url, category, note, "recon-ng")

        if key =='repositories':
            for i in range(len(val)):
                name = val[i]["name"]
                owner = val[i]["owner"]
                description = val[i]["description"]
                resource = val[i]["resource"]
                category = val[i]["category"]
                url = val[i]["url"]
                repositories_store(target, name, owner, description, resource, category, url, "recon-ng")


def request_recon_domain(target):
    #recon_domain
    recon_domain = RequestApi('recon_domain/'+target)
    result_recon = recon_domain.postApi()
    result_recon = json.loads(result_recon)
    for key, val in result_recon.items():
        if key =='hosts':
            for i in range(len(val)):
                host = val[i]["host"]
                ip_address = val[i]["ip_address"]
                type_ = ""
                region = val[i]["region"]
                country = val[i]["country"]
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                hosts_store(target, host, ip_address, type_, region, country, latitude, longitude, "recon-ng")

        if key =='companies':
            for i in range(len(val)):
                company = val[i]["company"]
                description = val[i]["description"]
                companies_store(target, company, description, "recon-ng")
        if key =='contacts':
            for i in range(len(val)):
                first_name = val[i]["first_name"]
                middle_name = val[i]["middle_name"]
                last_name = val[i]["last_name"]
                email = val[i]["email"]
                title = val[i]["title"]
                region = val[i]["region"]
                country = val[i]["country"]
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")
        if key =='credentials':
            for i in range(len(val)):
                username = val[i]["username"]
                password = val[i]["password"]
                hash_ = val[i]["hash"]
                type_ = val[i]["type"]
                leak = val[i]["leak"]
                credentials_store(target, username, password, hash_, type_, leak, "recon-ng")
       
        if key =='vulnerabilities':
            for i in range(len(val)):
                reference = val[i]["reference"]
                example = val[i]["example"]
                publish_date = val[i]["publish_date"]
                category = val[i]["category"]
                status = val[i]["status"]
                vulnerabilities_store(target, reference, example, publish_date, category, status, "recon-ng")



def request_darksearch(target, n):
    darks = RequestApi("darksearch/"+target+"/"+str(n))
    result_darks = darks.postApi()
    print(result_darks)
    result_darks = json.loads(result_darks)
    data = result_darks["data"]
    print(data)
    for i in range(len(data)):
        title = data[i]["title"]
        link = data[i]["link"]
        description = data[i]["description"]
        darksearch_store(target, title, link, description, "darksearch")


def request_torBot(target):
    torBot_ = RequestApi("torBot/"+target)
    result_torBot = torBot_.postApi()
    #print(result_torBot)
    result_torBot = json.loads(result_torBot)
    data = result_torBot["result"]
    print(data)
    emails = result_torBot["email"]["emails"]
    for i in range(len(emails)):
        contacts_store(target, "", "", "", emails[i], "", "", "", "torBot")

    for i in range(len(data)):
        title = data[i]["title"]
        link = data[i]["link"]
        if link != "":
            darksearch_store(target, title, link, "", "torBot")


def request_datasploit(target):
    #request to dataSploit
    dataSploit = RequestApi('datasploit/'+target)
    result_datasploit = dataSploit.postApi()
    result_datasploit = dataSploit.getApi()
    result_datasploit = result_datasploit.decode("utf-8")
    result_datasploit = json.loads(result_datasploit)  
    data = result_datasploit["data"]

    if re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", target):
        #domain
        domain_shodan = {}
        domain_wappalyzer = {}
        domain_whois = {}
        domain_pagelinks = {}
        domain_github = {}
        domain_dnsrecords = {}
        domain_pastes = {}
        domain_googletracking = {}

        for i in range(len(data)):
            for key, val in data[i].items():
                if key == "domain_shodan":
                    domain_shodan = val
            
                if key == "domain_wappalyzer":
                    domain_wappalyzer = val
            
                if key == "domain_whois":
                    domain_whois = val
            
                if key == "domain_pagelinks":
                    domain_pagelinks = val
            
                if key == "domain_github":
                    domain_github = val

                if key == "domain_dnsrecords":
                    domain_dnsrecords = val

                if key == "domain_pastes":
                    domain_pastes = val

                if key == "domain_googletracking":
                    domain_googletracking = val

        http = domain_wappalyzer["HTTP"]
        https = domain_wappalyzer["HTTPS"]
        if len(http)!=0:
            technologie = ', '.join(http)
        if len(https)!=0:
            technologie = technologie + ', '.join(https)
        
        address = domain_whois["address"]
        city = domain_whois["city"]
        country = domain_whois["country"]
        registar = domain_whois["registrar"]
        for i in range(len(domain_googletracking)):
            domain_googletracking[i] = json.dumps(domain_googletracking[i])
        other_info = "googletracking : "+ ' ,'.join(domain_googletracking)
        dns_record = json.dumps(domain_dnsrecords)
        domains_store(result_datasploit["target"], technologie, address, city, country, registar, other_info, dns_record, "datasploit")

        for i in range(len(domain_github[1])):
            acount_git = domain_github[1][i]
            name = acount_git["repository"]["owner"]["login"]
            resource = "Github"
            category = "repo"
            url = acount_git["repository"]["owner"]["url"]
            tool = "datasploit"
            repositories_store(result_datasploit["target"], name, "", "", resource, category, url, tool)

    elif re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", target):
        #ip
        ip_whois=""
        ip_shodan=""
        ip_virustotal=""
        for i in range(len(data)):
            for key, val in data[i].items():
                if key == "ip_whois":
                    ip_whois = json.dumps(val)
                if key == "ip_shodan":
                    ip_shodan = json.dumps(val)
                if key == "ip_virustotal":
                    ip_virustotal = json.dumps(val)
        ips_store(result_datasploit["target"], ip_whois, ip_shodan, ip_virustotal, "datasploit")
    
    elif re.match('[^@]+@[^@]+\.[^@]+', target):
        #email
        email_fullcontact = ""
        email_pastes = ""
        email_clearbit = ""
        email_haveibeenpwned = ""
        for i in range(len(data)):
            for key, val in data[i].items():
                if key == "email_fullcontact":
                    email_fullcontact = json.dumps(val)
                if key == "email_pastes":
                    email_pastes = json.dumps(val)
                if key == "email_clearbit":
                    email_clearbit = json.dumps(val)
                if key == "email_haveibeenpwned":
                    email_haveibeenpwned = json.dumps(val)
        emails_store(result_datasploit["target"], email_fullcontact, email_pastes, email_clearbit, email_haveibeenpwned, "datasploit")
    else:
        #username
        for i in range(len(data)):
            for key, val in data[i].items():
                if key == "username_usernamesearch":
                    username = result_datasploit["target"]
                    for j in range(len(val)):
                        resource = val[j].split("/")[2]
                        url = val[j]
                        category = "social"
                        tool = "datasploit"
                        profiles_store(username, username, resource, url, category, "", tool)
    



@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        # afficher le formulaire
        return render_template('search_osint.html')
    else:
        # traiter les données reçues
        result = request.form
        print(result)





if __name__ == '__main__':
   app.run(debug = True)




'''
if __name__ == '__main__':
    
    #request to torBot
    torBotApi = RequestApi('torBot/torlinkbgs6aabns.onion')
    torBotApi.postApi()

    request_torBot("torlinkbgs6aabns.onion")'''











    









    
    

    
    
    

    

          






'''r = requests.post('http://localhost:5000/torBot/torlinkbgs6aabns.onion')
print(r.request.url)
print(r.request.body)
print('----------------------------result--------------------------------')
#print(r.text)
response = requests.get('http://localhost:5000/torBot/torlinkbgs6aabns.onion')

if response.status_code == 200:
    print('---------------------------------------------------Success!')
    print(response.content)
elif response.status_code == 404:
    print('----------------------------------------------Not Found.')



try:
    r = requests.get(url, params={'s': thing})
except requests.exceptions.RequestException as e:  # This is the correct syntax
    print e
    sys.exit(1)'''















