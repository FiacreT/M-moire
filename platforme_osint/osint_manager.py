#!/usr/bin/env python3
import requests
import psycopg2
import ast
import json
import re
from flask import Flask, render_template, request
from flask_table import Table, Col

app = Flask(__name__)



items_companies = []
items_contacts = []
items_credentials = []
items_darksearch = []
items_domains = []
items_emails = []
items_hosts = []
items_ips = []
items_locations = []
items_ports = []
items_profiles = []
items_pushpins = []
items_repositories = []
items_vulnerabilities = []

class RequestApi:
    url = ''
    def __init__(self, target):
        self.url = 'http://localhost:'+target
        print("--------------------------------------------------------------------")
        print(self.url)

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




#--------------------------------------------------------------------------------------------------------------
#Items

# Declare your table
class ItemTable_companies(Table):
    target = Col('Target')
    company = Col('Company')
    description = Col('Description')

# Get some objects
class Item_companies(object):
    def __init__(self, target, company, description):
        self.target = target
        self.company = company
        self.description = description



# Declare your table
class ItemTable_contacts(Table):
    target = Col('Target')
    first_name = Col('First name')
    middle_name = Col('Middle name')
    last_name = Col('Last name')
    email = Col('Email')
    title = Col('Title')
    region = Col('Region')
    country = Col('Country')

# Get some objects
class Item_contacts(object):
    def __init__(self, target, first_name, middle_name, last_name, email, title, region, country):
        self.target = target
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.title = title
        self.region = region
        self.country = country



# Declare your table
class ItemTable_credentials(Table):
    target = Col('Target')
    username = Col('Username')
    password = Col('Password')
    hash_ = Col('Hash')
    type_ = Col('Type')
    leak = Col('Leak')

# Get some objects
class Item_credentials(object):
    def __init__(self, target, username, password, hash_, type_, leak):
        self.target = target
        self.username = username
        self.password = password
        self.hash_ = hash_
        self.type_ = type_
        self.leak = leak



# Declare your table
class ItemTable_darksearch(Table):
    target = Col('Target')
    title = Col('Title')
    link = Col('Link')
    description = Col('Description')

# Get some objects
class Item_darksearch(object):
    def __init__(self, target, title, link, description):
        self.target = target
        self.title = title
        self.link = link
        self.description = description



# Declare your table
class ItemTable_domains(Table):
    target = Col('Target')
    technologie = Col('Technologie')
    address = Col('Address')
    city = Col('City')
    country = Col('Country')
    registar = Col('Registar')
    other_info = Col('Other info')
    dns_record = Col('Dns record')

# Get some objects
class Item_domains(object):
    def __init__(self, target, technologie, address, city, country, registar, other_info, dns_record):
        self.target = target
        self.technologie = technologie
        self.address = address
        self.city = city
        self.country = country
        self.registar = registar
        self.other_info = other_info
        self.dns_record = dns_record



# Declare your table
class ItemTable_emails(Table):
    target = Col('Target')
    email_fullcontact = Col('email_fullcontact')
    email_pastes = Col('email_pastes')
    email_clearbit = Col('email_clearbit')
    email_haveibeenpwned = Col('email_haveibeenpwned')

# Get some objects
class Item_emails(object):
    def __init__(self, target, email_fullcontact, email_pastes, email_clearbit, email_haveibeenpwned):
        self.target = target
        self.email_fullcontact = email_fullcontact
        self.email_pastes = email_pastes
        self.email_clearbit = email_clearbit
        self.email_haveibeenpwned = email_haveibeenpwned



# Declare your table
class ItemTable_hosts(Table):
    target = Col('Target')
    host = Col('Host')
    ip_address = Col('ip_address')
    type_ = Col('Type_')
    region = Col('Region')
    country = Col('Country')
    latitude = Col('Latitude')
    longitude = Col('Longitude')

# Get some objects
class Item_hosts(object):
    def __init__(self, target, host, ip_address, type_, region, country, latitude, longitude):
        self.target = target
        self.host = host
        self.ip_address = ip_address
        self.type_ = type_
        self.region = region
        self.country = country
        self.latitude = latitude
        self.longitude = longitude



