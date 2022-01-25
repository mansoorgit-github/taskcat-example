import boto3
import json
import csv

def create_network_account(Acc_email,Acc_name, OUid, rootOUid, rootOUuserID):
    print("\n Creating Role and Policy")
    RoleName=attach_child_account_policy(Acc_name, rootOUuserID)
    client = boto3.client('organizations')
    response = client.create_account(
        Email=Acc_email,
        AccountName=Acc_name,
        RoleName=RoleName,
        IamUserAccessToBilling='DENY',
        Tags=[
            {
                'Key': Acc_name,
                'Value': 'NW Account'
            },
        ]
    )
    acctStatusID = response['CreateAccountStatus']['Id']

    while True:
        createStatus = client.describe_create_account_status(
            CreateAccountRequestId=acctStatusID
        )
        print("\n creation in progress .... ")
        if str(createStatus['CreateAccountStatus']['State']) != 'IN_PROGRESS':
            newAccountId = str(createStatus['CreateAccountStatus']['AccountId'])
            break

    moveResponse = client.move_account(
        AccountId=newAccountId,
        SourceParentId=rootOUid,
        DestinationParentId=OUid
    )
    print("\n Sucessfully Created Network Account")

    print("\n Attaching Policy")
    newAccountId=str(newAccountId)
    # attach_child_account_policy(Acc_name, rootOUuserID)



def create_prod_account(Acc_email,Acc_name, OUid, rootOUid):
    client = boto3.client('organizations')
    response = client.create_account(
        Email=Acc_email,
        AccountName=Acc_name,
        RoleName='OrganizationAccountAccessRole',
        IamUserAccessToBilling='DENY',
        Tags=[
            {
                'Key': Acc_name,
                'Value': 'Prod Account'
            },
        ]
    )
    acctStatusID = response['CreateAccountStatus']['Id']

    while True:
        createStatus = client.describe_create_account_status(
            CreateAccountRequestId=acctStatusID
        )
        print("\n creation in progress ....")
        if str(createStatus['CreateAccountStatus']['State']) != 'IN_PROGRESS':
            newAccountId = str(createStatus['CreateAccountStatus']['AccountId'])
            break

    moveResponse = client.move_account(
        AccountId=newAccountId,
        SourceParentId=rootOUid,
        DestinationParentId=OUid
    )
    print("Sucessfully Created Prod Account")


def create_prod_account(Acc_email,Acc_name, OUid, rootOUid):
    client = boto3.client('organizations')
    response = client.create_account(
        Email=Acc_email,
        AccountName=Acc_name,
        RoleName='OrganizationAccountAccessRole',
        IamUserAccessToBilling='DENY',
        Tags=[
            {
                'Key': Acc_name,
                'Value': 'NonProd Account'
            },
        ]
    )
    acctStatusID = response['CreateAccountStatus']['Id']

    while True:
        createStatus = client.describe_create_account_status(
            CreateAccountRequestId=acctStatusID
        )
        print("\n creation in progress ....")
        if str(createStatus['CreateAccountStatus']['State']) != 'IN_PROGRESS':
            newAccountId = str(createStatus['CreateAccountStatus']['AccountId'])
            break

    moveResponse = client.move_account(
        AccountId=newAccountId,
        SourceParentId=rootOUid,
        DestinationParentId=OUid
    )
    print("Sucessfully Created Non Prod Account")


def inviteAccount():
    with open('invite_account.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    print(data)

    for i in data:
        client = boto3.client('organizations')
        id = str(i[0])
        print(id)
        response = client.invite_account_to_organization(
            Target={
                'Id': id,
                'Type': 'EMAIL'
            }
        )
        print(response)
        msg = id + ' is invited '
        print(msg)

def attach_child_account_policy(Acc_name, rootOUuserID):
    client = boto3.client('iam')                                     # iam client
    with open('./child_account_role.json', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('XXXXXXXXXXXX', rootOUuserID)

    # Write the file out again
    with open('./child_account_role.json', 'w') as file:
        file.write(filedata)

    file = open('./child_account_role.json')
    data = json.load(file)
    roleStatement = json.dumps(data)

    # create role
    response = client.create_role(
        RoleName='Role'+Acc_name,
        AssumeRolePolicyDocument=roleStatement,
        Description='Cross Account Access Role',
    )
    RoleName = response['Role']['RoleName']

    file = open('./child_account_policy.json')
    data = json.load(file)
    policyStatement = json.dumps(data)

    # create policy
    response = client.create_policy(
        PolicyName='Policy'+Acc_name,
        PolicyDocument=policyStatement,
        Description='Cross Account Access Policy'
    )
    policyArn = response['Policy']['Arn']
    print("\n Attaching policy to role")

    response = client.attach_role_policy(
        RoleName=RoleName,
        PolicyArn=policyArn
    )

    with open('./child_account_role.json', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(rootOUuserID, 'XXXXXXXXXXXX')

    # Write the file out again
    with open('./child_account_role.json', 'w') as file:
        file.write(filedata)

    RoleName=str(RoleName)
    return RoleName