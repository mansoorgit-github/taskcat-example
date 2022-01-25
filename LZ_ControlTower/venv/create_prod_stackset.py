import boto3
from datetime import date

def create_prod_stackset_vpc(networkOUid, tgwid):
    today = date.today()
    today=str(today)
    input("Press enter, if you have created KeyPair 'ctprodkey' in Prod :")

    with open('./vpc-with-tgw-attachment.yml', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('XXXXXXXXXXXX', tgwid)

    # Write the file out again
    with open('./vpc-with-tgw-attachment.yml', 'w') as file:
        file.write(filedata)

    bucket = "test-stack-set-for-prod-account-bucket"+today

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
    FILE_NAME = 'vpc-with-tgw-attachment.yml'
    OBJECT_NAME = 'vpc-with-tgw-attachment.yml'

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
        StackSetName='new-test-vpc-stackset'+today,
        Description='creating resource in prod account',
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
        StackSetName='new-test-vpc-stackset'+today,
        DeploymentTargets={
            'OrganizationalUnitIds': [
                networkOUid                                    #change
            ]
        },
        Regions=[
            my_region,
        ],
    )

'''def get_transit_gatewayid():
    client = boto3.client('ram')

    response = client.list_resources(
        resourceOwner='OTHER-ACCOUNTS',
        resourceRegionScope='ALL'
    )
    print(response)'''