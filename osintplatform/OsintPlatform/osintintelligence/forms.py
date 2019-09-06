from django import forms

class TheHarvesterForm(forms.Form):
    FAVORITE_COLORS_CHOICES = [
        ('all', 'all'),
        ('baidu', 'baidu'),
        ('bing', 'bing'),
        ('bingapi', 'bingapi'),
        ('censys', 'censys'),
        ('crtsh', 'crtsh'),
        ('cymon', 'cymon'),
        ('dnsdumpster', 'dnsdumpster'),
        ('dogpile', 'dogpile'),
        ('duckduckgo', 'duckduckgo'),
        ('google', 'google'),
        ('google-certificates', 'google-certificates'),
        ('hunter', 'hunter'),
        ('intelx', 'intelx'),
        ('linkedin', 'linkedin'),
        ('netcraft', 'netcraft'),
        ('securityTrails', 'securityTrails'),
        ('threatcrowd', 'threatcrowd'),
        ('trello', 'trello'),
        ('twitter', 'twitter'),
        ('vhost', 'vhost'),
        ('virustotal', 'virustotal'),
        ('yahoo', 'yahoo'),
        
    ]

    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))


    engine = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=FAVORITE_COLORS_CHOICES,
    )

class LinkedIntForm(forms.Form):
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    bycompany = forms.BooleanField(label='By Company', help_text="Effectuer la recherche suivant la compagnie.", required=False)
    domain_surfix = forms.CharField(label='Domain Surfix', widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    FORMAT_EMAIL = [
        ('full','full'),
        ('firstlast','firstlast'), 
        ('firstmlast','firstmlast'),
        ('flast','flast'), 
        ('firstl','firstl'),
        ('first','first'), 
        ('first.last','first.last'),
        ('fmlast','fmlast'),
        ('lastfirst','lastfirst'),
    ]
    format_email = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'data-live-search':'true', 'width': '70px'}),
        choices=FORMAT_EMAIL,
    )

class TwintForm(forms.Form):
    FONCTION = [
        ('tweet','tweet'),
        ('followers','followers'), 
    ]
    choose = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'id':'function-twint', 'data-live-search':'true', 'width': '70px', 'onchange':"change()", 'style': 'margin:auto;'}),
        choices=FONCTION,
        
    )
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    #all_tweet = forms.BooleanField(label='Tout les Tweet', help_text="Effectuer la recherche suivant la compagnie.", required=False)
    #followers = forms.BooleanField(label='Rechercher les Followers', help_text="Effectuer la recherche suivant la compagnie.", required=False)
    search = forms.CharField(label ='Mot clé', required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'id':'search-twint', 'display':'flex', 'width': '50%', 'name':'engine'}))


class TargetForm(forms.Form):
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))

class PhotonForm(forms.Form):
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    level_ = forms.CharField(label='Level to crawl', widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))

class Sublist3rForm(forms.Form):
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    ports = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))


class Recon_domainForm(forms.Form):
    MODULE = [
        ('recon/domains-hosts/bing_domain_web','recon/domains-hosts/bing_domain_web'),
        ('recon/domains-companies/pen','recon/domains-companies/pen'), 
        ('recon/domains-contacts/pen','recon/domains-contacts/pen'),
        ('recon/domains-contacts/pgp_search','recon/domains-contacts/pgp_search'), 
        ('recon/domains-contacts/whois_pocs','recon/domains-contacts/whois_pocs'),
        ('recon/domains-credentials/pwnedlist/api_usage','recon/domains-credentials/pwnedlist/api_usage'), 
        ('recon/domains-credentials/pwnedlist/domain_ispwned','recon/domains-credentials/pwnedlist/domain_ispwned'),
        ('recon/domains-domains/brute_suffix','recon/domains-domains/brute_suffix'),
        ('recon/domains-hosts/brute_hosts','recon/domains-hosts/brute_hosts'),
        ('recon/domains-hosts/builtwith','recon/domains-hosts/builtwith'),
        ('recon/domains-hosts/certificate_transparency','recon/domains-hosts/certificate_transparency'),
        ('recon/domains-hosts/findsubdomains','recon/domains-hosts/findsubdomains'), 
        ('recon/domains-hosts/hackertarget','recon/domains-hosts/hackertarget'),
        ('recon/domains-hosts/mx_spf_ip','recon/domains-hosts/mx_spf_ip'),
        ('recon/domains-hosts/netcraft','recon/domains-hosts/netcraft'),
        ('recon/domains-hosts/shodan_hostname','recon/domains-hosts/shodan_hostname'),
        ('recon/domains-hosts/ssl_san','recon/domains-hosts/ssl_san'),
        ('recon/domains-hosts/threatcrowd','recon/domains-hosts/threatcrowd'),
        ('recon/domains-hosts/threatminer','recon/domains-hosts/threatminer'),
    ]
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    module = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=MODULE,
    )

