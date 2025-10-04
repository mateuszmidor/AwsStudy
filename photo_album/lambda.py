# This Lambda handles S3 Event Notifications for creating and deleting objects:
# - on image create - it creates a thumbnail
# - on thumbnail create - it regenerates index.html
# - on image removal - it deletes thumbnail and regenerates index.html
import json
import pprint
import boto3
import os
import tempfile
from PIL import Image

# THUMB_PREFIX is to distinguish the generated thumbnails.
THUMB_PREFIX = 'thumb_'

# get_object_key retrieves the object_key from S3 event, e.g. "images/sky.jpg"
def get_object_key(event):
    try:
        return event['Records'][0]['s3']['object']['key']
    except (KeyError, IndexError, TypeError):
        return None

# get_bucket_name retrieves the bucket name from S3 event, e.g. "photo-album-bucket"
def get_bucket_name(event):
    try:
        return event['Records'][0]['s3']['bucket']['name']
    except (KeyError, IndexError, TypeError):
        return None

# get_object_name extracts S3 Object Name from Object Key, e.g. "images/sky.jpg" -> "sky.jpg"
def get_object_name(object_key):
    return os.path.basename(object_key)

def is_image(object_key):
    return object_key.endswith((".jpg", ".jpeg", ".png"))

def is_thumbnail(object_key):
    name = get_object_name(object_key).lower() # e.g. "images/thumb_sky.jpg" -> "thumb_sky.jpg"
    prefix = THUMB_PREFIX.lower()
    return name.startswith(prefix)

# is_S3_event returns true if the event represents S3 notification event named "event_name"
def is_S3_event(event, event_name):
    if event.get('Records') is None:
        return False
    if len(event['Records']) == 0:
        return False
    record = event['Records'][0]
    if record.get('eventName') != event_name:
        return False

    if record.get('s3') is None:
        return False
    s3 = record['s3']
    if s3.get('bucket') is None:
        return False
    bucket = s3['bucket']
    if bucket.get('name') is None:
        return False
    if s3.get('object') is None:
        return False
    obj = s3['object']
    if obj.get('key') is None:
        return False
    return True

def is_S3_file_upload_event(event):
    return is_S3_event(event, "ObjectCreated:Put")

def is_S3_file_remove_event(event):
    return is_S3_event(event, "ObjectRemoved:Delete")

# make_thumb_key adds "thumb_" prefix to the object key, eg "images/sky.jpg" -> "images/thumb_sky.jpg"
def make_thumb_key(object_key):
    dirname = os.path.dirname(object_key)
    object_name = get_object_name(object_key)

    thumb_basename = THUMB_PREFIX + object_name
    if dirname and dirname != '.':
        return f"{dirname}/{thumb_basename}"
    else:
        return thumb_basename

# create_thumbnail creates a thumbnail of maximum size 256x256 pixels for image under bucket_name/object_key,
# and saves it to S3 in provided bucket_name under object_key name prefixed with 'thumb_'
def create_thumbnail(bucket_name, object_key):
    SIZE = 256
    s3 = boto3.client('s3')

    # Download image from  S3 into tmp directory, create thumbnail, and upload the thumbnail to S3
    with tempfile.TemporaryDirectory() as tmpdir:
        # Download original image
        download_path = os.path.join(tmpdir, os.path.basename(object_key))
        s3.download_file(bucket_name, object_key, download_path)

        # Open image, create thumbnail, save in tmp folder
        with Image.open(download_path) as img:
            img.thumbnail((SIZE, SIZE))
            thumb_path = os.path.join(tmpdir, THUMB_PREFIX + os.path.basename(object_key))
            img.save(thumb_path, format=img.format, exif=img._exif) # exif to avoid image being rotated

        # Upload thumbnail to S3
        thumb_key = make_thumb_key(object_key)
        print(f"creating thumbnail: {bucket_name}/{thumb_key}")
        s3.upload_file(thumb_path, bucket_name, thumb_key)

