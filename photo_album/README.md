# low-cost photo album in AWS

Highlights:
- uses S3 to store uploaded images
- uses S3 static web hosting to expose the index.html and images to the world
- uses S3 event notifications to react to images being uploaded/removed
  - uses Lambda to generate thumbnail & update index.html on file upload
  - uses Lambda to remove thumbnail & update index.html on file removal
  - note: Lambda needs Pillow package added as a Layer: arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p312-Pillow:7

## S3 bucket policy for album bucket
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowViewImagesByAnyone",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mateuszmidor-photo-album/*"
        },
        {
            "Sid": "AllowReadImagesByLambda",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::222165755023:role/service-role/mateuszmidor-photo-album"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mateuszmidor-photo-album/*"
        },
        {
            "Sid": "AllowListBucketByLambda",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::222165755023:role/service-role/mateuszmidor-photo-album"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::mateuszmidor-photo-album"
        },
        {
            "Sid": "AllowStoreThumbnailsByLambda",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::222165755023:role/service-role/mateuszmidor-photo-album"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::mateuszmidor-photo-album/*"
        },
        {
            "Sid": "AllowRemoveThumbnailsByLambda",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::222165755023:role/service-role/mateuszmidor-photo-album"
            },
            "Action": "s3:DeleteObject",
            "Resource": "arn:aws:s3:::mateuszmidor-photo-album/thumb_*"
        }
    ]
}
```

## Resource-based policy statements for Lambda
Should get automatically added when selecting the Lambda as S3 event notification handler - should allow invocations by S3.