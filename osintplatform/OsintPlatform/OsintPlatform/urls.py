"""OsintPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from osintintelligence import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('intelligence', views.intelligence),
    path('intelligence/form_theHarvester', views.request_theHarvester, name="request_theHarvester"),
    path('intelligence/form_sherlock', views.request_sherlock, name="request_sherlock"),
    path('intelligence/form_infoga', views.request_infoga, name="request_infoga"),
    path('intelligence/form_dnsrecon', views.request_dnsrecon, name="request_dnsrecon"),
    path('intelligence/form_sublist3r', views.request_sublist3r, name="request_sublist3r"),
    path('intelligence/form_dnstwist', views.request_dnstwist, name="request_dnstwist"),
    path('intelligence/form_linkedInt', views.request_linkedInt, name="request_linkedInt"),
    path('intelligence/form_twint', views.request_twint, name="request_twint"),
    path('intelligence/form_photon', views.request_photon, name="request_photon"),
    path('intelligence/form_automater', views.request_automater, name="request_automater"),
    path('intelligence/form_datasploit', views.request_datasploit, name="request_datasploit"),
    path('intelligence/form_recon_domain', views.request_recon_domain, name="request_recon_domain"),
    path('intelligence/form_recon_company', views.request_recon_company, name="request_recon_company"),
    path('intelligence/form_recon_contact', views.request_recon_contact, name="request_recon_contact"),
    path('intelligence/form_recon_host', views.request_recon_host, name="request_recon_host"),
    path('intelligence/form_recon_profile', views.request_recon_profile, name="request_recon_profile"),
    path('intelligence/form_recon_location', views.request_recon_location, name="request_recon_location"),
    path('intelligence/form_darksearch', views.request_darksearch, name="request_darksearch"),
    path('intelligence/form_torBot', views.request_torBot, name="request_torBot"),
    path('intelligence/form_shodan', views.request_shodan, name="request_shodan"),
    path('administration', views.administration),
    path('connexion', views.connexion),
    path('intelligence/visualisation', views.search, name="search")
]
