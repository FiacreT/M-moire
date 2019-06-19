import darksearch

"""
 `timeout`, `headers`, and `proxies`  are optional
 timeout = 10
 proxies = {
     "http": "http://127.0.0.1:8080"
 }
 headers = {
     "User-Agent": "Chrome/57.0.2987.133"
 }
 """
print("darksearch")
'''client = darksearch.client(timeout=30, headers=None, proxies=None)
results = client.search("cameroun")
#results = results.decode("utf-8")
results = json.loads(results)
print(results)'''

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
    sys.exit(1)


DarkScrape

https://github.com/itsmehacker/CardPwn.git'''