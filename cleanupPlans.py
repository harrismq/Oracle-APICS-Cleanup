# -*- coding: utf-8 -*-
"""
@author: harris.qureshi@oracle.com
"""

import Config
import requests
import json

authToken = ""

def getPlanDetails(planid):
    """
    This function is used to get the Plan Details.
    :param planid: is the unique ID for a Plan.
    :return: JSON object that contains the Plan Details.
    """    
    header = {
    'Authorization': authToken,
     'cache-control': "no-cache"
    }
    url = Config.PLAN_URL + "/" + planid
    response = requests.request("GET", url, headers=header)
    json_obj = json.loads(response.text)
    return json_obj

def getPlanList():
    """
    This function is used to get the list of Plans starting with 
    the value stored in the Config file variable PLAN_Name_Identifier.
    :return: List of Plans.
    """    
    url = Config.PLAN_URL

    headers = {
            'Authorization': authToken,
            'cache-control': "no-cache"
            }
    response = requests.request("GET", url, headers=headers)

    resp = json.loads(response.text)

#print(resp["items"])
    planlist = []

    for i in resp["items"]:
        if i["name"].startswith(Config.PLAN_Name_Identifier):
            #print (i["name"] + " " + i["id"])
            planlist.append(i["id"])
            #print(planlist)
    return planlist

def unpublishPLANPortal(planid):
    """
    This function is used to unpublish the Plan from Developer Portal.
    :param planid: is the unique ID for a Plan.
    """
    
    hdr = {
    'Content-Type': "application/json",
     'Authorization': authToken,
     'cache-control': "no-cache"
    }

    payload =  "{\"state\":\"UNPUBLISHED\"}"
    url = Config.PLAN_URL + "/" + planid + "/publication"
    #print(url)
    requests.request("PUT", url, data=payload, headers=hdr)
    #print(response.text)
    
def checkPlanSubscriptions(planid):
    """
    This function is used to check if the Plan has any Application 
    subscriptions.
    :param planid: is the unique ID for a Plan.
    :return: JSON object that contains the collection of Plan Subscriptions.
    """
    
    header = {
    'Authorization': authToken,
     'cache-control': "no-cache"
     }
    url = Config.PLAN_URL + "/" + planid + "/subscriptions"
    response = requests.request("GET", url, headers=header)
    json_obj = json.loads(response.text)
    return json_obj
 
def unsubscribePlanSubscription(planid,subscriptionid):
    """
    This function is used to unscubscribe appplications from the Plan.
    :param planid: is the unique ID for a Plan.
    :param subscriptionid: is the unique ID for a subscription.
    """
    hdr = {
    'Content-Type': "application/json",
     'Authorization': authToken,
     'cache-control': "no-cache"
    }

    payload =  "{\"state\":\"UNSUBSCRIBED\"}"
    url = Config.PLAN_URL + "/" + planid + "/subscriptions/" + subscriptionid + "/state"
    requests.request("PUT", url, data=payload, headers=hdr)
    
 
def deletePlanSubscriptions(planid, subscriptions):
    """
    This function is used to delete the Plan Subscriptions.
    :param planid: is the unique ID for a Plan.
    :param subscriptions: JSON object that contains the collection of Plan 
    Subscriptions.
    """
    hdr = {
     'Authorization': authToken,
     'cache-control': "no-cache"
    }
    
    for i in subscriptions["items"]:
        subscriptionid = i["id"]
        state = i["state"]
        url = Config.PLAN_URL + "/" + planid + "/subscriptions/" + subscriptionid
        print ("subscriptionid : %s and its state is %s " % (subscriptionid,state))
        if state == Config.SUBSCRIPTION_STATE_SUBSCRIBED:
            unsubscribePlanSubscription(planid,subscriptionid )
        requests.request("DELETE", url, headers=hdr)

def checkPlanEntitlements(planid):
    """
    This function is used to check if Plan got any Entitlememts.
    :param planid: is the unique ID for a Plan.
    :return: JSON object that contains the collection of Plan entitlements.
    """    
    
    header = {
    'Authorization': authToken,
     'cache-control': "no-cache"
     }
    url = Config.PLAN_URL + "/" + planid + "/entitlements"
    response = requests.request("GET", url, headers=header)
    json_obj = json.loads(response.text)
    return json_obj

def unpublishPlanEntitlement(planid,entitlementid):
    """
    This function is used to unpublish the Plan Entitlement from 
    the Developers Portal.
    :param planid: is the unique ID for an Plan.
    :param entitlementid: is the unique ID for an entitlement.
    """
    
    hdr = {
    'Content-Type': "application/json",
     'Authorization': authToken,
     'cache-control': "no-cache"
    }

    payload =  "{\"state\":\"UNPUBLISHED\"}"
    url = Config.PLAN_URL + "/" + planid + "/entitlements/" + entitlementid + "/publication"
    requests.request("PUT", url, data=payload, headers=hdr)

def deletePlanEntitlements(planid, entitlements):
    """
    This function is used to delete the Plan Entitlements.
    :param planid: is the unique ID for an Plan.
    :entitlements: JSON object that contains the collection of Plan 
    entitlements.
    """
    
    hdr = {
     'Authorization': authToken,
     'cache-control': "no-cache"
    }
    
    for i in entitlements["items"]:
        entitlementid = i["id"]
        url = Config.PLAN_URL + "/" + planid + "/entitlements/" + entitlementid
        state = i["publication"].get("state")
        print("planid is %s and entitlementid is %s and subscription state is %s" % (planid,entitlementid,state))
        if i["publication"].get("state") == Config.PUBLICATION_STATE_PUBLISHED:
            unpublishPlanEntitlement(planid,entitlementid )
        requests.request("DELETE", url, headers=hdr)
        
def deletePlan(planid):
    """
    This function is used to delete the Plan.
    :param planid: is the unique ID for an Plan.
    """
    
    hdr = {
     'Authorization': authToken,
     'cache-control': "no-cache"
    }
    url = Config.PLAN_URL + "/" + planid
    requests.request("DELETE", url, headers=hdr)

def deletePlanList():
    """
    This is the main function used to delete the Plan List.
    """    
    planlist = getPlanList()
    
    plandetail = []
    
    for planid in planlist:
            plandetail = getPlanDetails(planid)
            
            if plandetail["publication"].get("state") == Config.PUBLICATION_STATE_PUBLISHED:
                unpublishPLANPortal(planid)
                print("Published state planid : " + planid)
                
            subsc = checkPlanSubscriptions(planid)
            
            if subsc.get("count") > 0:
                deletePlanSubscriptions(planid,subsc)
                #print("tested")
                
            entitlement = checkPlanEntitlements(planid)
            
            if entitlement.get("count") > 0:
                deletePlanEntitlements(planid,entitlement)
                
            deletePlan(planid)
                
            print("Deleted PlanId : " + planid)
            
if __name__=="__main__":
    
    authToken = "Bearer " + Config.IDCS_Access_Token
    deletePlanList()








