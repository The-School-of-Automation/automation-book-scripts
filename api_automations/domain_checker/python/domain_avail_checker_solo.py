import argparse
import time
import os

import requests

# set up cli domain argument
parser = argparse.ArgumentParser(description="Check domain for availability")
parser.add_argument("domain", type=str, help="Domain name to be checked")
args = parser.parse_args()

# godaddy API credentials for authoriztation
api_key = "3mM44UahMcshjE_R1iX6AkK5L14Q9CYPNfyw6"
api_secret = "WmHxMWoB2BvBBuyMh7qCuc"
req_headers = {"Authorization": f"sso-key {api_key}:{api_secret}"}


# request the development instance of godaddy for the domain
def get_req_url(check_domain):
    return f"https://api.ote-godaddy.com/v1/domains/available?domain={check_domain}"


def check_domain_available(check_domain):
    print(f"Checking availability of domain {check_domain}")
    req_url = get_req_url(check_domain)
    req = requests.get(req_url, headers=req_headers)

    # if the request was unsuccessful, notify and return
    if req.status_code != 200:
        print(
            f"Could not get availability state of domain {check_domain} - Status Code {req.response_code}"
        )
        return

    # check if the domain is available
    response = req.json()
    if response["available"] == True:
        print(f"Domain {check_domain} is available for purchase")

    else:
        print(
            f"{time.strftime('%Y-%m-%d %H:%M')} - Domain {check_domain} is not available for purchase."
        )


check_domain_available(args.domain)
