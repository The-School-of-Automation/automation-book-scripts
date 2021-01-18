import argparse
import time

import requests
import schedule
from twilio.rest import Client 

# set up cli domain argument
parser = argparse.ArgumentParser(description="Check domain for availability")
parser.add_argument("domain", type=str, help="Domain name to be checked")
args = parser.parse_args()

# godaddy API credentials for authorization
api_key = "3mM44UahMcshjE_HUPueqAPN6dU6DSVoBAsxn"
api_secret = "QdV9FjZjKvxXmVFqfLJEMk"
req_headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "accept": "application/json"
}

# twilio API credentials
account_sid = 'ACc40eb1c0368aca104f3f07a3ddb223dd' 
auth_token = '464dac8466082d9e85d2307aef1d62b1' 
client = Client(account_sid, auth_token)
to_whatsapp_number = "+4915128288055"

def send_message(check_domain, to_whatsapp_number):
    domain_purchase_url = f"https://de.godaddy.com/domainsearch/find?domainToCheck={check_domain}"

    message = client.messages.create( 
        from_='whatsapp:+14155238886',        
        to=f'whatsapp:{to_whatsapp_number}',
        body=f'Your domain {check_domain} is now available for purchase. {domain_purchase_url}' 
    )

    print(f"Message was sent to {to_whatsapp_number}, message_id is {message.sid}")

# assemble the request url with the given domain
def get_req_url(check_domain):
    return f"https://api.ote-godaddy.com/v1/domains/available?domain={check_domain}"

def check_domain_availability(check_domain, to_whatsapp_number):
    print(f"Checking availability of domain {check_domain}")
    req_url = get_req_url(check_domain)
    req = requests.get(req_url, headers=req_headers)

    # if the request was unsuccessful, notify the user and stop
    if req.status_code != 200:
        print(f"Could not get availability state of domain {check_domain} - Status Code {req.status_code}")
        return

    # check if the domain is available
    response = req.json()
    if response["available"] == True:
        print(f"Domain {check_domain} is available for purchase, sending message to {to_whatsapp_number}")
        # send whatsapp message if domain is free
        send_message(check_domain, to_whatsapp_number)
    
    else:
        print(f"{time.strftime('%Y-%m-%d %H:%M')} - Domain {check_domain} is not available for purchase.")

check_domain_availability(args.domain, to_whatsapp_number)