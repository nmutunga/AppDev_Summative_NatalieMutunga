from twilio.rest import Client
from Predictions import final_dataframe
import pandas as pd
import numpy as np
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message
from twilio.rest import Client
import urllib


output_text = final_dataframe['Total_Output(MW)'][0]

# app = Flask(__name__)
# Your Account Sid and Auth Token from twilio.com / console
account_sid = 'AC0adfaf15116c4650bd4020dd4d65a9b9'
auth_token = '1036e95afb7fa679169aedbcd463ab88'
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

