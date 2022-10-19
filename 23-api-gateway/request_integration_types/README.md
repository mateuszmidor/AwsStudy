# Integrations: LAMBDA_PROXY vs LAMBDA

- `LAMBDA_PROXY` request integration fills "event" passed into handler func: 
    ```python
    def lambda_handler(event, context):
        ...
    ```
- `LAMBDA` request integration leaves "event" empty, unless you fill it in "mapping template" using Velocity language 

## "event" in direct lambda URL call

```sh
curl -X GET 'https://7syfjbogtq52kqpczfwvhqbqha0tzeav.lambda-url.us-east-1.on.aws?a=4&b=5' -H "myheader: myvalue" -H "content-type: application/json" -d '{"filename":"CV.pdf"}' 
"Hello from Lambda!"
```

"event":
```json
{
   "version":"2.0",
   "routeKey":"$default",
   "rawPath":"/",
   "rawQueryString":"a=4&b=5",
   "headers":{
      "content-length":"21",
      "x-amzn-tls-cipher-suite":"ECDHE-RSA-AES128-GCM-SHA256",
      "x-amzn-tls-version":"TLSv1.2",
      "x-amzn-trace-id":"Root=1-6331ee16-6d225e437f682e7a2c4cd96f",
      "x-forwarded-proto":"https",
      "host":"7syfjbogtq52kqpczfwvhqbqha0tzeav.lambda-url.us-east-1.on.aws",
      "x-forwarded-port":"443",
      "content-type":"application/json",
      "x-forwarded-for":"91.215.35.228",
      "accept":"*/*",
      "user-agent":"curl/7.74.0",
      "myheader":"myvalue"
   },
   "queryStringParameters":{
      "a":"4",
      "b":"5"
   },
   "requestContext":{
      "accountId":"anonymous",
      "apiId":"7syfjbogtq52kqpczfwvhqbqha0tzeav",
      "domainName":"7syfjbogtq52kqpczfwvhqbqha0tzeav.lambda-url.us-east-1.on.aws",
      "domainPrefix":"7syfjbogtq52kqpczfwvhqbqha0tzeav",
      "http":{
         "method":"GET",
         "path":"/",
         "protocol":"HTTP/1.1",
         "sourceIp":"91.215.35.228",
         "userAgent":"curl/7.74.0"
      },
      "requestId":"427ef64d-c075-4d40-8d2c-e9abb5304de5",
      "routeKey":"$default",
      "stage":"$default",
      "time":"26/Sep/2022:18:23:18 +0000",
      "timeEpoch":1664216598915
   },
   "body":"{\"filename\":\"CV.pdf\"}",
   "isBase64Encoded":false
}
```

## "event" in call through API Gateway with LAMBDA_INTEGRATION

```sh
curl -X POST 'https://upjq3e07ih.execute-api.us-east-1.amazonaws.com/prod/upload?a=4&b=5' -H "myheader: myvalue" -H "content-type: application/json" -d '{"filename":"CV.pdf"}'
"Hello from Lambda!"
```

"event":
```json
{
   "resource":"/upload",
   "path":"/upload",
   "httpMethod":"POST",
   "headers":{
      "accept":"*/*",
      "content-type":"application/json",
      "Host":"upjq3e07ih.execute-api.us-east-1.amazonaws.com",
      "User-Agent":"curl/7.74.0",
      "X-Amzn-Trace-Id":"Root=1-6331f15a-6b6db5cf3383749971b7f2f3",
      "X-Forwarded-For":"91.215.35.228",
      "X-Forwarded-Port":"443",
      "X-Forwarded-Proto":"https",
      "myheader":"myvalue"
   },
   "multiValueHeaders":{
      "accept":[
         "*/*"
      ],
      "content-type":[
         "application/json"
      ],
      "Host":[
         "upjq3e07ih.execute-api.us-east-1.amazonaws.com"
      ],
      "myheader":[
         "myvalue"
      ],
      "User-Agent":[
         "curl/7.74.0"
      ],
      "X-Amzn-Trace-Id":[
         "Root=1-6331f15a-6b6db5cf3383749971b7f2f3"
      ],
      "X-Forwarded-For":[
         "91.215.35.228"
      ],
      "X-Forwarded-Port":[
         "443"
      ],
      "X-Forwarded-Proto":[
         "https"
      ]
   },
   "queryStringParameters":{
      "a":"4",
      "b":"5"
   },
   "multiValueQueryStringParameters":{
      "a":[
         "4"
      ],
      "b":[
         "5"
      ]
   },
   "pathParameters":"None",
   "stageVariables":"None",
   "requestContext":{
      "resourceId":"ws0vo4",
      "resourcePath":"/upload",
      "httpMethod":"POST",
      "extendedRequestId":"ZFKmNG9eIAMFaYw=",
      "requestTime":"26/Sep/2022:18:37:14 +0000",
      "path":"/prod/upload",
      "accountId":"808768216571",
      "protocol":"HTTP/1.1",
      "stage":"prod",
      "domainPrefix":"upjq3e07ih",
      "requestTimeEpoch":1664217434705,
      "requestId":"eda39e9d-84f8-427b-a0a2-80fe06c7cb51",
      "identity":{
         "cognitoIdentityPoolId":"None",
         "accountId":"None",
         "cognitoIdentityId":"None",
         "caller":"None",
         "sourceIp":"91.215.35.228",
         "principalOrgId":"None",
         "accessKey":"None",
         "cognitoAuthenticationType":"None",
         "cognitoAuthenticationProvider":"None",
         "userArn":"None",
         "userAgent":"curl/7.74.0",
         "user":"None"
      },
      "domainName":"upjq3e07ih.execute-api.us-east-1.amazonaws.com",
      "apiId":"upjq3e07ih"
   },
   "body":"{\"filename\":\"CV.pdf\"}",
   "isBase64Encoded":false
}
```