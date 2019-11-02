# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACa8b8499c4379b5b36d473cc857d8d6e3'
auth_token = '210e881f87774813168e3150c46b5181'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hello from FitMyFriends!",
                     from_='+12018957532',
                     to='16155097738'
                 )

print(message.sid)
