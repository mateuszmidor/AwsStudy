# Elasticache

Elasticache Clusters are intended to be run from inside Amazon VPC, connecting from outside Amazon results in
```sh
docker run -it --network host --rm redis redis-cli -h redis.mufbi3.ng.0001.use1.cache.amazonaws.com -p 6379
Could not connect to Redis at redis.mufbi3.ng.0001.use1.cache.amazonaws.com:6379: No route to host
```

To connecto to Elasticache from the internet, you must use VPN.

## Connect to Elasticache Redis from EC2

```sh
sudo yum install docker
sudo systemctl start docker

sudo docker run -it --rm redis redis-cli -h redis.mufbi3.ng.0001.use1.cache.amazonaws.com -p 6379 ping
PONG
```

## Elasticache CloudFormation template

[CloudFormation Elasticache](../../18-cloud-formation/examples/elasticache.yaml)