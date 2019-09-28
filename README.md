# DigitalOcean DNS update client

The script updates the ip address for a given record using DigitalOcean API v2

## Usage

1. Set the following environmental variables:

`DO_DNS_KEY`    <DigitalOcean API access token>
`DO_DNS_DOMAIN` <e.g.: example.gr>
`DO_DNS_RECORD` <e.g.: adminpanel (adminpanel.example.gr)>

2. either run the script manually by running

`python do_dns_update_client.py`

or set a cronjob to run the script every one hour:

`0 * * * * python /path_to_script/refresh_do_dns.py >> /path_to_logs/do_dns.log 2>&1`
