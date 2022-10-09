# Lambda Authorizer for API Gateway

Need to:
- create new authorizer under `Authorizers`
- set the authorizer in  API resource's `Method Request`
- modify `Gateway Responses -> [Access Denied, Unauthorized] -> Response templates` to
    ```json
    {
        "message":$context.error.messageString, 
        "hint":"$context.authorizer.context.hint"
    }
    ```

**Note:** updating `Gateway Responses` requires re-deploying the API to take effect

## Call with wrong pass

```sh
curl 'https://upjq3e07ih.execute-api.us-east-1.amazonaws.com/prod/upload?user=admin&pass=wrongpass'
```
```json
{ 
    "message":"User is not authorized to access this resource with an explicit deny", 
    "hint":"for authentication, use 'user=admin' and 'pass=admin' query string parameters" 
}
```
## Lambda authorizer

```python
import json

PRINCIPAL = "*"
ARN = "arn:aws:execute-api:us-east-1:808768216571:upjq3e07ih/*/GET/*" # all resources under "prod" stage

def lambda_handler(event, context):
    print("Event:", event)
    action = "allow" if is_user_allowed(event) else "deny"
    policy = generatePolicy(PRINCIPAL, action, ARN)
    print("Policy:", policy)
    return policy
    
def is_user_allowed(event):
    return event["queryStringParameters"]["user"] == "admin" and event["queryStringParameters"]["pass"] == "admin" 
    
def generatePolicy(principalId, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId
 
    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'API Gateway execute-api Policy',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }
        authResponse['policyDocument'] = policyDocument
        
    # "context" can be used in Gateway Responses->[Access Denied, Unauthorized]->Response Template: 
    # {"message":$context.error.messageString, "hint":"$context.authorizer.context.hint"}
    # NOTE: overriding default 403 message is not possible in Integration Reponse!!!
    authResponse["context"]= { "hint":"for authentication, use 'user=admin' and 'pass=admin' query string parameters" } 
    
    return authResponse
```