# Systems Manager

Encrypt using default KMS key:
```sh
aws ssm put-parameter --name MyParameter --value "secret_value" --type SecureString
```
```json
{
    "Version": 1,
    "Tier": "Standard"
}
```

Decrypt using default KMS key:
```sh
aws ssm get-parameter --name MyParameter --with-decryption
```
```json
{
    "Parameter": {
        "Name": "MyParameter",
        "Type": "SecureString",
        "Value": "secret_value",
        "Version": 1,
        "LastModifiedDate": 1661582232.867,
        "ARN": "arn:aws:ssm:us-east-1:808768216571:parameter/MyParameter",
        "DataType": "text"
    }
}
```