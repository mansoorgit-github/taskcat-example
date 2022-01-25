import boto3
import json
import subprocess
import time

def batch_account_creation():
    client = boto3.client('servicecatalog')

    response = client.search_products(
        AcceptLanguage='en',
        Filters={
            'FullTextSearch': ['AWS Control Tower Account Factory']
        }
    )
    productID=response['ProductViewSummaries'][0]['ProductId']
    print(productID)

    response = client.describe_product(
        AcceptLanguage='en',
        Id=productID,
    )
    proArtifact=response['ProvisioningArtifacts'][0]['Id']
    print(proArtifact)

    noOfAccounts = input("How many accounts you want to provision : ")
    noOfAccounts = int(noOfAccounts)
    input("Fill the details in Account/prod_acc directory & Press Enter")

    for i in range(noOfAccounts):
        i = str(i)
        print("\n Provisioning "+i+" Account ...")
        filename = str('./Account/prod_acc_'+i+'.json')
        time.sleep(1)
        print("\n Reading ... " + filename)
        file = open(filename)
        data = json.load(file)

        response = client.provision_product(
            AcceptLanguage='en',
            ProductId=productID,
            ProvisioningArtifactId=proArtifact,
            ProvisionedProductName='mynew_CT_Catalog'+i,
            ProvisioningParameters=data
        )
        provProductID = response['RecordDetail']['ProvisionedProductId']
        print(provProductID)

        response = client.describe_provisioned_product(
            AcceptLanguage='en',
            Id=provProductID,
        )
        print("\n Each Account Provisioning Can take up to 10-15 min . . .")

        STATUS = response['ProvisionedProductDetail']['Status']
        print(STATUS)
        while True:
            if(STATUS=='AVAILABLE'):
                break
            print("\n Provisioning Account . . .")
            time.sleep(60)