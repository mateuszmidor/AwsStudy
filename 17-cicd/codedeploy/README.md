# Create CodeDeploy app, configure and run EC2 instance

## Service Roles

- EC2 IAM Role - you need to create a new role in IAM Console with "AmazonS3ReadOnlyAccess" policy attached. Then specify this role when launching EC2
  - this is for CodeDeploy Agent running on that EC2 to pull code from S3 or CodeCommit
- CodeDeploy Service Role - you need to create new role in IAM Console with "AWSCodeDeployRole" policy attached. Then specify this role when creating new Deployment Group
  - this is to manage autoscaling, loadbalancers, cloud watch etc needed for deployed application

## Agent installation on EC2

EC2 User Data:

```sh
#!/usr/bin/env bash
yum update -y
yum install -y ruby
wget https://aws-codedeploy-eu-west-3.s3.eu-west-3.amazonaws.com/latest/install
chmod +x ./install
./install auto
systemctl status codedeploy-agent
```

## Troubleshooting

### Application Lifecycle Logs

On EC2 instance: `/opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log`

### CodeDeploy Agent

- agent service status: `systemctl status codedeploy-agent`
- agent service logs: `journalctl -u codedeploy-agent`