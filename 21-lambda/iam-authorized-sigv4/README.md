# HTTP POST to IAM-protected lambda

Requests towards Lambda functions with `auth type=AWS_IAM` must be signed vith SigV4 - in http header or in query string.  

## Lambda API

- POST (sync invoke): https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html

## Signing the request - Python example

- Lambda POST: https://gist.github.com/nivertech/013fd0f8aa116c3edb65
- IAM POST, IAM GET: https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html