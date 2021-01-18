from twilio.rest import Client 
 
account_sid = 'ACc40eb1c0368aca104f3f07a3ddb223dd' 
auth_token = '464dac8466082d9e85d2307aef1d62b1' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Your Twilio code is 1238432',      
                              to='whatsapp:+4915128288055' 
                          ) 
 
print(message.sid)