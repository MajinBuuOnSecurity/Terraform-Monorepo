import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def get_public_load_balancer_arns_elbv2(region):
    try:
        elb_client = boto3.client('elbv2', region_name=region)
    except ClientError:  # Note: ClientError should maybe be caught below, as well
        print("shit, ClientError")

    try:
        load_balancers = elb_client.describe_load_balancers()
    except BotoCoreError:
        print("shit, BotoCoreError")

    public_elb_v2_arns = [
        lb['LoadBalancerArn']
        for lb in load_balancers['LoadBalancers']
        if lb.get('Scheme') == 'internet-facing'
    ]

    return public_elb_v2_arns


def _get_aws_account_id():
    # Initialize the Boto3 STS client
    sts_client = boto3.client('sts')

    # Retrieve account ID using GetCallerIdentity API
    response = sts_client.get_caller_identity()

    # Extract and return the account ID
    account_id = response['Account']
    return account_id


def get_public_load_balancer_arns_elbv1(region):
    try:
        elb_client = boto3.client('elb', region_name=region)
    except ClientError:  # Note: ClientError should maybe be caught below, as well
        print("shit, ClientError")

    try:
        load_balancers = elb_client.describe_load_balancers()
    except BotoCoreError:
        print("shit, BotoCoreError")

    public_load_balancer_names = [
        lb['LoadBalancerName']
        for lb in load_balancers['LoadBalancerDescriptions']
        if lb.get('Scheme') == 'internet-facing'
    ]

    public_elb_v1_arns = [
        f"arn:aws:elasticloadbalancing:{region}:{_get_aws_account_id()}:loadbalancer/{name}"
        for name in public_load_balancer_names
    ]

    return public_elb_v1_arns


def get_regions():
    return ["us-east-2"]
    # Deadcode
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    return [
        region['RegionName'] 
        for region in ec2_client.describe_regions()['Regions']
    ]

public_elb_arns = []
for region in get_regions():
    public_elb_arns += get_public_load_balancer_arns_elbv1(region)
    public_elb_arns += get_public_load_balancer_arns_elbv2(region)

output = {
    # Need to be a JSON string for Terraform to parse
    "public_elb_arns": json.dumps(public_elb_arns),
}

# Need to print JSON for Terraform to parse
print(json.dumps(output))