# Declare your table
class ItemTable_ips(Table):
    target = Col('Target')
    ip_whois = Col('ip_whois')
    ip_shodan = Col('ip_shodan')
    ip_virustotal = Col('ip_virustotal')

# Get some objects
class Item_ips(object):
    def __init__(self, target, ip_whois, ip_shodan, ip_virustotal):
        self.target = target
        self.ip_whois = ip_whois
        self.ip_shodan = ip_shodan
        self.ip_virustotal = ip_virustotal



# Declare your table
class ItemTable_locations(Table):
    target = Col('Target')
    latitude = Col('Latitude')
    longitude = Col('Longitude')
    street_address = Col('Street address')

# Get some objects
class Item_locations(object):
    def __init__(self, target, latitude, longitude, street_address):
        self.target = target
        self.latitude = latitude
        self.longitude = longitude
        self.street_address = street_address



# Declare your table
class ItemTable_ports(Table):
    target = Col('Target')
    ip_address = Col('ip_address')
    host = Col('Host')
    port = Col('Port')
    protocol = Col('Protocol')

# Get some objects
class Item_ports(object):
    def __init__(self, target, ip_address, host, port, protocol):
        self.target = target
        self.ip_address = ip_address
        self.host = host
        self.port = port
        self.protocol = protocol



# Declare your table
class ItemTable_profiles(Table):
    target = Col('Target')
    username = Col('Username')
    resource = Col('Resource')
    url = Col('Url')
    category = Col('Category')
    note = Col('Note')

# Get some objects
class Item_profiles(object):
    def __init__(self, target, username, resource, url, category, note):
        self.target = target
        self.username = username
        self.resource = resource
        self.url = url
        self.category = category
        self.note = note



# Declare your table
class ItemTable_pushpins(Table):
    target = Col('Target')
    source = Col('Source')
    screen_name = Col('Screen name')
    profile_name = Col('Profile name')
    profile_url = Col('Profile url')
    media_url = Col('Media url')
    thumb_url = Col('Thumb url')
    message = Col('Message')
    latitude = Col('Latitude')
    longitude = Col('Tongitude')
    time = Col('Time')

# Get some objects
class Item_pushpins(object):
    def __init__(self, target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time):
        self.target = target
        self.source = source
        self.screen_name = screen_name
        self.profile_name = profile_name
        self.profile_url = profile_url
        self.media_url = media_url
        self.thumb_url = thumb_url
        self.message = message
        self.latitude = latitude
        self.longitude = longitude
        self.time = time



# Declare your table
class ItemTable_repositories(Table):
    target = Col('Target')
    name = Col('Name')
    owner = Col('Owner')
    description = Col('Description')
    resource = Col('Resource')
    category = Col('Category')
    url = Col('Url')

# Get some objects
class Item_repositories(object):
    def __init__(self, target, name, owner, description, resource, category, url):
        self.target = target
        self.name = name
        self.owner = owner
        self.description = description
        self.resource = resource
        self.category = category
        self.url = url



# Declare your table
class ItemTable_vulnerabilities(Table):
    target = Col('Target')
    reference = Col('reference')
    example = Col('example')
    publish_date = Col('publish_date')
    category = Col('category')
    status = Col('status')

# Get some objects
class Item_vulnerabilities(object):
    def __init__(self, target, reference, example, publish_date, category, status):
        self.target = target
        self.reference = reference
        self.example = example
        self.publish_date = publish_date
        self.category = category
        self.status = status






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



def request_theHarvester(target, port):
    #request to theHarvester  
    theHarvester = RequestApi(str(port)+'/theHarvester/'+target+'/'+'baidu')
    
    result_harvester = ast.literal_eval(theHarvester.postApi())
    #result_harvester = json.loads(theHarvester.postApi())
    items_contacts.clear()
    items_hosts.clear()

    #Store emails
    for email in result_harvester["emails"]:
        items_contacts.append(Item_contacts(result_harvester["target"], '','', '', email,'','',''))
        contacts_store(result_harvester["target"], '','', '', email,'','','','theHarvester')
    
    #Store hosts
    for host in result_harvester["host"]:
        items_hosts.append(Item_hosts(result_harvester["target"], host, '', '', '', '', '', ''))
        hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')

    for host in result_harvester["vhost"]:
        items_hosts.append(Item_hosts(result_harvester["target"], host, '', '', '', '', '', ''))
        hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')
    
    for host in result_harvester["shodan"]:
        items_hosts.append(Item_hosts(result_harvester["target"], host, '', '', '', '', '', ''))
        hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')


