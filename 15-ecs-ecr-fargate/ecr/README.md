# ECR

## Login

`docker login` here uses default "AWS" as a login and ECR temporary token as a password that is read from std in
```sh
# NOTE: using aws cli profile configured to aws account 808768216571
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 808768216571.dkr.ecr.us-east-1.amazonaws.com

WARNING! Your password will be stored unencrypted in /home/mateusz/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

## Build & Tag

```sh
docker build -t flight-finder .
docker tag flight-finder:latest 808768216571.dkr.ecr.us-east-1.amazonaws.com/flight-finder:latest # tag the image so Docker can extract target registry url from the tag upon "push"
```

## Push
```
docker push 808768216571.dkr.ecr.us-east-1.amazonaws.com/flight-finder:latest
```

## Pull

```sh
docker pull 808768216571.dkr.ecr.us-east-1.amazonaws.com/flight-finder

Using default tag: latest
latest: Pulling from flight-finder
188c0c94c7c5: Already exists 
990c8fcaa7c2: Pull complete 
ed3bfe1a7508: Pull complete 
d916dd7cc02c: Pull complete 
Digest: sha256:59c98a6e911543684ccbbed6c85cd7ac511ba8cf01b51c539ea034e6c56358c2
Status: Downloaded newer image for 808768216571.dkr.ecr.us-east-1.amazonaws.com/flight-finder:latest
808768216571.dkr.ecr.us-east-1.amazonaws.com/flight-finder:latest
```