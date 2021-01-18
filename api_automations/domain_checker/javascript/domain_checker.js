// npm install twilio argparse axios
const twilio = require('twilio');
const axios = require('axios').default;
const { ArgumentParser } = require('argparse');

const parser = new ArgumentParser({ description: 'Check domain for availability' });
parser.addArgument('domain', {
  type: 'string',
  help: 'Domain name to be checked',
});

const { domain } = parser.parseArgs();

// twilio credentials
const accountSid = 'ENTER ACCOUNT SID HERE';
const authToken = 'ENTER AUTH TOKEN HERE';
const whatsappNumber = 'ENTER NUMBER HERE';
const client = new twilio(accountSid, authToken);

// godaddy credentials
const apiKey = 'ENTER API KEY HERE';
const apiSecret = 'ENTER API SECRET HERE';
const headers = {
  Authorization: `sso-key ${apiKey}:${apiSecret}`,
  accept: 'application/json',
};

function sendMessage(domain, number) {
  const domain_purchase_url = `https://de.godaddy.com/domainsearch/find?domainToCheck=${domain}`;
  client.messages.create({
    from: 'whatsapp:+14155238886',
    to: `whatsapp:${number}`,
    body: `Your domain ${domain} is now available for purchase. ${domain_purchase_url}`,
  }).then(() => {
    console.log(`Message was sent to ${number}.`);
  });
}

const getUrl = domain => `https://api.ote-godaddy.com/v1/domains/available?domain=${domain}`;

async function checkDomainAvailability(domain, to_number) {
  console.log(`Checking availability of domain ${domain}`);
  const res = await axios.get(getUrl(domain), { headers });

  if (res.status != 200) {
    console.log(`Error getting state of Domain ${domain}`);
    return;
  }

  const available = res.data.available;
  if (!available) {
    console.log(`Domain ${domain} is not available.`);
    return;
  }

  // send twilio message
  sendMessage(domain, to_number);
}

checkDomainAvailability(domain, whatsappNumber);