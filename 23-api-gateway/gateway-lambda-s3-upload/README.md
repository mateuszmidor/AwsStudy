# Serve file upload page from API Gateway with LAMBDA_PROXY integration to S3

Lambda:
```python
import json
import traceback

import cgi
import io 
import logging
import base64
import boto3

STORAGE_BUCKET_NAME = "upload-file-cognito-s3" # target S3
MAX_UPLOAD_SIZE = 10*1024 # limit uploaded file size
INPUT_NAME = "payload"

def lambda_handler(event, context):
    try:
        return handle_request(event)
    except Exception as e:
        msg = str(e) + "\n" + traceback.format_exc() + "\nEvent: " + str(event)
        print(msg)
        msg_html = msg.replace("\n", "<br>")
        return http200(msg_html)
        
def handle_request(event):
    # HTTP GET - display upload page
    if get_http_method(event) == "GET":
        upload_page = upload_page_template % (get_object_list_as_html())
        return http200(upload_page)      
        
    # HTTP POST - save file in s3 and display it's contents
    body_bytes = base64.b64decode(event["body"]) if event["isBase64Encoded"] else event["body"].encode()
    file_item = get_file_from_request_body(headers=event["headers"], body_bytes=body_bytes)
    file_content = file_item.file.read()
    if len(file_content) > MAX_UPLOAD_SIZE:
        return http200(f"File max size is {MAX_UPLOAD_SIZE} bytes")
    put_s3_object(file_item.filename, file_content)
    lines = file_content.decode('UTF-8').splitlines()
    html_content = "<br>".join(lines)
    return http200(uploaded_page_template % html_content)
    
def get_object_list_as_html():
    s3 = boto3.resource('s3')
    storage_bucket = s3.Bucket(STORAGE_BUCKET_NAME)
    items = [f"<li>key={obj.key}, size={obj.size}</li>" for obj in storage_bucket.objects.all()]
    return "<ol>\n" + "\n".join(items) + "\n</ol>\n"
    
    
def get_file_from_request_body(headers, body_bytes):
    # result:
    # {'keep_blank_values': 0, 'strict_parsing': 0, 'max_num_fields': None, 'separator': '&', 'qs_on_post': None, 'headers': , 'fp': <_io.BytesIO object at 0x7fa04808c810>, 
    # 'encoding': 'utf-8', 'errors': 'replace', 'outerboundary': b'---------------------------20411960131265153271655432068', 'bytes_read': 69, 'limit': 69, 'disposition': 'form-data', 
    # 'disposition_options': {'name': 'avatar', 'filename': 'halo.txt'}, 'name': 'avatar', 'filename': 'halo.txt', '_binary_file': True, 'type': 'text/plain', 'type_options': {}, 
    # 'innerboundary': b'', 'length': -1, 'list': None, 'file': <_io.BytesIO object at 0x7fa0473c61d0>, 'done': 1, '_FieldStorage__file': <_io.BytesIO object at 0x7fa0473c61d0>}
    fp = io.BytesIO(body_bytes)
    environ = {"REQUEST_METHOD": "POST"}
    headers = {
        "content-type": headers.get("Content-Type") or headers.get("content-type"),
    }

    fs = cgi.FieldStorage(fp=fp, environ=environ, headers=headers) 
    return  fs[INPUT_NAME]
    
def get_http_method(event):
    try:
        return event["requestContext"]["http"]["method"] # call to lambda URL
    except:
        pass
    try:
        return event["httpMethod"] # call to API Gateway with LAMBDA_PROXY
    except:
        pass
    
    raise Exception("Could not extract request method")
    
def put_s3_object(file_name, content_bytes):
    s3_path = "" + file_name
    s3 = boto3.resource("s3")
    s3.Bucket(STORAGE_BUCKET_NAME).put_object(Key=s3_path, Body=content_bytes)
    
def http200(body):
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": body
    }
    

upload_page_template= f'''
<!DOCTYPE html>
<html>
<body>

<form action="#" method="POST" enctype="multipart/form-data">
<label for="{INPUT_NAME}">Choose a file to upload:</label>
<input type="file"  id="{INPUT_NAME}" name="{INPUT_NAME}">
<input type="submit" value="Upload Now">
</form>

Objects:
%s
</body>
</html>
'''

uploaded_page_template= f'''
<!DOCTYPE html>
<html>
<body>
%s
<br>
<form>
<input type="button" value="Go back!" onclick="history.back()">
</form>

</body>
</html>
'''
```