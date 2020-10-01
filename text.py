from twilio.rest import Client
from Predictions import final_dataframe
import pandas as pd
import numpy as np


output_text = final_dataframe['Total_Output(MW)'][0]

# Your Account Sid and Auth Token from twilio.com / console
account_sid = 'AC0XXXXXXXXXXXXXXXXXXXXXXX5a9b9'
auth_token = '1036eXXXXXXXXXXXXXXXXXXXXXX3ab88'
client = Client(account_sid, auth_token)

message = 'Total predicted power is {}'.format(output_text)

def sms():
    message_body = client.messages.create(
        body=message,
        from_='+12106101830',
        to='+254719671850'
        )
    return(message_body)

print(message)

