# How to assume a "guest" IAM role in target AWS account by user from current AWS account

The point in assuming a role is that:
* target account may create a "guest" role with permissions for the guest users from another AWS accounts, so they can do things in that target account
* guest user from current AWS account can asssume the role (basically he calls "aws sts assume-role ..." and receives temporary credentials that allow him to use the guest role)
* to make this work, "guest" role must allow being assumed by specified user from current account, and the user himself needs permission policy to call aws sts assume-role

## Steps

Having AWS current account `177634097045` and target account `808768216571`:

1. Create regular user "user" in current AWS account `177634097045` with Permission policy allowing him to call aws sts asume-role:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "1",
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Resource": "*"
            }
        ]
    }
    ```
    This user needs no other permissions; permissions will come from the "guest" role assumed in target AWS account `808768216571`.

2. Create "guest" role in target AWS account `808768216571`.  
This role will be assumed by "user" from current account `177634097045`.  
To allow being assumed, the "guest" role needs a TrustRelationship policy:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::177634097045:user/user" <--- user "user" from current account is allowed to assume this role
                },
                "Action": "sts:AssumeRole",
                "Condition": {}
            }
        ]
    } 
    ```
    Beside TrustRelationship policy, the "guest" role should also provide some actual Permissions policy for the guest user, say, S3 reading:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:Get*",
                    "s3:List*",
                ],
                "Resource": "*"
            }
        ]
    }
    ```

3. Assume the role in the target account `808768216571`:
    ```sh
    aws --profile=user sts assume-role --role-arn arn:aws:iam::808768216571:role/guest --role-session-name my-temporary-role
    ```
    , temporary credentials get returned (valid for max 60 minutes and can be manually invalidated on the Role page in AWS Console):
    ```json
    {
        "Credentials": {
            "AccessKeyId": "ASIA3YTSXTX57R7W5FGE",
            "SecretAccessKey": "7XZTWm8B6223HF26GPDoXW7Sh0kXHCAoIymhwRF1",
            "SessionToken": "FwoGZXIvYXdzEPL//////////wEaDIceT1eMkt1AskWtsyKyAbRoORKjiJ06SJIgCJ/uondYBX0tLGtJujF9aiDti2EM2UHGlyI1WyoZxY0ECBe10dobH45iEAwFdEvbDY1AeK9A3i/MnOwlB62szVlEAiGpF+eTWoDHsygPAt+zUF1y81G+jm7voyJbBxnzBQBUkhSAuBrN74LK4Vjaja9lPvbE3vh1CWF7IItLuN+sfehRppYxPfu5c4KYcBsNbYYoiarp+5iwnJUe7bleyKU/2UmDwvgo3NCHmAYyLdF+jvmqsHvRNgaIUbZpDNeb4HzE40RfccI4RTdd1xr3A7eTsrmjZMe6W1O9LQ==",
            "Expiration": "2022-08-21T09:10:04Z"
        },
        "AssumedRoleUser": {
            "AssumedRoleId": "AROA3YTSXTX5SVVUEOLYJ:my-temporary-role",
            "Arn": "arn:aws:sts::808768216571:assumed-role/guest/my-temporary-role"
        }
    }
    ```

    , now set the credentials:
    ```sh
    export AWS_ACCESS_KEY_ID=RoleAccessKeyID
    export AWS_SECRET_ACCESS_KEY=RoleSecretKey
    export AWS_SESSION_TOKEN=RoleSessionToken
    ```

4. Check if assume role was successful, don't use --profile as it overrides the env variables!
    ```sh
    aws sts get-caller-identity
    ```

    ```json
    {
        "UserId": "AROA3YTSXTX5SVVUEOLYJ:my-temporary-role",
        "Account": "808768216571",
        "Arn": "arn:aws:sts::808768216571:assumed-role/guest/my-temporary-role"
    }
    ```
5. Call AWS API in current account:
    ```sh
    aws s3 ls s3://blue-bucket
    ```
    ```text
    2022-08-21 10:24:11        216 websocket.sh
    ...
    ```