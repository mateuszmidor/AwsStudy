# 1. make bucket
aws s3 mb s3://mateusz-demo-sam-bucket

# 2. package cloudformation
aws cloudformation package --s3-bucket mateusz-demo-sam-bucket --template-file template.yaml --output-template-file gen/template-generated.yaml

# 3. deploy cloudformation
aws cloudformation deploy --template-file gen/template-generated.yaml --stack-name sam-hello-world --capabilities CAPABILITY_IAM