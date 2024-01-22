import concurrent.futures

import boto3


def _get_available_regions(credentials):
    ec2_client = boto3.client(
        'ec2',
        region_name='us-east-1',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    regions = ec2_client.describe_regions()
    region_names = [region['RegionName'] for region in regions['Regions']]
    return region_names


def delete_default_vpc(region, ec2_resource, ec2_client, default_vpc_id):
    vpc = ec2_resource.Vpc(default_vpc_id)

    print(f"[In {region}] Deleting gateways of VPC {default_vpc_id}")
    for gateway in vpc.internet_gateways.all():
        vpc.detach_internet_gateway(InternetGatewayId=gateway.id)
        gateway.delete()

    print(f"[In {region}] Deleting route tables associations of VPC {default_vpc_id}")
    for route_table in vpc.route_tables.all():
        for association in route_table.associations:
            if not association.main:
                association.delete()

    print(f"[In {region}] Deleting security groups of VPC {default_vpc_id}")
    for security_group in vpc.security_groups.all():
        if security_group.group_name != "default":
            security_group.delete()

    print(f"[In {region}] Deleting subnets and interfaces of VPC {default_vpc_id}")
    for subnet in vpc.subnets.all():
        for interface in subnet.network_interfaces.all():
            interface.delete()
        subnet.delete()

    print(f"[In {region}] Deleting default VPC {default_vpc_id}")
    ec2_client.delete_vpc(VpcId=default_vpc_id)



def find_default_vpc(ec2_client):
    vpc_response = ec2_client.describe_vpcs()
    for vpc in vpc_response["Vpcs"]:
        if vpc["IsDefault"] is True:
            return vpc["VpcId"]
    return None


def delete_all_default_vpcs(credentials):
    """
    Inspired by:
    - https://github.com/davidobrien1985/delete-aws-default-vpc/blob/master/delete-default-vpc.py
    - https://github.com/awslabs/aws-deployment-framework/blob/bcc100e215912fa3dbc2f64e3a9bb161d92f822f/src/lambda_codebase/account_processing/delete_default_vpc.py
    """
    futures = []
    THREADPOOL_MAX_WORKERS = 20
    sorted_regions = sorted(_get_available_regions(credentials))

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADPOOL_MAX_WORKERS) as executor:
        for region in sorted_regions:
            region_specific_ec2_client = boto3.client(
                "ec2",
                region_name=region,
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
            )
            region_specific_ec2_resource = boto3.resource(
                "ec2",
                region_name=region,
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
            )

            default_vpc_id = find_default_vpc(region_specific_ec2_client)
            if not default_vpc_id:
                print(f"[In {region}] No default VPC")
                continue

            futures.append(
                executor.submit(
                    delete_default_vpc,
                    region,
                    region_specific_ec2_resource,
                    region_specific_ec2_client,
                    default_vpc_id,
                )
            )

    concurrent.futures.wait(futures)
    print('Deleted all default VPCs')
