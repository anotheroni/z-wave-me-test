import json
import requests # apt install python-requests

topLevelUrl = 'http://IP.OF.ZWAVE.ME:8083'
DevicesUrl= topLevelUrl +'/ZAutomation/api/v1/devices'
LoginUrl = topLevelUrl + '/ZAutomation/api/v1/login'
username = 'admin'
password = 'PASSWORD'
LoginHeader = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
Formlogin = '{"form": true, "login": "'+username+'", "password": "'+password+'", "keepme": false, "default_ui": 1}'

session = requests.Session()
session.post(LoginUrl, headers=LoginHeader, data=Formlogin)

response = session.get(DevicesUrl)
parsed_json = response.json()
devices = parsed_json['data']['devices']
for entry in devices:
   try:
      print("%s %s" % (entry['metrics']['title'],
         entry['metrics']['level']))
   except KeyError:
      print("%s NONE" % (entry['metrics']['title']))