class Recon_companyForm(forms.Form):
    MODULE = [
        ('recon/companies-contacts/bing_linkedin_cache','recon/companies-contacts/bing_linkedin_cache'),
        ('recon/companies-contacts/jigsaw/point_usage','recon/companies-contacts/jigsaw/point_usage'), 
        ('recon/companies-contacts/jigsaw/purchase_contact','recon/companies-contacts/jigsaw/purchase_contact'),
        ('recon/companies-contacts/jigsaw/search_contacts','recon/companies-contacts/jigsaw/search_contacts'), 
        ('recon/companies-contacts/pen','recon/companies-contacts/pen'),
        ('recon/companies-domains/pen','recon/companies-domains/pen'), 
        ('recon/companies-multi/github_miner','recon/companies-multi/github_miner'),
        ('recon/companies-multi/whois_miner','recon/companies-multi/whois_miner'),

    ]
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    module = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=MODULE,
    )

class Recon_contactForm(forms.Form):
    MODULE = [
        ('recon/contacts-contacts/mailtester','recon/contacts-contacts/mailtester'),
        ('recon/contacts-contacts/mangle','recon/contacts-contacts/mangle'), 
        ('recon/contacts-contacts/unmangle','recon/contacts-contacts/unmangle'),
        ('recon/contacts-credentials/hibp_breach','recon/contacts-credentials/hibp_breach'), 
        ('recon/contacts-domains/migrate_contacts','recon/contacts-domains/migrate_contacts'),
        ('recon/contacts-profiles/fullcontact','recon/contacts-profiles/fullcontact'), 
    ]
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    module = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=MODULE,
    )


class Recon_hostForm(forms.Form):
    MODULE = [
        ('recon/hosts-domains/migrate_hosts','recon/hosts-domains/migrate_hosts'),
        ('recon/hosts-hosts/ipinfodb','recon/hosts-hosts/ipinfodb'), 
        ('recon/hosts-hosts/ipstack','recon/hosts-hosts/ipstack'),
        ('recon/hosts-hosts/resolve','recon/hosts-hosts/resolve'), 
        ('recon/hosts-hosts/reverse_resolve','recon/hosts-hosts/reverse_resolve'),
        ('recon/hosts-hosts/ssltools','recon/hosts-hosts/ssltools'),
        ('recon/hosts-hosts/virustotal','recon/hosts-hosts/virustotal'),
        ('recon/hosts-locations/migrate_hosts','recon/hosts-locations/migrate_hosts'), 
        ('recon/hosts-ports/shodan_ip','recon/hosts-ports/shodan_ip'),   
    ]
    host = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    ip_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    latitude = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    longitude = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    module = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=MODULE,
    )

class Recon_profileForm(forms.Form):
    MODULE = [
        ('recon/profiles-contacts/dev_diver','recon/profiles-contacts/dev_diver'),
        ('recon/profiles-contacts/github_users','recon/profiles-contacts/github_users'), 
        ('recon/profiles-profiles/namechk','recon/profiles-profiles/namechk'),
        ('recon/profiles-profiles/profiler','recon/profiles-profiles/profiler'), 
        ('recon/profiles-profiles/twitter_mentioned','recon/profiles-profiles/twitter_mentioned'),
        ('recon/profiles-profiles/twitter_mentions','recon/profiles-profiles/twitter_mentions'),
        ('recon/profiles-repositories/github_repos','recon/profiles-repositories/github_repos'),  
    ]
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    resource = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    category = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    module = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=MODULE,
    )

class Recon_locationForm(forms.Form):
    MODULE = [
        ('recon/locations-locations/reverse_geocode','recon/locations-locations/reverse_geocode'),
        ('recon/locations-pushpins/flickr','recon/locations-pushpins/flickr'), 
        ('recon/locations-pushpins/shodan','recon/locations-pushpins/shodan'),
        ('recon/locations-pushpins/twitter','recon/locations-pushpins/twitter'), 
        ('recon/locations-pushpins/youtube','recon/locations-pushpins/youtube'), 
    ]
    latitude = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    longitude = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '50%', 'name':'engine'}))
    
    module = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '200px'}),
        choices=MODULE,
    )


class searchForm(forms.Form):
    ENTITE = [
        ('Companies','Companies'),
        ('Contact','Contact'), 
        ('Credentials','Credentials'),
        ('Darksearch','Darksearch'), 
        ('Emails','Emails'),
        ('Hosts','Hosts'), 
        ('Domains','Domains'),
        ('Locations','Locations'),
        ('Profiles','Profiles'),
        ('Ips','Ips'),
        ('Ports','Ports'),
        ('Pushpins','Pushpins'), 
        ('Repositories','Repositories'),
        ('Vulnerabilities','Vulnerabilities'),
    ]

    entite = forms.ChoiceField(
        widget=forms.Select(attrs={'class' : 'selectpicker form-search', 'multiple':'true', 'data-live-search':'true', 'width': '70px'}),
        choices=ENTITE,
    )
    noeud = forms.BooleanField(help_text="Cochez si vous souhaitez effectuer une recherche sur les noeuds de l'entité.", required=False)
    target = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-search', 'display':'flex', 'width': '30%', 'name':'engine'}))