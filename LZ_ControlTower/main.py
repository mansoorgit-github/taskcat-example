import create_ou
import time
import create_account
import create_network_stackset
import create_prod_stackset
import create_nonprod_stackset
import batch_account_creation
import customize_control_tower
import os
'''
print("Configuring Control Tower - Boto3")
rootOUid = input("\n Enter root OU ID :")
rootOUid = str(rootOUid)

rootOUuserID = input("\n Enter root account ID no. :")
rootOUuserID = str(rootOUuserID)

# create OU's
ouDetails1=create_ou.create_network_org_unit(rootOUid)                 # Network OU

print("Creating Prod OU")
ouDetails2=create_ou.create_prod_org_unit(rootOUid)                    # Prod OU

print("Creating Non Prod OU")
ouDetails3=create_ou.create_nonprod_org_unit(rootOUid)                 # Non Prod OU

# create accounts
print("\n Please Enter Details for Network Account ")
Acc_name=input("\n Enter Account Name: ")
Acc_email=input("\n Enter Email: ")

Acc_name=str(Acc_name)
Acc_email=str(Acc_email)

create_account.create_network_account(Acc_email,Acc_name, ouDetails1[0], rootOUid, rootOUuserID)
input("\n Please Register Your OU's & Account and Press Enter")

print("\n Please Enter Details for Prod Account ")
Acc_name=input("\n Enter Account Name: ")
Acc_email=input("\n Enter Email: ")

Acc_name=str(Acc_name)
Acc_email=str(Acc_email)
create_account.create_prod_account(Acc_email,Acc_name, ouDetails2[0], rootOUid)

print("\n Please Enter Details for NonProd Account ")
Acc_name=input("\n Enter Account Name: ")
Acc_email=input("\n Enter Email: ")

Acc_name=str(Acc_name)
Acc_email=str(Acc_email)
create_account.create_prod_account(Acc_email,Acc_name, ouDetails3[0],rootOUid)
input("\n Please Register Your OU's & Account and Press Enter")


input("\n Press enter to create resource in Network Account:")
# create_network_stackset.create_root_account_role_policy()
# create_network_stackset.create_network_account_policy_attachment(ouDetails1[0],rootOUuserID)
create_network_stackset.create_network_stackset_for_tgw(ouDetails1[0], rootOUuserID)  # create TGW            ouDetails1[0]
# create_network_stackset.create_tgw_sts_assume_role(rootOUuserID)

print("\n Successfully created TGW in network account ...")

tgwID=input("\n Enter Transit Gateway ID from Network Account :")
input("\n Press enter to create VPC in Prod Account:")


create_prod_stackset.create_prod_stackset_vpc(ouDetails2[0], tgwID)   # parameter to be changed
print("\n successfully created VPC in Prod account ...")
input("\n Press enter to create VPC in Non Prod Account:")

create_nonprod_stackset.create_nonprod_stackset_vpc(ouDetails3[0], tgwID)  # parameter to be changed
print("\n successfully created VPC in Non Prod account ...")

# Batch Account Creation
userinput = input("\n Do you want to Start Batch Account Creation :")
if( userinput=='Yes' or userinput=='yes' or userinput=='y' or userinput =='Y' ):
    batch_account_creation.batch_account_creation()
else:
    input("\n ok, Thanks!")'''

# Invite Existing Account
userinput = input("\n Do you want to invite Account Yes/No, make sure your account is verified :")
if( userinput=='Yes' or userinput=='yes' or userinput=='y' or userinput =='Y' ):
    create_account.inviteAccount()
else:
    input("\n ok, Press enter to set up infrastructure")


'''# Customize Control Tower
userinput = input("\n Do you want to Customize Control Tower :")
if( userinput=='Yes' or userinput=='yes' or userinput=='y' or userinput =='Y' ):
    customize_control_tower.cloudformation_customize_ct()
else:
    input("\n ok, Thanks!")'''

