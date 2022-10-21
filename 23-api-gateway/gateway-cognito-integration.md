# How to secure API Gateway with Cognito User Pool authorizer 

Cognito Authorizer expects the `id_token` received from User Pool login to be provided in incoming request's header `Authorization: Bearer <id_token>` to let the request through