# generate_index_html regenerates the gallery main page:
# 1. list all thumbnails under bucket_name bucket (images which name starts with "thumb_")
# 2. create a gallery that displays the listed thumbnails, 7 elements per row
#   -> after clicking thumbnail, the full-size image is opened in a new tab
# 3. store the generated web page under bucket_name/index.html
def generate_index_html(bucket_name):
    print(f"regenerating index page: {bucket_name}/index.html")

    s3 = boto3.client('s3')

    # 1. List all thumbnails under bucket_name
    paginator = s3.get_paginator('list_objects_v2')
    thumb_keys = []
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if is_image(key) and is_thumbnail(key):
                thumb_keys.append(key)

    # 2. Create a gallery that displays the listed thumbnails, 7 per row. After clicking the thumbnail, the full-size image is opened in new tab
    #    Assume all images are in the root or subfolders, and the full image is the same key without the prefix
    gallery_html = '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    gallery_html += '    <meta charset="UTF-8">\n'
    gallery_html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    gallery_html += '    <title>Photo Album</title>\n'
    gallery_html += '    <style>\n'
    gallery_html += '        body { font-family: Arial, sans-serif; }\n'
    gallery_html += '        .gallery { display: flex; flex-wrap: wrap; gap: 10px; }\n'
    gallery_html += '        .gallery-item { flex: 1 0 13%; box-sizing: border-box; margin-bottom: 10px; }\n'
    gallery_html += '        .gallery-item img { max-width: 100%; height: auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: block; }\n'
    gallery_html += '        .gallery-item { text-align: center; }\n'
    gallery_html += '        @media (max-width: 800px) { .gallery-item { flex-basis: 45%; } }\n'
    gallery_html += '        @media (max-width: 500px) { .gallery-item { flex-basis: 100%; } }\n'
    gallery_html += '    </style>\n'
    gallery_html += '</head>\n<body>\n'
    gallery_html += f'    <h1>Photo Album - {len(thumb_keys)} images</h1>\n'
    gallery_html += '    <div class="gallery">\n'

    for thumb_key in thumb_keys:
        # Remove THUMB_PREFIX from basename to get original image key
        import os
        dirname = os.path.dirname(thumb_key)
        basename = os.path.basename(thumb_key)
        if basename.startswith(THUMB_PREFIX):
            orig_basename = basename[len(THUMB_PREFIX):]
        else:
            orig_basename = basename
        if dirname and dirname != '.':
            orig_key = f"{dirname}/{orig_basename}"
        else:
            orig_key = orig_basename

        thumb_url = f"/{thumb_key}"
        orig_url = f"/{orig_key}"
        gallery_html += f'        <div class="gallery-item"><a href="{orig_url}" target="_blank"><img src="{thumb_url}" alt="Photo"></a></div>\n'

    gallery_html += '    </div>\n'
    gallery_html += '</body>\n</html>\n'

    # 3. Store the generated web page under bucket_name/index.html
    s3.put_object(
        Bucket=bucket_name,
        Key="index.html",
        Body=gallery_html.encode("utf-8"),
        ContentType="text/html"
    )

def handle_file_upload(bucket_name, object_key):
    print(f"handling S3 Create Event: {bucket_name}/{object_key}")

    # skip non-image uploads
    if not is_image(object_key):
        print("not image, skipping")
        return

    # handle image uploads
    if is_thumbnail(object_key): # thumbnail image has just been uploaded; update the gallery index page
        generate_index_html(bucket_name)
    else: # non-thumbnail image has been uploaded; create a thumbnail for it
        create_thumbnail(bucket_name, object_key)

def handle_file_remove(bucket_name, object_key):
    print(f"handling S3 Delete Event: {bucket_name}/{object_key}")

    # skip non-image removals
    if not is_image(object_key):
         print("not image, skipping")
         return

    # skip thumbnail removals
    if is_thumbnail(object_key):
        print("a thumbnail, skipping")
        return

    # remove thumbnail image from S3
    thumb_key = make_thumb_key(object_key)
    print(f"removing thumbnail: {bucket_name}/{thumb_key}")
    s3 = boto3.client('s3')
    s3.delete_object(Bucket=bucket_name, Key=thumb_key)

    # regenerate the gallery index page
    generate_index_html(bucket_name)

# lambda_handler is the entry point to the Lambda; it is called in reponse to S3 Event Notification
def lambda_handler(event, context):
    print ("starting photo album lambda_handler")
    print(event)

    # handle file operations in S3 bucket
    if is_S3_file_upload_event(event):
        bucket_name = get_bucket_name(event)
        object_key = get_object_key(event)
        handle_file_upload(bucket_name, object_key)
        return "SUCCESS"
    elif is_S3_file_remove_event(event):
        bucket_name = get_bucket_name(event)
        object_key = get_object_key(event)
        handle_file_remove(bucket_name, object_key)
        return "SUCCESS"
    else:
        print("Not S3 File Upload Event; skipping")
        return "FAILURE"