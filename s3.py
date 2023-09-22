import json
import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

s3 = boto3.client('s3')
ses = boto3.client('ses')

def lambda_handler(event, context):
    # Get the S3 bucket and object information from the event
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Construct the S3 URL for the uploaded file
    s3_url = f's3://{bucket}/{key}'

    # Sender and recipient email addresses
    sender_email = 'charanmohitay2002@gmail.com'
    recipient_email = 'charanmohitay2002@gmail.com'

    # Email subject and body
    subject = 'File Upload Notification'
    body = f'A new file has been uploaded to S3: {s3_url}'

    # Create a MIME message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Retrieve the file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    file_data = response['Body'].read()

    # Attach the file as an attachment
    attachment = MIMEApplication(file_data)
    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(key))
    msg.attach(attachment)

    # Send the email with the file as an attachment
    try:
        response = ses.send_raw_email(
            Source=sender_email,
            Destinations=[recipient_email],
            RawMessage={'Data': msg.as_string()}
          )

        print(f"Email sent with MessageId: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': 'Email Sent Successfully.',
        }
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error Sending Email.',
        }