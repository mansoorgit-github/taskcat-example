import boto3
from datetime import date

def cloudformation_customize_ct():
    today = date.today()
    today = str(today)
    bucket = "stack-for-ct-customization"+today

    email = input("\n Please enter, Pipeline Approval Email Address :")
    email=str(email)

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
    FILE_NAME = 'custom-ct.template'
    OBJECT_NAME = 'custom-ct.template'

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

    name = 'CTcustomization'+today

    client = boto3.client('cloudformation')
    response = client.create_stack(
        StackName=name,
        TemplateURL=URL,
        TimeoutInMinutes=123,
        Parameters=[
            {
                'ParameterKey': 'PipelineApprovalEmail',
                'ParameterValue': email,
            },
        ],
        Capabilities=[
            'CAPABILITY_NAMED_IAM',
        ],
        OnFailure='ROLLBACK',
        Tags=[
            {
                'Key': 'Control_Tower',
                'Value': 'CT_customization'
            },
        ],
    )
