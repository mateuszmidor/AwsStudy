# AWS Lambda Go example

AWS needs a library compiled for Linux, static build:
```sh
CGO_ENABLED=0 GOOS=linux go build func.go
```

AWS needs the binary in ZIP:
```sh
zip func.zip func
```

AWS Lambda needs the RuntimeSettings.Handler name match the binary name - i.e. "func" (set it in your AWS Console)