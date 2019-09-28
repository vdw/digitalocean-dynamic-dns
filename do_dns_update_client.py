#!/usr/bin/env python

# DigitalOcean Dynamic DNS
#
# The script updates the ip address
# for a given record using DigitalOcean API v2
#
# Requires Python 2

from datetime import datetime
import requests, certifi, json, re, os

APIKEY  = os.environ.get('DO_DNS_KEY')
DOMAIN  = os.environ.get('DO_DNS_DOMAIN')
RECORD  = os.environ.get('DO_DNS_RECORD')

CHECKIP = 'https://ipinfo.io/ip'
APIURL  = 'https://api.digitalocean.com/v2'

HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(APIKEY)}

def get_ip():
    response = requests.get(CHECKIP, verify=certifi.where())

    if response.status_code == 200:
        return response.content.rstrip()
    else:
        return response.status_code

def get_record_id():
    response = requests.get('{0}/domains/{1}/records'.format(APIURL, DOMAIN),
                            verify=certifi.where(),
                            headers=HEADERS)

    if response.status_code == 200:
        results = response.json()

        for record in results['domain_records']:
            if record['name'] == RECORD:
                return record['id']
    else:
        return response.status_code

def update_record(record_id, current_ip):
    response = requests.put('{0}/domains/{1}/records/{2}'.format(APIURL, DOMAIN, record_id),
                            verify=certifi.where(),
                            headers=HEADERS,
                            data=json.dumps({'data': current_ip}).encode('utf-8'))

    if response.status_code == 200:
        return 'ok'
    else:
        return response.status_code

if __name__ == '__main__':

    if (not APIKEY) or (not DOMAIN) or (not RECORD):
        print('Environment variables (DO_DNS_KEY, DO_DNS_DOMAIN, DO_DNS_RECORD) are missing!')

    else:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        current_time_human = now.strftime("%B %d, %Y %H:%M:%S")

        try:
            current_ip = get_ip()
            record_id = get_record_id()
            update_record(record_id, current_ip)

            print('{0} {1} Record ID: {2}; Current IP: {3}'.format(current_time_human, record_id, current_ip))

        except Exception, err:
            print('{0} Error: {1}'.format(current_time_human, err))
