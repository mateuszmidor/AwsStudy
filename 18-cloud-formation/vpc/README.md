# Create VPC with CloudFormation

This VPC allows EC2 connection to internet - if EC2 created in public subnetwork.  
Connecting with EC2 over SSH or AWS Connect requires adding SecurityGroup allowing inbound SSH.  
Template from: https://docs.aws.amazon.com/codebuild/latest/userguide/cloudformation-vpc-template.html  

- create stack
    ```sh
    aws cloudformation create-stack --stack-name myteststack --template-body file://vpc.yaml --parameters ParameterKey=EnvironmentName,ParameterValue=mytestenv
    ```

- list stacks
    ```sh
    aws cloudformation list-stacks
    ```

- delete stack
    ```sh
    aws cloudformation delete-stack --stack-name myteststack
    ```

