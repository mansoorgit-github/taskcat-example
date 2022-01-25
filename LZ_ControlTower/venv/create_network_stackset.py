import boto3
from datetime import date
import time
import json
import subprocess

def create_network_stackset_for_tgw(networkOUid, rootOUuserID):
    today = date.today()
    today=str(today)

    networkOUid = str(networkOUid)

    rootOrgID = input("\n Enter Organization ID from ( Organization -> Settings ) : ")
    rootOrgID = str(rootOrgID)

    with open('./tg-rt.yaml', 'r') as file:
        filedata = file.read()

    # Replace the target string


    filedata = filedata.replace('XXXXXXXXXXXX', rootOUuserID)
    filedata = filedata.replace('ZZZZZZZZZZZZ', rootOrgID)

    # Write the file out again
    with open('./tg-rt.yaml', 'w') as file:
        file.write(filedata)

    bucket = "new-stack-set-for-tgw-bucket-1"+today

    client = boto3.client('s3')
    try:
        response = client.create_bucket(
            ACL='public-read',
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-northeast-1'
            }
        )
    except Exception as e:
        print("Error:", e)

    print("\n bucket created")

    BUCKET_NAME = bucket
    FILE_NAME = 'tg-rt.yaml'
    OBJECT_NAME = 'tg-rt.yaml'

    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            FILE_NAME, BUCKET_NAME, OBJECT_NAME,
            ExtraArgs={'ACL': 'public-read'}
        )
    except Exception as e:
        print("Error:", e)

    print("\n Object uploaded")

    my_session = boto3.session.Session()
    my_region = my_session.region_name

    URL = 'https://'+BUCKET_NAME+'.s3.'+my_region+'.amazonaws.com/'+OBJECT_NAME
    print(URL)

    client = boto3.client('cloudformation')
    response = client.create_stack_set(
        StackSetName='mynew-network-resources-tgw-creation-5'+today,
        Description='creating resource in network account',
        #TemplateBody= URL,
        TemplateURL=URL,
        Capabilities=[
            'CAPABILITY_AUTO_EXPAND',
        ],
        PermissionModel='SERVICE_MANAGED',
        AutoDeployment={
            'Enabled': True,
            'RetainStacksOnAccountRemoval': False
        },
    )

    response = client.create_stack_instances(
        StackSetName='mynew-network-resources-tgw-creation-5'+today,
        DeploymentTargets={
            'OrganizationalUnitIds': [networkOUid]
        },
        Regions=[
            my_region,
        ],
    )



def create_network_stackset_for_nfw(networkOUid):
    today = date.today()
    today=str(today)
    bucket = "new-stack-set-for-nfw-bucket-"+today

    client = boto3.client('s3')
    try:
        response = client.create_bucket(
            ACL='public-read',
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-northeast-1'
            }
        )
    except Exception as e:
        print("Error:", e)

    print("\n bucket created")

    BUCKET_NAME = bucket
    FILE_NAME = 'nf-tg.yaml'
    OBJECT_NAME = 'nf-tg.yaml'

    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            FILE_NAME, BUCKET_NAME, OBJECT_NAME,
            ExtraArgs={'ACL': 'public-read'}
        )
    except Exception as e:
        print("Error:", e)

    print("\n Object uploaded")

    my_session = boto3.session.Session()
    my_region = my_session.region_name

    URL = 'https://'+BUCKET_NAME+'.s3.'+my_region+'.amazonaws.com/'+OBJECT_NAME
    print(URL)

    client = boto3.client('cloudformation')
    response = client.create_stack_set(
        StackSetName='mynew-network-resources-nfw-creation'+today,
        Description='creating resource in network account',
        #TemplateBody= URL,
        TemplateURL=URL,
        Capabilities=[
            'CAPABILITY_AUTO_EXPAND',
        ],
        PermissionModel='SERVICE_MANAGED',
        AutoDeployment={
            'Enabled': True,
            'RetainStacksOnAccountRemoval': False
        },
    )

    response = client.create_stack_instances(
        StackSetName='mynew-network-resources-nfw-creation'+today,
        DeploymentTargets={
            'OrganizationalUnitIds': [
                networkOUid                                #change
            ]
        },
        Regions=[
            my_region,
        ],
    )



