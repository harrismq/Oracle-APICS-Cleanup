# -*- coding: utf-8 -*-
"""
@author: harris.qureshi@oracle.com
"""

import requests
import Config
import json

authToken = ""

def getAPIDetails(apiid):
    """
    This function is used to get the API Details.
    :param apiid: is the unique ID for an API.
    :return: JSON object that contains the API Details.
    """
    
    header = {
    'Authorization': authToken,
     'cache-control': "no-cache"
    }
    url = Config.API_URL + "/" + apiid
    response = requests.request("GET", url, headers=header)
    json_obj = json.loads(response.text)
    return json_obj

def unpublishAPIPortal(apiid):
    """
    This function is used to unpublish the API from Developer Portal.
    :param apiid: is the unique ID for an API.
    """
    hdr = {
    'Content-Type': "application/json",
     'Authorization': authToken,
     'cache-control': "no-cache"
    }

    payload =  "{\"state\":\"UNPUBLISHED\"}"
    url = Config.API_URL + "/" + apiid + "/publication"
    requests.request("PUT", url, data=payload, headers=hdr)
    
def checkAPIDeployments(apiid):
    
    """
    This function is used to check if the API is deployed on any gateway
    and get the deployment details.
    :param apiid: is the unique ID for an API.
    :return: JSON object that contains the API deployment details.
    """
    
    header = {
    'Authorization': authToken,
     'cache-control': "no-cache"
     }
    url = Config.API_URL + "/" + apiid + "/deployments"
    response = requests.request("GET", url, headers=header)
    json_obj = json.loads(response.text)
    return json_obj
 
def undeployAPI(apiid, deployments):
    """
    This function is used to undeploy the API from API Gateways.
    :param apiid: is the unique ID for an API.
    :deployments: JSON object that contains the API deployment details.
    """
    url = Config.API_URL + "/" + apiid + "/deployments"
    hdr = {
    'Content-Type': "application/json",
     'Authorization': authToken,
     'cache-control': "no-cache"
    }
    
    for i in deployments.get("items"):
        gatewayid = i.get("gateway")["id"]
        payload = "{\"gatewayId\":\"" + gatewayid + "\",\"action\":\"UNDEPLOY\",\"description\":\"\"}"
        #print(payload)
        requests.request("POST", url, data=payload, headers=hdr)
        #print(response.text)

def checkAPIEntitlements(apiid):
    """
    This function is used to check if API got any Entitlememts.
    :param apiid: is the unique ID for an API.
    :return: JSON object that contains the collection of API entitlements.
    """
    
    header = {
    'Authorization': authToken,
     'cache-control': "no-cache"
     }
    url = Config.API_URL + "/" + apiid + "/entitlements"
    response = requests.request("GET", url, headers=header)
    json_obj = json.loads(response.text)
    return json_obj

def unpublishAPIEntitlement(apiid, entitlementid):
    """
    This function is used to unpublish the API Entitlement from 
    the Developers Portal.
    :param apiid: is the unique ID for an API.
    :param entitlementid: is the unique ID for an entitlement.
    """
    hdr = {
    'Content-Type': "application/json",
     'Authorization': authToken,
     'cache-control': "no-cache"
    }

    payload =  "{\"state\":\"UNPUBLISHED\"}"
    url = Config.API_URL + "/" + apiid + "/entitlements/" + entitlementid + "/publication"
    requests.request("PUT", url, data=payload, headers=hdr)

def deleteAPIEntitlements(apiid, entitlements):
    """
    This function is used to delete the API Entitlements.
    :param apiid: is the unique ID for an API.
    :entitlements: JSON object that contains the collection of API entitlements.
    """
    
    hdr = {
     'Authorization': authToken,
     'cache-control': "no-cache"
    }
    
    for i in entitlements["items"]:
        entitlementid = i["id"]
        url = Config.API_URL + "/" + apiid + "/entitlements/" + entitlementid
        if i["publication"].get("state") == Config.PUBLICATION_STATE_PUBLISHED:
            unpublishAPIEntitlement(apiid,entitlementid )
        requests.request("DELETE", url, headers=hdr)
    
def deleteAPI(apiid):
    """
    This function is used to delete the API.
    :param apiid: is the unique ID for an API.
    """
    
    hdr = {
     'Authorization': authToken,
     'cache-control': "no-cache"
    }
    url = Config.API_URL + "/" + apiid
    requests.request("DELETE", url, headers=hdr)
    
def getAPIList():
    """
    This function is used to get the list of API's starting with 
    the value stored in the Config file variable API_Name_Identifier.
    :return: List of APIs.
    """

    url = Config.API_URL
    #print(authToken)

    headers = {
            'Authorization': authToken,
            'cache-control': "no-cache"
            }
    response = requests.request("GET", url, headers=headers)

    resp = json.loads(response.text)

    #print(resp)
    apilist = []

    for i in resp["items"]:
        if i["name"].startswith(Config.API_Name_Identifier):
            #print (i["name"] + " " + i["id"])
            apilist.append(i["id"])
            print(apilist)
    return apilist

def deleteAPIList():
    """
    This is the main function used to delete the API List.
    """
    apilist = getAPIList()
    
    for apiid in apilist:
        apidetail = getAPIDetails(apiid)

        if apidetail["publication"].get("state") == Config.PUBLICATION_STATE_PUBLISHED:
            unpublishAPIPortal(apiid)
    
        deployment = checkAPIDeployments(apiid)

        if deployment.get("count") > 0:
            undeployAPI(apiid,deployment)
            #print("tested")

        entitlement = checkAPIEntitlements(apiid)
        
        if entitlement.get("count") > 0:
            deleteAPIEntitlements(apiid,entitlement)

        deleteAPI(apiid)
   
        print("APIID : %s has been deleted." % (apiid))
        
   

if __name__ == "__main__":
    
    authToken = "Bearer " + Config.IDCS_Access_Token
    deleteAPIList()