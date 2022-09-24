# CDK example - Create S3 Bucket in Python

Based on https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html

## Prerequisites

- Python >= 3.6
- Node.js > 13.6.0 (Ubuntu install: `sudo snap install node --classic`)
- Configured AWS CLI (add profile using: `aws configure`)

## Steps

- Install CKD:
    ```sh
    npm install -g aws-cdk
    ```

- Bootstrap CDK in the cheapest region (this will create S3 bucket, CloudFormation stack, IAM roles for working with CDK):
    ```sh
    aws sts get-caller-identity # get your AWS account number
    cdk bootstrap aws://ACCOUNT-NUMBER/us-east-1 
    ```

- Init Python `storage` app in an empty folder (must be empty):
    ```sh
    mkdir storage
    cd storage
    cdk init app --language python # app is a CDK template for empty application; there is also 'sample-app' - Example CDK Application with some constructs
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    ```
- Verify the CDK stack is created:
    ```sh
    cdk ls
    ```
    ```sh
    StorageStack
    ```

- Add S3 Bucket in `storage_stack.py` (replace file content altogether):
    ```python
    import aws_cdk as cdk
    import aws_cdk.aws_s3 as s3


    class StorageStack(cdk.Stack):
        def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)

            bucket = s3.Bucket(self, "MyFirstBucket")

    ```
- Synthesize the stack (translate CDK code -> CloudFormation template) - this step is just for validation:
    ```sh
    cdk synth 
    ```
    ```yaml
    Resources:
    MyFirstBucketB8884501:
        Type: AWS::S3::Bucket
        UpdateReplacePolicy: Retain
        DeletionPolicy: Retain
        Metadata:
        aws:cdk:path: StorageStack/MyFirstBucket/Resource
    CDKMetadata:
        Type: AWS::CDK::Metadata
        Properties:
        Analytics: v2:deflate64:H4sIAAAAAAAA/yXITQ5AMBBA4bPYt+M3EVsuIBxAqIpRpolOIyLujli9Ly+BLIYo6A8n1WjkigNcLffKiHd1LoWr9MpoFtVEv+6PjXbW70p/riyNyGjpFvXJs6UwhQLyYHGIcvfEuGlo/j5mOGWSbwAAAA==
        Metadata:
        aws:cdk:path: StorageStack/CDKMetadata/Default
        Condition: CDKMetadataAvailable
    Conditions:
    CDKMetadataAvailable:
        Fn::Or:
        - Fn::Or:
            - Fn::Equals:
                - Ref: AWS::Region
                - af-south-1
            - Fn::Equals:
                - Ref: AWS::Region
                - ap-east-1
            - Fn::Equals:
                - Ref: AWS::Region
                - ap-northeast-1
            - Fn::Equals:
                - Ref: AWS::Region
                - ap-northeast-2
            - Fn::Equals:
                - Ref: AWS::Region
                - ap-south-1
            - Fn::Equals:
                - Ref: AWS::Region
                - ap-southeast-1
            - Fn::Equals:
                - Ref: AWS::Region
                - ap-southeast-2
            - Fn::Equals:
                - Ref: AWS::Region
                - ca-central-1
            - Fn::Equals:
                - Ref: AWS::Region
                - cn-north-1
            - Fn::Equals:
                - Ref: AWS::Region
                - cn-northwest-1
        - Fn::Or:
            - Fn::Equals:
                - Ref: AWS::Region
                - eu-central-1
            - Fn::Equals:
                - Ref: AWS::Region
                - eu-north-1
            - Fn::Equals:
                - Ref: AWS::Region
                - eu-south-1
            - Fn::Equals:
                - Ref: AWS::Region
                - eu-west-1
            - Fn::Equals:
                - Ref: AWS::Region
                - eu-west-2
            - Fn::Equals:
                - Ref: AWS::Region
                - eu-west-3
            - Fn::Equals:
                - Ref: AWS::Region
                - me-south-1
            - Fn::Equals:
                - Ref: AWS::Region
                - sa-east-1
            - Fn::Equals:
                - Ref: AWS::Region
                - us-east-1
            - Fn::Equals:
                - Ref: AWS::Region
                - us-east-2
        - Fn::Or:
            - Fn::Equals:
                - Ref: AWS::Region
                - us-west-1
            - Fn::Equals:
                - Ref: AWS::Region
                - us-west-2
    Parameters:
    BootstrapVersion:
        Type: AWS::SSM::Parameter::Value<String>
        Default: /cdk-bootstrap/hnb659fds/version
        Description: Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store. [cdk:skip]
    Rules:
    CheckBootstrapVersion:
        Assertions:
        - Assert:
            Fn::Not:
                - Fn::Contains:
                    - - "1"
                    - "2"
                    - "3"
                    - "4"
                    - "5"
                    - Ref: BootstrapVersion
            AssertDescription: CDK bootstrap stack version 6 required. Please run 'cdk bootstrap' with a recent version of the CDK CLI.
    ```

