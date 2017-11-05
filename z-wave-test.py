import json
import requests # apt install python-requests
import re
import rrdtool # apt install python-rrdtool

from sensors import SENSORS, RRD_DEFS  # Sensors config file

topLevelUrl = 'http://IP.OF.ZWAVE.ME:8083'
DevicesUrl= topLevelUrl +'/ZAutomation/api/v1/devices'
LoginUrl = topLevelUrl + '/ZAutomation/api/v1/login'
username = 'admin'
password = 'PASSWORD'
LoginHeader = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
Formlogin = '{"form": true, "login": "'+username+'", "password": "'+password+'", "keepme": false, "default_ui": 1}'

re_idmatch = re.compile('\((\S+)\)') # Match 12.0 in "Dimmer (12.0) 99"

def prepare_rrd_data():
    data = dict()
    for rrd, rrdparms in RRD_DEFS.iteritems():
        data[rrd] = 'N'

    return data

def main():
    rrd_data = prepare_rrd_data()

    # Get data from Z-Wave
    session = requests.Session()
    session.post(LoginUrl, headers=LoginHeader, data=Formlogin)

    response = session.get(DevicesUrl)
    parsed_json = response.json()
    devices = parsed_json['data']['devices']

    # Parse
    for entry in devices:
       res = re_idmatch.search(entry['metrics']['title'])
       if res:
           try:
               info = SENSORS[res.group(1)]
           except KeyError:
               continue
           if info:
               try:
                   #print("%s %s %s" % (info[0], entry['metrics']['level'], info[1]))
                   if info[0]:
                       reading = entry['metrics']['level']
                       if reading == "off":
                           value = "0.0"
                       elif reading == "on":
                           value = "254.0"
                       else:
                           value = str(reading)
                       rrd_data[info[0]] += (':' + value)
               except KeyError:
                   print("%s NONE %s" % (info[0], info[1]))
                   if info[0]:
                       rrd_data[info[0]] += ':0.0'

    # Update RRD files
    for i in rrd_data:
        #print(RRD_DEFS[i]['file'] +' '+ rrd_data[i])
        res = rrdtool.update(RRD_DEFS[i]['file']+".rrd", rrd_data[i])
        if res:
            print(rrdtool.error())


if __name__ == "__main__":
    main()
