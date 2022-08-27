    # Resource-based policy to allow lambda invocation from another AWS account

    ```json
    {
      "Sid": "Allow3dInvoke",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::177634097045:root"
      },
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:808768216571:function:demo-lambda-func"
    }
    ```