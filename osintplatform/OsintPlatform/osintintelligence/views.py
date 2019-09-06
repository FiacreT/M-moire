from django.shortcuts import render
from django.http import HttpResponse
import requests
import psycopg2
import ast
import json
import re
from .forms import searchForm, TargetForm, TheHarvesterForm, Sublist3rForm, LinkedIntForm, TwintForm, PhotonForm, Recon_domainForm, Recon_companyForm, Recon_contactForm, Recon_hostForm, Recon_profileForm, Recon_locationForm      
from osintintelligence.models import Locations, Hosts, Ips, Ports, Domains, Emails, Contacts, Profiles, Companies, Credentials, Pushpins, Repositories, Vulnerabilities
from osintintelligence.models import Companies, Contacts

# Create your views here.

result = {}

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


def request_sherlock(request):
    global result
    result.clear()
    form_sherlock = TargetForm(request.POST or None)
    result_sherlock = {}
    if form_sherlock.is_valid():
        target = form_sherlock.cleaned_data['target']
        port = 5009
        sherlock = RequestApi(str(port)+"/sherlock/"+target)
        result_sherlock = sherlock.postApi()
        result_sherlock = sherlock.getApi()
        result_sherlock = json.loads(result_sherlock)
        print(result_sherlock)

    else:
        form_sherlock = TargetForm()
    result = result_sherlock
    return render(request, 'osintintelligence/homePage.html', {'form_sherlock':form_sherlock, 'result':result})

def request_infoga(request):
    global result
    result.clear()
    form_infoga = TargetForm(request.POST or None)
    result_infoga = {}
    if form_infoga.is_valid():
        target = form_infoga.cleaned_data['target']
        port = 5008
        infoga = RequestApi(str(port)+"/infoga/"+target)
        result_infoga = infoga.postApi()
        result_infoga = infoga.getApi()
        result_infoga = json.loads(result_infoga)
        print(result_infoga)
    else:
        form_infoga = TargetForm()
    result = result_infoga
    return render(request, 'osintintelligence/homePage.html', {'form_infoga':form_infoga, 'result':result})


def request_dnsrecon(request):
    global result
    result.clear()
    form_dnsrecon = TargetForm(request.POST or None)
    result_dnsrecon = {}
    if form_dnsrecon.is_valid():
        target = form_dnsrecon.cleaned_data['target']
        port = 5003
        dnsrecon = RequestApi(str(port)+'/dnsrecon/'+target)
        result_dnsrecon = dnsrecon.postApi()
        result_dnsrecon = dnsrecon.getApi()
        #result_dnsrecon = result_dnsrecon.decode("utf-8")
        result_dnsrecon = json.loads(result_dnsrecon)  
        data = result_dnsrecon["data"]
        host = []
        target_ = []
        ip_address = []
        type_ = []
        #items_hosts.clear()
        for i in range(len(data)):
            for key, val in data[i].items():
                if key == "name":
                    host.append(val) 
                if key == "target":
                    target_.append(val)
                if key == "address":
                    ip_address.append(val)
                if key == "type":
                    type_.append(val)
        #items_hosts.append(Item_hosts(result_dnsrecon["target"], host, ip_address, type_, "", "", "", "")) 
        #hosts_store(result_dnsrecon["target"], host, ip_address, type_, "", "", "", "", "dnsrecon")
        result_dnsrecon = {"Host": host, "target": target_, "IP Address": ip_address, "Type": type_}
    else:
        form_dnsrecon = TargetForm()
    result = result_dnsrecon
    return render(request, 'osintintelligence/homePage.html', {'form_dnsrecon':form_dnsrecon, 'result':result})
    
    
def request_sublist3r(request):
    result = {}
    form_sublist3r = Sublist3rForm(request.POST or None)
    result_sublist3r = {}
    if form_sublist3r.is_valid():
        target = form_sublist3r.cleaned_data['target']
        port = 5007
        sublist3r = RequestApi(str(port)+"/sublist3r/"+target)
        result_sublist3r = sublist3r.postApi()
        result_sublist3r = sublist3r.getApi()
        result_sublist3r = json.loads(result_sublist3r)
        print(result_sublist3r) 
    else:
        form_sublist3r = Sublist3rForm()
    result = result_sublist3r
    return render(request, 'osintintelligence/homePage.html', {'form_sublist3r':form_sublist3r, 'result':result})