def create_root_account_role_policy():
    client = boto3.client('iam')

    file = open('./root_account_role.json')
    data = json.load(file)
    roleStatement = json.dumps(data)

    # create role
    response = client.create_role(
        RoleName='AWSCloudFormationStackSetAdministrationRole',
        AssumeRolePolicyDocument=roleStatement,
        Description='Root Account Access Role',
    )
    RoleName = response['Role']['RoleName']

    file = open('./root_account_policy.json')
    data = json.load(file)
    policyStatement = json.dumps(data)

    # create policy
    response = client.create_policy(
        PolicyName='AssumeRole-AWSCloudFormationStackSetExecutionRole',
        PolicyDocument=policyStatement,
        Description='Root Account Access Policy'
    )
    policyArn = response['Policy']['Arn']
    print("\n Attaching policy to role")

    response = client.attach_role_policy(
        RoleName=RoleName,
        PolicyArn=policyArn
    )
    print("Sucess")

    response = client.attach_user_policy(
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess',
        UserName='control-tower',
    )

def create_network_account_policy_attachment(networkOUid,rootOUuserID):
    today = date.today()
    today = str(today)

    with open('./AWSCloudFormationStackSetExecutionRole.yml', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('XXXXXXXXXXXX', rootOUuserID)

    # Write the file out again
    with open('./AWSCloudFormationStackSetExecutionRole.yml', 'w') as file:
        file.write(filedata)

    bucket = "stack-set-for-network-account-policy-bucket" + today
    client = boto3.client('s3')
    try:
        response = client.create_bucket(
            ACL='public-read',
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-northeast-1'
            }
        )
    except Exception as e:
        print("Error:", e)

    print("\n bucket created")

    BUCKET_NAME = bucket
    FILE_NAME = 'AWSCloudFormationStackSetExecutionRole.yml'
    OBJECT_NAME = 'AWSCloudFormationStackSetExecutionRole.yml'

    s3 = boto3.client("s3")
    try:
        s3.upload_file(
            FILE_NAME, BUCKET_NAME, OBJECT_NAME,
            ExtraArgs={'ACL': 'public-read'}
        )
    except Exception as e:
        print("Error:", e)

    print("\n Object uploaded")

    my_session = boto3.session.Session()
    my_region = my_session.region_name

    URL = 'https://' + BUCKET_NAME + '.s3.' + my_region + '.amazonaws.com/' + OBJECT_NAME
    print(URL)

    # create stack set
    client = boto3.client('cloudformation')
    response = client.create_stack_set(
        StackSetName='network-account-policy-attachment-001' + today,
        Description='creating role and policy in network account',
        # TemplateBody= URL,
        TemplateURL=URL,
        Capabilities=[
            'CAPABILITY_NAMED_IAM',
        ],
        PermissionModel='SERVICE_MANAGED',
        AutoDeployment={
            'Enabled': True,
            'RetainStacksOnAccountRemoval': False
        },
    )

    response = client.create_stack_instances(
        StackSetName='network-account-policy-attachment-001' + today,
        DeploymentTargets={
            'OrganizationalUnitIds': [
                'ou-972v-tbtyaw7f'  # change
            ]
        },
        Regions=[
            my_region,
        ],
    )


def create_tgw_sts_assume_role(rootOUuserID):
    boto_sts = boto3.client('sts')
    rootOUuserID = str(rootOUuserID)

    roleArn = str('aws:arn:iam::'+rootOUuserID+':role/AWSCloudFormationStackSetAdministrationRole')
    stsresponse = boto_sts.assume_role(
        RoleArn=roleArn,
        RoleSessionName='tgw-new-session'
    )

    newsession_id = stsresponse["Credentials"]["AccessKeyId"]
    newsession_key = stsresponse["Credentials"]["SecretAccessKey"]
    newsession_token = stsresponse["Credentials"]["SessionToken"]

    my_session = boto3.session.Session()
    my_region = my_session.region_name

    s3_assumed_client = boto3.client(
        's3',
        region_name=my_region,
        aws_access_key_id=newsession_id,
        aws_secret_access_key=newsession_key,
        aws_session_token=newsession_token
    )

    response = s3_assumed_client.list_buckets()
    print(response)

