# AWS Version 4 signing example
# taken from:
#    http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html

# Lambda API (InvokeAsync)
# http://docs.aws.amazon.com/lambda/latest/dg/API_InvokeAsync.html

# See: http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
# This version makes a POST request and passes request parameters
# in the body (payload) of the request. Auth information is passed in
# an Authorization header.
import sys, os, datetime, hashlib, hmac
import requests  # pip install requests


# ************* REQUEST VALUES *************
FUNCTION_NAME = "iam-secured-example"
method = "POST"  # Lambda exposes POST API, as it is generally a data processor: input -> Lambda -> output
service = "lambda"
region = "us-east-1"
host = "lambda.us-east-1.amazonaws.com"
endpoint = "https://lambda.us-east-1.amazonaws.com"
path = f"/2015-03-31/functions/{FUNCTION_NAME}/invocations"
request_url = endpoint + path

# POST requests use a content type header.
content_type = "application/x-amz-json-1.0"

# Request parameters  passed in a JSON
request_parameters = "{}"

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, "aws4_request")
    return kSigning


# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
access_key = os.environ.get("AWS_ACCESS_KEY_ID")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

if access_key is None or secret_key is None:
    print("No access key is available (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).")
    sys.exit(1)

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amz_date = t.strftime("%Y%m%dT%H%M%SZ")
date_stamp = t.strftime("%Y%m%d")  # Date w/o time, used in credential scope


# ************* TASK 1: CREATE A CANONICAL REQUEST *************
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Step 1 is to define the verb (GET, POST, etc.)--already done.

# Step 2: Create canonical URI--the part of the URI from domain to query
# string (use '/' if no path)
canonical_uri = path

## Step 3: Create the canonical query string. In this example, request
# parameters are passed in the body of the request and the query string
# is blank.
canonical_querystring = ""

# Step 4: Create the canonical headers. Header names and values
# must be trimmed and lowercase, and sorted in ASCII order.
# Note that there is a trailing \n.
# canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:' + amz_target + '\n'
canonical_headers = "content-type:" + content_type + "\n" + "host:" + host + "\n" + "x-amz-date:" + amz_date + "\n"


# Step 5: Create the list of signed headers. This lists the headers
# in the canonical_headers list, delimited with ";" and in alpha order.
# Note: The request can include any headers; canonical_headers and
# signed_headers include those that you want to be included in the
# hash of the request. "Host" and "x-amz-date" are always required.
# For DynamoDB, content-type and x-amz-target are also required.
# signed_headers = 'content-type;host;x-amz-date;x-amz-target'
signed_headers = "content-type;host;x-amz-date"


# Step 6: Create payload hash. In this example, the payload (body of
# the request) contains the request parameters.
payload_hash = hashlib.sha256(request_parameters.encode("utf-8")).hexdigest()

# Step 7: Combine elements to create create canonical request
canonical_request = (
    method
    + "\n"
    + canonical_uri
    + "\n"
    + canonical_querystring
    + "\n"
    + canonical_headers
    + "\n"
    + signed_headers
    + "\n"
    + payload_hash
)
print(canonical_request)


# ************* TASK 2: CREATE THE STRING TO SIGN*************
# Match the algorithm to the hashing algorithm you use, either SHA-1 or
# SHA-256 (recommended)
algorithm = "AWS4-HMAC-SHA256"
credential_scope = date_stamp + "/" + region + "/" + service + "/" + "aws4_request"
string_to_sign = (
    algorithm
    + "\n"
    + amz_date
    + "\n"
    + credential_scope
    + "\n"
    + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
)
print("To sign:\n", string_to_sign)

# ************* TASK 3: CALCULATE THE SIGNATURE *************
# Create the signing key using the function defined above.
signing_key = getSignatureKey(secret_key, date_stamp, region, service)

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256).hexdigest()


# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
# Put the signature information in a header named Authorization.
authorization_header = (
    algorithm
    + " "
    + "Credential="
    + access_key
    + "/"
    + credential_scope
    + ", "
    + "SignedHeaders="
    + signed_headers
    + ", "
    + "Signature="
    + signature
)

# For DynamoDB, the request can include any headers, but MUST include "host", "x-amz-date",
# "x-amz-target", "content-type", and "Authorization". Except for the authorization
# header, the headers must be included in the canonical_headers and signed_headers values, as
# noted earlier. Order here is not significant.
# # Python note: The 'host' header is added automatically by the Python 'requests' library.
headers = {"Content-Type": content_type, "Host": host, "X-Amz-Date": amz_date, "Authorization": authorization_header}

# ************* SEND THE REQUEST *************
print("\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++")
print("Request URL = " + request_url)

r = requests.post(request_url, data=request_parameters, headers=headers)

print("\nRESPONSE++++++++++++++++++++++++++++++++++++")
print("Response code: %d" % r.status_code)
print(r.text)