def request_dnstwist(request):
    results = {}
    form_dnstwist = TargetForm(request.POST or None)
    result_dnstwist = {}
    if form_dnstwist.is_valid():
        target = form_dnstwist.cleaned_data['target']
        port = 5010
        dnstwist = RequestApi(str(port)+"/dnstwist/"+target)
        result_dnstwist = dnstwist.postApi()
        result_dnstwist = dnstwist.getApi()
        result_dnstwist = json.loads(result_dnstwist)
        print(result_dnstwist)
    else:
        form_dnstwist = TargetForm()
    results = result_dnstwist
    return render(request, 'osintintelligence/homePage.html', {'form_dnstwist':form_dnstwist, 'results':results})
    

def request_linkedInt(request):
    result = {}
    form_linkedInt = LinkedIntForm(request.POST or None)
    result_linkedInt = {}
    if form_linkedInt.is_valid():
        port = 5012
        target = form_linkedInt.cleaned_data['target']
        bycompany = form_linkedInt.cleaned_data['bycompany']
        company = ''
        if bycompany:
            company = 'y'
        else:
            company = 'n'
        domain_surfix = form_linkedInt.cleaned_data['domain_surfix']
        format_email = form_linkedInt.cleaned_data['format_email']
        linkedInt = RequestApi(str(port)+"/linkedInt/"+target+"/"+company+"/"+domain_surfix+"/"+format_email)
        result_linkedInt = linkedInt.postApi()
        result_linkedInt = linkedInt.getApi()
        result_linkedInt = json.loads(result_linkedInt)
        print(result_linkedInt)
    else:
        form_linkedInt = LinkedIntForm()
    result = result_linkedInt
    return render(request, 'osintintelligence/homePage.html', {'form_linkedInt':form_linkedInt, 'result_linkedInt':result_linkedInt})


def request_twint(request):
    form_twint = TwintForm(request.POST or None, initial={'choose': 'tweet'})
    result_tweet = {}
    result = {}
    print("*************************************************")
    if form_twint.is_valid():
        port = 5014
        choose = form_twint.cleaned_data['choose']
        username = form_twint.cleaned_data['username']
        print(choose)
        
        if choose == "tweet":
            print(choose)
            search = form_twint.cleaned_data['search']
            twint_tweet = RequestApi(str(port)+"/twint_tweet/"+username+"/"+search)
            result_twint_tweet = twint_tweet.postApi()
            result_twint_tweet = twint_tweet.getApi()
            result_twint_tweet = json.loads(result_twint_tweet)
            print(result_twint_tweet)
            result_tweet = result_twint_tweet
        if choose == "followers":
            print(choose)
            print("******************* FOLLOWERS ******************************")
            twint_relation = RequestApi(str(port)+"/twint_relation/"+username)
            result_twint_relation = twint_relation.postApi()
            result_twint_relation = twint_relation.getApi()
            result_twint_relation = json.loads(result_twint_relation)
            print(result_twint_relation)
            result_tweet = result_twint_relation
    else:
        form_twint = TwintForm(initial={'choose': 'tweet'})
    result = result_tweet
    return render(request, 'osintintelligence/homePage.html', {'form_twint':form_twint, 'result_tweet':result_tweet})

def request_photon(request):
    form_photon = PhotonForm(request.POST or None)
    result_photon = {}
    result = {}
    if form_photon.is_valid():
        port = 5013
        target = form_photon.cleaned_data['target']
        level_ = form_photon.cleaned_data['level_']
        photon = RequestApi(str(port)+"/photon/"+target+"/"+level_)
        result_photon = photon.postApi()
        result_photon = photon.getApi()
        result_photon = json.loads(result_photon)
        print(result_photon)
    else:
        form_photon = PhotonForm()
    result = result_photon
    return render(request, 'osintintelligence/homePage.html', {'form_photon':form_photon, 'result':result})