def request_dnsrecon(target, port):
    #dnsRecon
    dnsrecon = RequestApi(str(port)+'/dnsrecon/'+target)
    result_dnsrecon = dnsrecon.postApi()
    result_dnsrecon = dnsrecon.getApi()
    #result_dnsrecon = result_dnsrecon.decode("utf-8")
    result_dnsrecon = json.loads(result_dnsrecon)  
    data = result_dnsrecon["data"]
    host = ""
    ip_address = ""
    type_ = ""
    items_hosts.clear()
    
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
        items_hosts.append(Item_hosts(result_dnsrecon["target"], host, ip_address, type_, "", "", "", "")) 
        hosts_store(result_dnsrecon["target"], host, ip_address, type_, "", "", "", "", "dnsrecon")



def request_automater(target, port):
    #automater
    automater = RequestApi(str(port)+'/automater/'+target)
    result_automater = automater.postApi()
    print(result_automater)
    result_automater = automater.getApi()
    result_automater = result_automater.decode("utf-8")
    result_automater = json.loads(result_automater)
    reference = ""
    status = ""
    target = result_automater["target"]
    items_vulnerabilities.clear()

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
            items_vulnerabilities.append(Item_vulnerabilities(target, reference, "", "", "", status))
            vulnerabilities_store(target, reference, "", "", "", status, "automater")


def request_recon_company(target, port):
    #recon_company
    recon_company = RequestApi(str(port)+'/recon_company/'+target)
    result_recon = recon_company.postApi()
    result_recon = json.loads(result_recon)
    items_contacts.clear()
    items_repositories.clear()
    items_profiles.clear()

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
                items_contacts.append(Item_contacts(target, first_name, middle_name, last_name, email, title, region, country))
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")
        if key =='repositories':
            for i in range(len(val)):
                name = val[i]["name"]
                owner = val[i]["owner"]
                description = val[i]["description"]
                resource = val[i]["resource"]
                category = val[i]["category"]
                url = val[i]["url"]
                items_repositories.append(Item_repositories(target, name, owner, description, resource, category, url))
                repositories_store(target, name, owner, description, resource, category, url, "recon-ng")

        if key =='profiles':
            for i in range(len(val)):
                username = val[i]["username"]
                resource = val[i]["resource"]
                url = val[i]["url"]
                category = val[i]["category"]
                note = val[i]["notes"]
                items_profiles.append(Item_profiles(target, username, resource, url, category, note))
                profiles_store(target, username, resource, url, category, note, "recon-ng")


def request_recon_contact(target, port):
    #recon_contact
    recon_contact = RequestApi(str(port)+'/recon_contact/'+target)
    result_recon = recon_contact.postApi()
    result_recon = json.loads(result_recon)
    items_contacts.clear()
    items_credentials.clear()
    items_profiles.clear()

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
                items_contacts.append(Item_contacts(target, first_name, middle_name, last_name, email, title, region, country))
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")

        if key =='credentials':
            for i in range(len(val)):
                username = val[i]["username"]
                password = val[i]["password"]
                hash_ = val[i]["hash"]
                type_ = val[i]["type"]
                leak = val[i]["leak"]
                items_credentials.append(Item_credentials(target, username, password, hash_, type_, leak))
                credentials_store(target, username, password, hash_, type_, leak, "recon-ng")

        if key =='profiles':
            for i in range(len(val)):
                username = val[i]["username"]
                resource = val[i]["resource"]
                url = val[i]["url"]
                category = val[i]["category"]
                note = val[i]["notes"]
                items_profiles.append(Item_profiles(target, username, resource, url, category, note))
                profiles_store(target, username, resource, url, category, note, "recon-ng")


