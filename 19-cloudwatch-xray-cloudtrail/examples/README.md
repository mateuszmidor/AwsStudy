# CloudWatch

## Run Unified Agent on EC2 - for memory usage & logs forwarding

1. attach `CloudWatchAgentServerPolicy` IAM Policy to EC2 Instance Profile's Role

1. ssh to your EC2 instance

1. download
    ```sh
    wget https://s3.us-east-1.amazonaws.com/amazoncloudwatch-agent-us-east-1/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
    ```

1. install
    ```sh
    sudo rpm -U ./amazon-cloudwatch-agent.rpm
    ```

1. create Unified Agent [config file](./unified_agent_config.json) at `/opt/aws/amazon-cloudwatch-agent/bin/config.json`, or run config wizard:
    ```sh
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
    ```

1. run Unified Agent
    ```sh
        sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
    ```

1. new metrics should show up under NameSpace `CWAgent` and logs under log_group_name configured in [config file](./unified_agent_config.json)