def request_darksearch(request):
    form_darksearch = PhotonForm(request.POST or None)
    result_darks = {}
    result = {}
    data = []
    if form_darksearch.is_valid():
        port = 5015
        target = form_darksearch.cleaned_data['target']
        level_ = form_darksearch.cleaned_data['level_']
        
        darks = RequestApi(str(port)+"/darksearch/"+target+"/"+level_)
        result_darks = darks.postApi()
        print(result_darks)
        result_darks = json.loads(result_darks)
        data = result_darks["data"]
        '''items_darksearch.clear()
        for i in range(len(data)):
            title = data[i]["title"]
            link = data[i]["link"]
            description = data[i]["description"]
            items_darksearch.append(Item_darksearch(target, title, link, description))
            darksearch_store(target, title, link, description, "darksearch")'''
    else:
        form_darksearch = PhotonForm()
    #results = data
    return render(request, 'osintintelligence/homePage.html', {'form_darksearch':form_darksearch, 'data':data})


def request_torBot(request):
    form_torBot = TargetForm(request.POST or None)
    result_torBot = {}
    result = {}
    if form_torBot.is_valid():
        port = 5016
        target = form_torBot.cleaned_data['target']
        torBot_ = RequestApi(str(port)+"/torBot/"+target)
        result_torBot = torBot_.postApi()
        result_torBot = json.loads(result_torBot)
        data = result_torBot["result"]
        emails = result_torBot["email"]["emails"]
        '''items_darksearch.clear()
        items_contacts.clear()
        for i in range(len(emails)):
            items_contacts.append(Item_contacts(target, "", "", "", emails[i], "", "", ""))
            contacts_store(target, "", "", "", emails[i], "", "", "", "torBot")

        for i in range(len(data)):
            title = data[i]["title"]
            link = data[i]["link"]
            if link != "":
                items_darksearch.append(Item_darksearch(target, title, link, ""))
                darksearch_store(target, title, link, "", "torBot")'''
    else:
        form_torBot = TargetForm()
    result = result_torBot
    return render(request, 'osintintelligence/homePage.html', {'form_torBot':form_torBot, 'result':result})


def request_shodan(request):
    form_shodan = TargetForm(request.POST or None)
    result_shodan = {}
    data = []
    result = {}
    if form_shodan.is_valid():
        port = 5017
        target = form_shodan.cleaned_data['target']
        shodan_ = RequestApi(str(port)+"/shodan/"+target)
        result_shodan = shodan_.postApi()
        result_shodan = json.loads(result_shodan)
        data = result_shodan['data']
    else:
        form_shodan = TargetForm()
    
    '''print("*************************************")
    print(data)
    print(type(data))'''
    return render(request, 'osintintelligence/homePage.html', {'form_shodan':form_shodan, 'data':data})


def request_recon_location(request):
    form_recon_location = Recon_locationForm(request.POST or None)
    result_recon = {}
    result = {}
    if form_recon_location.is_valid():
        port = 5002
        latitude = form_recon_location.cleaned_data['latitude']
        longitude = form_recon_location.cleaned_data['longitude']
        target = latitude+"*"+longitude
        module = request.POST.getlist('module')
        modules = '**'.join(module)
        modules = modules.replace("/", ".")

        recon_location = RequestApi(str(port)+'/recon_location/'+target+"/"+modules)
        result_recon = recon_location.postApi()
        result_recon = json.loads(result_recon)
        
        '''items_locations.clear()
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
                    pushpins_store(target, source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time, "recon-ng")'''
    else:
        form_recon_location = Recon_locationForm()
    result = result_recon
    return render(request, 'osintintelligence/homePage.html', {'form_recon_location':form_recon_location, 'result':result})

def request_recon_profile(request):
    form_recon_profile = Recon_profileForm(request.POST or None)
    result_recon = {}
    result = {}
    if form_recon_profile.is_valid():
        port = 5002
        username = form_recon_profile.cleaned_data['username']
        resource = form_recon_profile.cleaned_data['resource']
        url = form_recon_profile.cleaned_data['url']
        category = form_recon_profile.cleaned_data['category']
        target = username+"*"+resource+"*"+url+"*"+category
        module = request.POST.getlist('module')
        modules = '**'.join(module)
        modules = modules.replace("/", ".")
        recon_profile = RequestApi(str(port)+'/recon_profile/'+target+"/"+modules)
        result_recon = recon_profile.postApi()
        result_recon = json.loads(result_recon)

        '''items_contacts.clear()
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
                    repositories_store(target, name, owner, description, resource, category, url, "recon-ng")'''
    else:
        form_recon_profile = Recon_profileForm()
    result = result_recon
    return render(request, 'osintintelligence/homePage.html', {'form_recon_profile':form_recon_profile, 'result':result})


