import boto3
import time
import json

def create_network_org_unit(rootOUid):
    ou_name = "Network OU"
    parentID = str(rootOUid)
    client = boto3.client('organizations')                       # create organisation
    response = client.create_organizational_unit(
        ParentId=parentID,                                       # root OU ID
        Name=ou_name,
        Tags=[
            {
                'Key': ou_name,
                'Value': 'ou'
            },
        ]
    )
    OUid = response['OrganizationalUnit']['Id']
    print(OUid)

    time.sleep(1)
    '''print("Enabling SCP")
    response = client.enable_policy_type(                       # Enable SCP
        RootId=parentID,
        PolicyType='SERVICE_CONTROL_POLICY'
    )'''

    print("Creating Policy")
    name = str(ou_name + "_policy")
    file = open('./organization_policy.json')
    data = json.load(file)
    policyStatement = json.dumps(data)
    response = client.create_policy(                            # Create SCP policy
        Content= policyStatement,
        Description='List, Read and Tagging Policy for OU',
        Name= name,
        Type='SERVICE_CONTROL_POLICY',
        Tags=[
            {
                'Key': ou_name,
                'Value': 'ou_policy'
            },
        ]
    )
    policyID = response['Policy']['PolicySummary']['Id']
    print(policyID)
    time.sleep(1)

    print("Attaching Policy")
    response = client.attach_policy(
        PolicyId=policyID,
        TargetId=OUid
    )
    time.sleep(1)

    print("Sucess")
    mylist=[]
    mylist.append(OUid)
    mylist.append(policyID)
    return (mylist)


def create_prod_org_unit(rootOUid):
    ou_name = "Prod OU"
    parentID = str(rootOUid)
    client = boto3.client('organizations')                       # create organisation
    response = client.create_organizational_unit(
        ParentId=parentID,                                       # root OU ID
        Name=ou_name,
        Tags=[
            {
                'Key': ou_name,
                'Value': 'ou'
            },
        ]
    )
    OUid = response['OrganizationalUnit']['Id']
    print(OUid)

    time.sleep(1)
    '''print("Enabling SCP")
    response = client.enable_policy_type(                       # Enable SCP
        RootId=parentID,
        PolicyType='SERVICE_CONTROL_POLICY'
    )'''
    time.sleep(1)
    print("Creating Policy")
    name = str(ou_name + "_policy")
    file = open('./organization_policy.json')
    data = json.load(file)
    policyStatement = json.dumps(data)
    response = client.create_policy(                            # Create SCP policy
        Content= policyStatement,
        Description='List, Read and Tagging Policy for OU',
        Name= name,
        Type='SERVICE_CONTROL_POLICY',
        Tags=[
            {
                'Key': ou_name,
                'Value': 'ou_policy'
            },
        ]
    )
    policyID = response['Policy']['PolicySummary']['Id']
    print(policyID)

    print("Attaching Policy")
    response = client.attach_policy(
        PolicyId=policyID,
        TargetId=OUid
    )
    print("Sucess")
    mylist=[]
    mylist.append(OUid)
    mylist.append(policyID)
    return (mylist)


def create_nonprod_org_unit(rootOUid):
    ou_name = "NonProd OU"
    parentID = str(rootOUid)
    client = boto3.client('organizations')                       # create organisation
    response = client.create_organizational_unit(
        ParentId=parentID,                                       # root OU ID
        Name=ou_name,
        Tags=[
            {
                'Key': ou_name,
                'Value': 'ou'
            },
        ]
    )
    OUid = response['OrganizationalUnit']['Id']
    print(OUid)

    time.sleep(1)
    '''print("Enabling SCP")
    response = client.enable_policy_type(                       # Enable SCP
        RootId=parentID,
        PolicyType='SERVICE_CONTROL_POLICY'
    )'''
    time.sleep(1)
    print("Creating Policy")
    name = str(ou_name + "_policy")
    file = open('./organization_policy.json')
    data = json.load(file)
    policyStatement = json.dumps(data)
    response = client.create_policy(                            # Create SCP policy
        Content= policyStatement,
        Description='List, Read and Tagging Policy for OU',
        Name= name,
        Type='SERVICE_CONTROL_POLICY',
        Tags=[
            {
                'Key': ou_name,
                'Value': 'ou_policy'
            },
        ]
    )
    policyID = response['Policy']['PolicySummary']['Id']
    print(policyID)

    print("Attaching Policy")
    response = client.attach_policy(
        PolicyId=policyID,
        TargetId=OUid
    )
    print("Sucess")
    mylist=[]
    mylist.append(OUid)
    mylist.append(policyID)
    return (mylist)