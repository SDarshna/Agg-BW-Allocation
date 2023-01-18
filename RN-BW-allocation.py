#!/usr/bin/env python3

import prisma_sase
import io
import requests
import json
import os
import argparse
import yaml
import termtables as tt

agg_bw_url = "https://api.sase.paloaltonetworks.com/sse/config/v1/bandwidth-allocations"

def sdk_login_to_controller(filepath):
    with open(filepath) as f:
        client_secret_dict = yaml.safe_load(f)
        client_id = client_secret_dict["client_id"]
        client_secret = client_secret_dict["client_secret"]
        tsg_id_str = client_secret_dict["scope"]
        tsg = tsg_id_str.split(":")[1]
        #print(client_id, client_secret, tsg)

    global sdk 
    sdk = prisma_sase.API(controller="https://sase.paloaltonetworks.com/", ssl_verify=False)
   
    sdk.interactive.login_secret(client_id, client_secret, tsg)
    print("--------------------------------")
    print("Script Execution Progress: ")
    print("--------------------------------")
    print("Login to TSG ID {} successful".format(tsg))

def set_agg_bw(agg_bw_reg_name, agg_bw):
    payload = {
        "name":agg_bw_reg_name,
        "allocated_bandwidth":agg_bw,
        
    }
    sdk_resp = sdk.rest_call(url=agg_bw_url, data=payload, method="POST")  
    resp = sdk_resp.json()
    try:
        reg_name = resp["name"]
    except:
        print("BW Allocation not successful")
        exit(0)
    #print(resp)

    print("BW Allocation Successful")
    Header = ["Agg BW Region", "BW Allocated", "SPN Node"]
    RList = []
   
    RList.append([resp["name"],resp["allocated_bandwidth"],resp["spn_name_list"][0]])
    
   

    table_string = tt.to_string(RList, Header, style=tt.styles.ascii_thin_double)
    print(table_string)


   



def go():
    parser = argparse.ArgumentParser(description='Onboarding the LocalUsers, Service Connection and Security Rules.')
    parser.add_argument('-t1', '--T1Secret', help='Input secret file in .yml format for the tenant(T1) from which the security rules have to be replicated.')
    parser.add_argument('-Regname', '--aggBWRegionName', help='name of the aggregated bandwidth region')  
    parser.add_argument('-bw', '--AggBWAlloc', help='Input the total agg BW in Mbps to be configured in that agg BW region')
     
    args = parser.parse_args()
    T1_secret_filepath = args.T1Secret
    agg_bw_region_name = args.aggBWRegionName
    agg_bw = args.AggBWAlloc

    #Pass the secret of 'from tenant' to login
    sdk_login_to_controller(T1_secret_filepath)

    #Update the Region with BW
    set_agg_bw(agg_bw_region_name, agg_bw)







if __name__ == "__main__":
    go()