def request_recon_host(request):
    form_recon_host = Recon_hostForm(request.POST or None)
    result_recon = {}
    result = {}
    if form_recon_host.is_valid():
        port = 5002
        host = form_recon_host.cleaned_data['host']
        ip_address = form_recon_host.cleaned_data['ip_address']
        latitude = form_recon_host.cleaned_data['latitude']
        longitude = form_recon_host.cleaned_data['longitude']
        target = host+"*"+ip_address+"*"+latitude+"*"+longitude
        module = request.POST.getlist('module')
        modules = '**'.join(module)
        modules = modules.replace("/", ".")
        recon_host = RequestApi(str(port)+'/recon_host/'+target+"/"+modules)
        result_recon = recon_host.postApi()
        result_recon = json.loads(result_recon)
        '''items_hosts.clear()
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
                    ports_store(target, ip_address, host, port, protocol, "recon-ng")'''
    else:
        form_recon_host = Recon_hostForm()
    result = result_recon
    return render(request, 'osintintelligence/homePage.html', {'form_recon_host':form_recon_host, 'result':result})

def request_recon_contact(request):
    form_recon_contact = Recon_contactForm(request.POST or None)
    result_recon = {}
    result = {}
    if form_recon_contact.is_valid():
        port = 5002
        first_name = form_recon_contact.cleaned_data['first_name']
        last_name = form_recon_contact.cleaned_data['last_name']
        email = form_recon_contact.cleaned_data['email']
        title = form_recon_contact.cleaned_data['title']
        country = form_recon_contact.cleaned_data['country']
        target = first_name+"*"+last_name+"*"+email+"*"+title+"*"+country
        module = request.POST.getlist('module')
        modules = '**'.join(module)
        modules = modules.replace("/", ".")
        recon_contact = RequestApi(str(port)+'/recon_contact/'+target+"/"+modules)
        result_recon = recon_contact.postApi()
        result_recon = json.loads(result_recon)

        '''items_contacts.clear()
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
                    profiles_store(target, username, resource, url, category, note, "recon-ng")'''
    else:
        form_recon_contact = Recon_contactForm()
    result = result_recon
    return render(request, 'osintintelligence/homePage.html', {'form_recon_contact':form_recon_contact, 'result':result})

def request_recon_company(request):
    form_recon_company = Recon_companyForm(request.POST or None)
    result_recon = {}
    result = {}
    if form_recon_company.is_valid():
        port = 5002
        target = form_recon_company.cleaned_data['target']
        module = request.POST.getlist('module')
        modules = '**'.join(module)
        modules = modules.replace("/", ".")
        recon_company = RequestApi(str(port)+'/recon_company/'+target+"/"+modules)
        result_recon = recon_company.postApi()
        result_recon = json.loads(result_recon)
        '''items_contacts.clear()
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
                    profiles_store(target, username, resource, url, category, note, "recon-ng")'''
    else:
        form_recon_company = Recon_companyForm()
    result = result_recon
    return render(request, 'osintintelligence/homePage.html', {'form_recon_company':form_recon_company, 'result':result})



def request_recon_domain(request):
    form_recon_domain = Recon_domainForm(request.POST or None)
    result_recon = {}
    result = {}
    if form_recon_domain.is_valid():
        port = 5002
        target = form_recon_domain.cleaned_data['target']
        module = request.POST.getlist('module')
        modules = '**'.join(module)
        modules = modules.replace("/", ".")
        #recon_domain
        recon_domain = RequestApi(str(port)+'/recon_domain/'+target+"/"+modules)
        result_recon = recon_domain.postApi()
        result_recon = json.loads(result_recon)
        '''items_hosts.clear()
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
                    vulnerabilities_store(target, reference, example, publish_date, category, status, "recon-ng")'''
    else:
        form_recon_domain = Recon_domainForm()
    result = result_recon
    return render(request, 'osintintelligence/homePage.html', {'form_recon_domain':form_recon_domain, 'result':result})









