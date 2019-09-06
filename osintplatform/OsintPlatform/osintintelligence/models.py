from django.db import models
#from django.urls import reverse
from django.utils import timezone
from neomodel import config, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, StructuredNode, DateProperty, Relationship
from django_neomodel import DjangoNode
# Create your models here.

class Locations(StructuredNode):
    target = StringProperty(max_length=100)
    latitude = StringProperty(max_length=100)
    longitude = StringProperty(max_length=100)
    street_address = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.target

class Hosts(StructuredNode):
    target = StringProperty(max_length=100)
    host = StringProperty(max_length=100)
    ip_address = StringProperty(max_length=100)
    type_ = StringProperty(max_length=100)
    region = StringProperty(max_length=100)
    country = StringProperty(max_length=100)
    latitude = StringProperty(max_length=100)
    longitude = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.host

class Ips(StructuredNode):
    target = StringProperty(max_length=100)
    ip_whois = StringProperty(max_length=10000)
    ip_shodan = StringProperty(max_length=10000)
    ip_virustotal = StringProperty(max_length=10000)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.target

class Ports(StructuredNode):
    target = StringProperty(max_length=100)
    ip_address = StringProperty(max_length=100)
    host = StringProperty(max_length=100)
    port = StringProperty(max_length=100)
    protocol = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.port

class Domains(StructuredNode):
    target = StringProperty(max_length=100)
    technologie = StringProperty(max_length=10000)
    address = StringProperty(max_length=100)
    city = StringProperty(max_length=100)
    country = StringProperty(max_length=100)
    registrar = StringProperty(max_length=100)
    other_info = StringProperty(max_length=10000)
    dns_record = StringProperty(max_length=10000)
    tool = StringProperty(max_length=100)
    locations = RelationshipTo(Locations, 'localisation')
    hosts = RelationshipTo(Hosts,'posede')
    ips = RelationshipTo(Ips,'possede')
    ports = RelationshipTo(Ports,'possede')

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.target

class Emails(StructuredNode):
    target = StringProperty(max_length=100)
    email_fullcontact = StringProperty(max_length=10000)
    email_pastes = StringProperty(max_length=10000)
    email_clearbit = StringProperty(max_length=10000)
    email_haveibeenpwned = StringProperty(max_length=10000)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.target

class Contacts(StructuredNode):
    target = StringProperty(max_length=100)
    first_name = StringProperty(max_length=100)
    last_name = StringProperty(max_length=100)
    email = StringProperty(max_length=100)
    title = StringProperty(max_length=100)
    region = StringProperty(max_length=100)
    country = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)
    emails = RelationshipTo(Emails,'possede')
    locations = RelationshipTo(Locations,'habite')

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.email

class Profiles(StructuredNode):
    target = StringProperty(max_length=100)
    username = StringProperty(max_length=100)
    ressource = StringProperty(max_length=100)
    url = StringProperty(max_length=100)
    category = StringProperty(max_length=100)
    note = StringProperty(max_length=10000)
    tool = StringProperty(max_length=100)
    contacts = Relationship(Contacts,'possede')

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.username


class Companies(StructuredNode):
    target = StringProperty(max_length=100)
    company = StringProperty(max_length=100)
    description = StringProperty(max_length=10000)
    tool = StringProperty(max_length=100)
    contacts = Relationship(Contacts,'emploie')
    profiles = RelationshipTo(Profiles,'emploie')
    domains = RelationshipTo(Domains,'possede')

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.company

class Credentials(StructuredNode):
    target = StringProperty(max_length=100)
    username = StringProperty(max_length=100)
    password = StringProperty(max_length=100)
    hash_ = StringProperty(max_length=10000)
    type_ = StringProperty(max_length=100)
    leak = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.username

class Pushpins(StructuredNode):
    target = StringProperty(max_length=100)
    source = StringProperty(max_length=100)
    screen_name = StringProperty(max_length=100)
    profile_name = StringProperty(max_length=100)
    profile_url = StringProperty(max_length=100)
    media_url = StringProperty(max_length=100)
    thumb_url = StringProperty(max_length=100)
    message = StringProperty(max_length=10000)
    latitude = StringProperty(max_length=100)
    longitude = StringProperty(max_length=100)
    time = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.profile_name

class Repositories(StructuredNode):
    target = StringProperty(max_length=100)
    name = StringProperty(max_length=100)
    owner = StringProperty(max_length=100)
    description = StringProperty(max_length=100)
    ressource = StringProperty(max_length=100)
    category = StringProperty(max_length=100)
    url = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.name

class Vulnerabilities(StructuredNode):
    target = StringProperty(max_length=100)
    reference = StringProperty(max_length=100)
    example = StringProperty(max_length=100)
    publish_date = StringProperty(max_length=100)
    category = StringProperty(max_length=100)
    status = StringProperty(max_length=100)
    tool = StringProperty(max_length=100)

    def __str__(self):
        """ 
        Table pour stocker les Companies
        """
        return self.target