- Deploy the stack:
    ```sh
    cdk deploy
    ```
    , CloudFormation stack `StorageStack` and S3 Bucket `MyFirstBucketB8884501` (suffix random) gets created

- Update the bucket definition in `storage_stack.py`, and run diff:
    ```python
    import aws_cdk as cdk
    import aws_cdk.aws_s3 as s3


    class StorageStack(cdk.Stack):
        def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)

            bucket = s3.Bucket(self, "MyFirstBucket", removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=True)

    ```
    ```sh
    cdk diff
    ```
    ```sh
    Stack StorageStack
    IAM Statement Changes
    ┌───┬───────────────────────────────────────────┬────────┬───────────────────────────────────────────┬───────────────────────────────────────────┬───────────┐
    │   │ Resource                                  │ Effect │ Action                                    │ Principal                                 │ Condition │
    ├───┼───────────────────────────────────────────┼────────┼───────────────────────────────────────────┼───────────────────────────────────────────┼───────────┤
    │ + │ ${Custom::S3AutoDeleteObjectsCustomResour │ Allow  │ sts:AssumeRole                            │ Service:lambda.amazonaws.com              │           │
    │   │ ceProvider/Role.Arn}                      │        │                                           │                                           │           │
    ├───┼───────────────────────────────────────────┼────────┼───────────────────────────────────────────┼───────────────────────────────────────────┼───────────┤
    │ + │ ${MyFirstBucket.Arn}                      │ Allow  │ s3:DeleteObject*                          │ AWS:${Custom::S3AutoDeleteObjectsCustomRe │           │
    │   │ ${MyFirstBucket.Arn}/*                    │        │ s3:GetBucket*                             │ sourceProvider/Role.Arn}                  │           │
    │   │                                           │        │ s3:List*                                  │                                           │           │
    └───┴───────────────────────────────────────────┴────────┴───────────────────────────────────────────┴───────────────────────────────────────────┴───────────┘
    IAM Policy Changes
    ┌───┬───────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────┐
    │   │ Resource                                                                  │ Managed Policy ARN                                                         │
    ├───┼───────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────┤
    │ + │ ${Custom::S3AutoDeleteObjectsCustomResourceProvider/Role}                 │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBa │
    │   │                                                                           │ sicExecutionRole"}                                                         │
    └───┴───────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────┘
    Resources
    [+] AWS::S3::BucketPolicy MyFirstBucket/Policy MyFirstBucketPolicy3243DEFD 
    [+] Custom::S3AutoDeleteObjects MyFirstBucket/AutoDeleteObjectsCustomResource MyFirstBucketAutoDeleteObjectsCustomResourceC52FCF6E 
    [+] AWS::IAM::Role Custom::S3AutoDeleteObjectsCustomResourceProvider/Role CustomS3AutoDeleteObjectsCustomResourceProviderRole3B1BD092 
    [+] AWS::Lambda::Function Custom::S3AutoDeleteObjectsCustomResourceProvider/Handler CustomS3AutoDeleteObjectsCustomResourceProviderHandler9D90184F 
    [~] AWS::S3::Bucket MyFirstBucket MyFirstBucketB8884501 
    ├─ [+] Tags
    │   └─ [{"Key":"aws-cdk:auto-delete-objects","Value":"true"}]
    ├─ [~] DeletionPolicy
    │   ├─ [-] Retain
    │   └─ [+] Delete
    └─ [~] UpdateReplacePolicy
        ├─ [-] Retain
        └─ [+] Delete
    ```
    , these changes will be applied when you run `cdk deploy`

- Delete all:
    ```sh
    cdk destroy
    ```