def request_datasploit(request):
    form_datasploit = TargetForm(request.POST or None)
    result_datasploit = {}
    result = {}
    data = {}
    if form_datasploit.is_valid():
        port = 5002
        target = form_datasploit.cleaned_data['target']
        #request to dataSploit
        dataSploit = RequestApi(str(port)+'/datasploit/'+target)
        result_datasploit = dataSploit.postApi()
        result_datasploit = dataSploit.getApi()
        result_datasploit = result_datasploit.decode("utf-8")
        result_datasploit = json.loads(result_datasploit)  
        data = result_datasploit["data"]
        '''items_domains.clear()
        items_repositories.clear()
        items_ips.clear()
        items_emails.clear()
        items_profiles.clear()'''

        '''if re.match("^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", target):
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
                            profiles_store(username, username, resource, url, category, "", tool)'''
    else:
        form_datasploit = TargetForm()
    result = data
    return render(request, 'osintintelligence/homePage.html', {'form_datasploit':form_datasploit, 'result':result})




def request_automater(request):
    form_automater = TargetForm(request.POST or None)
    result_automater = {}
    result = {}
    if form_automater.is_valid():
        port = 5001
        target = form_automater.cleaned_data['target']
        automater = RequestApi(str(port)+'/automater/'+target)
        result_automater = automater.postApi()
        print(result_automater)
        result_automater = automater.getApi()
        result_automater = result_automater.decode("utf-8")
        result_automater = json.loads(result_automater)
        '''reference = ""
        status = ""
        target = result_automater["target"]
        #items_vulnerabilities.clear()

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
                vulnerabilities_store(target, reference, "", "", "", status, "automater")'''
    else:
        form_automater = TargetForm()
    result = result_automater
    return render(request, 'osintintelligence/homePage.html', {'form_automater':form_automater, 'result':result})


def request_theHarvester(request):
    #request to theHarvester  
    global result
    form_theHarvester = TheHarvesterForm(request.POST or None)
    result_harvester = {}
    result.clear()

    if form_theHarvester.is_valid(): 
        target = form_theHarvester.cleaned_data['target']
        engine = request.POST.getlist('engine')
        engines = ' '.join(engine)
        print(target)
        print(engine)
        port = 5004
        theHarvester = RequestApi(str(port)+'/theHarvester/'+target+'/'+engines)
    
        result_harvester = ast.literal_eval(theHarvester.postApi())
        result_harvester = json.loads(theHarvester.postApi())

        #Store emails
        for email in result_harvester["emails"]:
            contacts = Contacts(target=result_harvester["target"], email = email)
            contacts.save()
            #contacts_store(result_harvester["target"], '','', '', email,'','','','theHarvester')
        
        #Store hosts
        for host in result_harvester["host"]:
            hosts = Hosts(target=result_harvester["target"], host=host)
            hosts.save()
            #hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')

        for host in result_harvester["vhost"]:
            hosts = Hosts(target=result_harvester["target"], host=host)
            hosts.save()
            #hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')
        
        for host in result_harvester["shodan"]:
            hosts = Hosts(target=result_harvester["target"], host=host)
            hosts.save()
            #hosts_store(result_harvester["target"], host, '', '', '', '', '', '', 'theHarvester')

    else:
        form_theHarvester = TheHarvesterForm()
    result = result_harvester
    return render(request, 'osintintelligence/homePage.html', {'form_theHarvester':form_theHarvester, 'result':result})



def intelligence(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return render(request, 'osintintelligence/homePage.html', {})


def administration(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    tools = {'Sherlock':'actived',
            'Infoga':'actived', 
            'PhoneInfoga':'actived',
            'theHarvester':'actived', 
            'DnsRecon':'actived',
            'Sublist3r':'actived', 
            'Google Safe Browsing API':'actived',
            'DnsTwist':'actived',
            'Google Maps':'actived',
            'Face Recognition':'actived',
            'Twint':'actived',
            'Instalooter':'actived', 
            'LinkedInt':'actived',
            'Automater':'actived',
            'Recon-ng':'actived',
            'photon':'actived',
            'Datasploit':'actived',
            'darksearch':'actived',
            'torBot':'actived',
            'OnionScan':'actived'
            }
    return render(request, 'osintintelligence/administration.html', {'tools':tools})



def search(request):
    form = searchForm(request.POST or None)
    result_search = []

    if form.is_valid():
        target = form.cleaned_data['target']
        #engine = form.cleaned_data['engine']
        entite = form.cleaned_data['entite']

        result_search = Companies.nodes.get(target=target)
       


    else:
        form = searchForm()
    return render(request, 'osintintelligence/visualisation.html', {'form':form, 'result_search':result_search})




def connexion(request):
    return render(request, 'osintintelligence/connexion.html', {})