def request_recon_host(target, port):
    #recon_host
    recon_host = RequestApi(str(port)+'/recon_host/'+target)
    result_recon = recon_host.postApi()
    result_recon = json.loads(result_recon)
    items_hosts.clear()
    items_locations.clear()
    items_ports.clear()

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
                items_hosts.append(Item_hosts(target, host, ip_address, type_, region, country, latitude, longitude))
                hosts_store(target, host, ip_address, type_, region, country, latitude, longitude, "recon-ng")

        if key =='locations':
            for i in range(len(val)):
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                street_address = val[i]["street_address"]
                items_locations.append(Item_locations(target, latitude, longitude, street_address))
                locations_store(target, latitude, longitude, street_address, "recon-ng")

        if key =='ports':
            for i in range(len(val)):
                ip_address = val[i]["ip_address"]
                host = val[i]["host"]
                port = val[i]["port"]
                protocol = val[i]["protocol"]
                items_ports.append(Item_ports(target, ip_address, host, port, protocol))
                ports_store(target, ip_address, host, port, protocol, "recon-ng")



def request_recon_location(target, port):
    #recon_location
    recon_location = RequestApi(str(port)+'/recon_location/'+target)
    result_recon = recon_location.postApi()
    result_recon = json.loads(result_recon)
    items_locations.clear()
    items_pushpins.clear()

    for key, val in result_recon.items():
        if key =='locations':
            for i in range(len(val)):
                latitude = val[i]["latitude"]
                longitude = val[i]["longitude"]
                street_address = val[i]["street_address"]
                items_locations.append(Item_locations(target, latitude, longitude, street_address))
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
                items_pushpins.append(Item_pushpins(target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
                pushpins_store(target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time, "recon-ng")



def request_recon_profile(target, port):
    #recon_profile
    recon_profile = RequestApi(str(port)+'/recon_profile/'+target)
    result_recon = recon_profile.postApi()
    result_recon = json.loads(result_recon)
    items_contacts.clear()
    items_profiles.clear()
    items_repositories.clear()

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
                items_contacts.append(Item_contacts(target, first_name, middle_name, last_name, email, title, region, country))
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")

        if key =='profiles':
            for i in range(len(val)):
                username = val[i]["username"]
                resource = val[i]["resource"]
                url = val[i]["url"]
                category = val[i]["category"]
                note = val[i]["notes"]
                items_profiles.append(Item_profiles(target, username, resource, url, category, note))
                profiles_store(target, username, resource, url, category, note, "recon-ng")

        if key =='repositories':
            for i in range(len(val)):
                name = val[i]["name"]
                owner = val[i]["owner"]
                description = val[i]["description"]
                resource = val[i]["resource"]
                category = val[i]["category"]
                url = val[i]["url"]
                items_repositories.append(Item_repositories(target, name, owner, description, resource, category, url))
                repositories_store(target, name, owner, description, resource, category, url, "recon-ng")


def request_recon_domain(target, port):
    #recon_domain
    recon_domain = RequestApi(str(port)+'/recon_domain/'+target)
    result_recon = recon_domain.postApi()
    result_recon = json.loads(result_recon)
    items_hosts.clear()
    items_companies.clear()
    items_contacts.clear()
    items_credentials.clear()
    items_vulnerabilities.clear()
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
                items_hosts.append(Item_hosts(target, host, ip_address, type_, region, country, latitude, longitude))
                hosts_store(target, host, ip_address, type_, region, country, latitude, longitude, "recon-ng")

        if key =='companies':
            for i in range(len(val)):
                company = val[i]["company"]
                description = val[i]["description"]
                items_companies.append(Item_companies(target, company, description))
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
                items_contacts.append(Item_contacts(target, first_name, middle_name, last_name, email, title, region, country))
                contacts_store(target, first_name, middle_name, last_name, email, title, region, country, "recon-ng")
        if key =='credentials':
            for i in range(len(val)):
                username = val[i]["username"]
                password = val[i]["password"]
                hash_ = val[i]["hash"]
                type_ = val[i]["type"]
                leak = val[i]["leak"]
                items_credentials.append(Item_credentials(target, username, password, hash_, type_, leak))
                credentials_store(target, username, password, hash_, type_, leak, "recon-ng")
       
        if key =='vulnerabilities':
            for i in range(len(val)):
                reference = val[i]["reference"]
                example = val[i]["example"]
                publish_date = val[i]["publish_date"]
                category = val[i]["category"]
                status = val[i]["status"]
                items_vulnerabilities.append(Item_vulnerabilities(target, reference, example, publish_date, category, status))
                vulnerabilities_store(target, reference, example, publish_date, category, status, "recon-ng")



def request_darksearch(target, n, port):
    darks = RequestApi(str(port)+"/darksearch/"+target+"/"+str(n))
    result_darks = darks.postApi()
    print(result_darks)
    result_darks = json.loads(result_darks)
    data = result_darks["data"]
    items_darksearch.clear()
    for i in range(len(data)):
        title = data[i]["title"]
        link = data[i]["link"]
        description = data[i]["description"]
        items_darksearch.append(Item_darksearch(target, title, link, description))
        darksearch_store(target, title, link, description, "darksearch")


def request_torBot(target, port):
    torBot_ = RequestApi(str(port)+"/torBot/"+target)
    result_torBot = torBot_.postApi()
    result_torBot = json.loads(result_torBot)
    data = result_torBot["result"]
    emails = result_torBot["email"]["emails"]
    items_darksearch.clear()
    items_contacts.clear()
    for i in range(len(emails)):
        items_contacts.append(Item_contacts(target, "", "", "", emails[i], "", "", ""))
        contacts_store(target, "", "", "", emails[i], "", "", "", "torBot")

    for i in range(len(data)):
        title = data[i]["title"]
        link = data[i]["link"]
        if link != "":
            items_darksearch.append(Item_darksearch(target, title, link, ""))
            darksearch_store(target, title, link, "", "torBot")



def request_dnstwist(target, port):
    dnstwist = RequestApi(str(port)+"/dnstwist/"+target)
    result_dnstwist = dnstwist.postApi()
    result_dnstwist = dnstwist.getApi()
    result_dnstwist = json.loads(result_dnstwist)
    print(result_dnstwist)

def request_infoga(target, port):
    infoga = RequestApi(str(port)+"/infoga/"+target)
    result_infoga = infoga.postApi()
    result_infoga = infoga.getApi()
    result_infoga = json.loads(result_infoga)
    print(result_infoga)

def request_linkedInt(target, bycompany, domain_surfix, prefix_email, port):
    linkedInt = RequestApi(str(port)+"/linkedInt/"+target+"/"+bycompany+"/"+domain_surfix+"/"+prefix_email)
    result_linkedInt = linkedInt.postApi()
    result_linkedInt = linkedInt.getApi()
    result_linkedInt = json.loads(result_linkedInt)
    print(result_linkedInt)


def request_photon(target, level_, port):
    photon = RequestApi(str(port)+"/photon/"+target+"/"+level_)
    result_photon = photon.postApi()
    result_photon = photon.getApi()
    result_photon = json.loads(result_photon)
    print(result_photon)


def request_sherlock(target, port):
    sherlock = RequestApi(str(port)+"/sherlock/"+target)
    result_sherlock = sherlock.postApi()
    result_sherlock = sherlock.getApi()
    result_sherlock = json.loads(result_sherlock)
    print(result_sherlock)


def request_sublist3r(target, ports_, port):
    sublist3r = RequestApi(str(port)+"/sublist3r/"+target+"/"+ports_)
    result_sublist3r = sublist3r.postApi()
    result_sublist3r = sublist3r.getApi()
    result_sublist3r = json.loads(result_sublist3r)
    print(result_sublist3r) 

def request_twint_tweet(target, search, port):
    twint_tweet = RequestApi(str(port)+"/twint_tweet/"+target+"/"+search)
    result_twint_tweet = twint_tweet.postApi()
    result_twint_tweet = twint_tweet.getApi()
    result_twint_tweet = json.loads(result_twint_tweet)
    print(result_twint_tweet)


def request_twint_relation(target, port):
    twint_relation = RequestApi(str(port)+"/twint_relation/"+target)
    result_twint_relation = twint_relation.postApi()
    result_twint_relation = twint_relation.getApi()
    result_twint_relation = json.loads(result_twint_relation)
    print(result_twint_relation)



def request_datasploit(target, port):
    #request to dataSploit
    dataSploit = RequestApi(str(port)+'/datasploit/'+target)
    result_datasploit = dataSploit.postApi()
    result_datasploit = dataSploit.getApi()
    result_datasploit = result_datasploit.decode("utf-8")
    result_datasploit = json.loads(result_datasploit)  
    data = result_datasploit["data"]
    items_domains.clear()
    items_repositories.clear()
    items_ips.clear()
    items_emails.clear()
    items_profiles.clear()

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
        items_domains.append(Item_domains(result_datasploit["target"], technologie, address, city, country, registar, other_info, dns_record))
        domains_store(result_datasploit["target"], technologie, address, city, country, registar, other_info, dns_record, "datasploit")

        for i in range(len(domain_github[1])):
            acount_git = domain_github[1][i]
            name = acount_git["repository"]["owner"]["login"]
            resource = "Github"
            category = "repo"
            url = acount_git["repository"]["owner"]["url"]
            tool = "datasploit"
            items_repositories.append(Item_repositories(result_datasploit["target"], name, "", "", resource, category, url))
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
        items_ips.append(Item_ips(result_datasploit["target"], ip_whois, ip_shodan, ip_virustotal))
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
        items_emails.append(Item_emails(result_datasploit["target"], email_fullcontact, email_pastes, email_clearbit, email_haveibeenpwned))
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
                        items_profiles.append(Item_profiles(username, username, resource, url, category, ""))
                        profiles_store(username, username, resource, url, category, "", tool)

        



'''results_ = {}
@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        print("-------------ggggggggggggggggggggggget")
        return render_template('search_osint.html')
    else:
        result = request.form
        print("---------------------------------------------------------------------")        
        tool_tab = result.getlist("tools")
        search = result["search"]
        print(tool_tab)
        print(search)
        tab_result = []
        results_.clear()
        

        for i in range(len(tool_tab)):
            if tool_tab[i] == 'automater':
                tab_result.clear()
                request_automater(search, 5001)
                tab_result.append(ItemTable_vulnerabilities(items_vulnerabilities))
                results_['automater'] = tab_result

            if tool_tab[i] == 'datasploit':
                tab_result.clear()
                request_datasploit(search, 5002)

                
                tab_result.append(ItemTable_domains(items_domains))
                tab_result.append(ItemTable_repositories(items_repositories))
                tab_result.append(ItemTable_ips(items_ips))
                tab_result.append(ItemTable_profiles(items_profiles))
                results_['datasploit'] = tab_result
                
            
            if tool_tab[i] == 'dnsRecon':
                tab_result.clear()
                request_dnsrecon(search, 5003)
                tab_result.append(ItemTable_hosts(items_hosts))
                results_['dnsRecon'] = tab_result

            if tool_tab[i] == 'theHarvester':
                tab_result.clear()
                request_theHarvester(search, 5004)

                tab_result.append(ItemTable_contacts(items_contacts))
                tab_result.append(ItemTable_hosts(items_hosts))
                results_['theHarvester'] = tab_result
            
            if tool_tab[i] == 'recon-ng':
                if re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", search):
                    request_recon_domain(search, 5005)




        items = [Item_vulnerabilities('Name1', 'Description1',"example", "publish_date", "category", "status"),
        Item_vulnerabilities('Name2', 'Description2',"example", "publish_date", "category", "status")]
        table = ItemTable_vulnerabilities(items)
        
        #for i in range(len(tool_tab)):

        print(table.__html__())
        result1 = table
        result2 = "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"

        print(results_)
        for key, val in results_.items():
            for i in range(len(val)):

                print(val[i].__html__())
        
        return render_template('search_osint.html', results_ = results_)
        





if __name__ == '__main__':
   app.run(debug = True)'''







if __name__ == '__main__':
    
    '''#request to torBot
    torBotApi = RequestApi('torBot/torlinkbgs6aabns.onion')
    torBotApi.postApi()

    request_torBot("torlinkbgs6aabns.onion")'''
    #request_twint_tweet("AdrienTchounkeu", "osint", 5014)
    request_dnstwist("antic.cm", 5010)







