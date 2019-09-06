
resultTemp = "\n____________________     Results found for: diablo3keygen.net     ____________________\nNo results found in the FNet URL\nNo results found in the Un Redirect\n[+] IP from URLVoid: No results found\n[+] Blacklist from URLVoid: No results found\n[+] Domain Age from URLVoid: No results found\n[+] Geo Coordinates from URLVoid: No results found\n[+] Country from URLVoid: No results found\n[+] pDNS data from VirusTotal: No results found\n[+] pDNS malicious URLs from VirusTotal: ('2019-04-26', 'hxxp://diablo3keygen.net/WinWord.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-04-26', 'hxxp://diablo3keygen.net/crvbox.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-04-11', 'hxxp://diablo3keygen.net/4512.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-04-07', 'hxxp://diablo3keygen.net/bit.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-04-07', 'hxxp://diablo3keygen.net/lol.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-04-01', 'hxxp://diablo3keygen.net/545.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-03-31', 'hxxp://diablo3keygen.net/harami.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-03-19', 'hxxp://diablo3keygen.net/potti.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-02-19', 'hxxp://diablo3keygen.net/\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2019-02-10', 'hxxp://diablo3keygen.net/tito.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2018-06-08', 'hxxp://diablo3keygen.net/fg_0d7cc44c.mod\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2018-06-01', 'hxxp://diablo3keygen.net/cgi-sys/suspendedpage.cgi\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2018-05-02', 'hxxp://diablo3keygen.net/crvbox.exe[\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2017-01-19', 'hxxp://diablo3keygen.net/redirect.php\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2016-09-14', 'hxxp://diablo3keygen.net/crvbox.exe[/\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2015-05-10', 'hxxp://diablo3keygen.net/idk.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2015-05-10', 'hxxp://diablo3keygen.net/fit.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2015-05-10', 'hxxp://diablo3keygen.net/8798.exe\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2014-02-28', 'hxxp://diablo3keygen.net/crvbox.exe%5B\\\\n    </a>\\\\n  </')\n[+] pDNS malicious URLs from VirusTotal: ('2014-02-19', 'hxxp://diablo3keygen.net/453.exe\\\\n    </a>\\\\n  </')\n[+] Malc0de Date: No results found\n[+] Malc0de IP: No results found\n[+] Malc0de Country: No results found\n[+] Malc0de ASN: No results found\n[+] Malc0de ASN Name: No results found\n[+] Malc0de MD5: No results found\nNo results found in the THIP\n[+] McAfee Web Risk: No results found\n[+] McAfee Web Category: No results found\n[+] McAfee Last Seen: No results found\n"

tabTemp = resultTemp.split("\n")
results = []
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
print(results)




