import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request

app = Flask(__name__)

def send_email(subject, recipient, body):
    sender_email = 'crumb.commander@gmail.com'
    password = 'dkab dctq eqok fbuq'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        return "Email sent successfully!"
    except Exception as e:
        return str(e)

def lambda_handler(event, context):
    if event.get('httpMethod') == 'POST' and event.get('body'):
        data = json.loads(event['body'])
        subject = data.get('subject')
        recipient = data.get('recipient')
        body = data.get('body')
        if not subject or not recipient or not body:
            return {
                "statusCode": 400,
                "body": "Error: Subject, recipient, and body are required."
            }
        else:
            result = send_email(subject, recipient, body)
            return {
                "statusCode": 200,
                "body": result
            }
    else:
        return {
            "statusCode": 400,
            "body": "Error: Invalid request."
        }

if __name__ == '__main__':
    app.run(debug=True)