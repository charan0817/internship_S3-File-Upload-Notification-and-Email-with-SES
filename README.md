This AWS Lambda function is triggered by an event in Amazon S3 whenever a file is uploaded to a specific bucket. Upon activation, 
the function performs the following actions:
1.Extracts the S3 bucket name and file key from the event data.
2.Constructs the S3 URL for the uploaded file.
3.Sends an email notification using Amazon Simple Email Service (SES) to the specified recipient. The email includes:
  i.A plain-text message informing the recipient about the uploaded file.
  ii.The uploaded file as an attachment, retrieved from the S3 bucket.
The script uses the boto3 library for interacting with AWS S3 and SES services and the email package to compose a MIME email with attachments. 
Error handling ensures that issues during email transmission are logged and returned as part of the Lambda function's response.
