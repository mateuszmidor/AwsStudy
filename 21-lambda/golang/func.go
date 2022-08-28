package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-lambda-go/lambda"
)

// What do we receive in HandlerRequest second argument?
// curl -X POST https://mgsgeks5uh3pa6zshktrcy46em0ipksu.lambda-url.us-east-1.on.aws?name=mateusz -H 'Content-Type: application/json' -d 'BODY HERE'
// map[
// 	   body:BODY HERE
// 	   headers:map[accept:*/* content-length:9 content-type:application/json host:mgsgeks5uh3pa6zshktrcy46em0ipksu.lambda-url.us-east-1.on.aws user-agent:curl/7.82.0 x-amzn-tls-cipher-suite:ECDHE-RSA-AES128-GCM-SHA256 x-amzn-tls-version:TLSv1.2 x-amzn-trace-id:Root=1-630658f0-109915076cca0ff76a060db8 x-forwarded-for:188.147.72.7 x-forwarded-port:443 x-forwarded-proto:https]
// 	   isBase64Encoded:false
// 	   queryStringParameters:map[name:mateusz]
// 	   rawPath:/
// 	   rawQueryString:name=mateusz
// 	   requestContext:map[
// 	   	   accountId:anonymous
// 	   	   apiId:mgsgeks5uh3pa6zshktrcy46em0ipksu
// 	   	   domainName:mgsgeks5uh3pa6zshktrcy46em0ipksu.lambda-url.us-east-1.on.aws
// 	   	   domainPrefix:mgsgeks5uh3pa6zshktrcy46em0ipksu
// 	   	   http:map[
// 	   	   	   method:POST
// 	   	   	   path:/
// 	   	   	   protocol:HTTP/1.1
// 	   	   	   sourceIp:188.147.72.7
// 	   	   	   userAgent:curl/7.82.0
// 	   	]
// 	   	requestId:422f6f2f-b9d7-4a9f-ac5c-c6ef3c0899c1
// 	   	routeKey:$default
// 	   	stage:$default
// 	   	time:24/Aug/2022:16:59:28 +0000 timeEpoch:1.661360368084e+12
// 	   ]
// 	   routeKey:$default
//     version:2.0
// ]

// type MyEvent map[string]interface{}
type MyEvent struct {
	QueryStringParameters map[string]string `json:"queryStringParameters"`
}

func HandleRequest(ctx context.Context, event MyEvent) (string, error) {
	name := event.QueryStringParameters["name"]
	json := fmt.Sprintf(`{"received_name" : "%s"}`, name) // lambda result is exected to be JSON string
	return json, nil

}

func main() {
	lambda.Start(HandleRequest)
}
