# Oracle APICS Cleanup
Python program to use the Oracle API Platfor Cloud Service API.
This is written using Rest APIs : https://docs.oracle.com/en/cloud/paas/api-platform-cloud/apfrm/rest-endpoints.html 
It allows you to delete APIs and Plans in your Oracle API Platform Cloud Service environment. 
You can provide an exact name of the API or Plan or just the starting letters and it will delete all APIs and Plans starting from those letters.

To learn more about the dependancies that needs to be handled before you can delete an API or a Plan and it's workflow, please refer to this article.

https://www.linkedin.com/pulse/how-cleanup-oracle-apics-environment-harris-qureshi/

## Dependencies
This was written using Python 3.
It requires Python requests and json libraries installed.

## Usage

You can use this code to bulk delete APIs and Plans in Oracle API Platform Cloud Service.

Before you can execute the cleanupAPI.py or cleanupPlan.py, you need to setup following attributes in the Config.py file.

**IDCS_Access_Token** : This is the IDCS Access Token, you can download it from the IDCS instance associated to your APICS instance. Or you may ask your Admin to provide this to you. You can find details in the following link on how to get this token.

https://docs.oracle.com/en/cloud/paas/api-platform-cloud/apfrp/Authentication.html

Only copy the value of app_access_token attribute here. This token should be of the user who has Admin priviledges of APICS.
*Note: Access token normally expires in 60 minutes, once it's expired you will need to update this again with the new access token.*

**API_URL** ="https://<example.com>/apiplatform/management/v1/apis"

**PLAN_URL** ="https://<example.com>/apiplatform/management/v1/plans"

Replace <example.com> from API_URL and PLAN_URL attribute with your API instance base url. For example.

API_URL=https://api01-gse.apiplatform.ocp.oraclecloud.com/apiplatform/management/v1/apis

PLAN_URL=https://api01-gse.apiplatform.ocp.oraclecloud.com/apiplatform/management/v1/plans

**API_Name_Identifier** ="Org"

Update the value of API_Name with the api name that you wish to delete. In this example it will delete all APIs starting with Org.

**PLAN_Name_Identifier** ="Org"

Update the value of PLAN_Name with the plan name that you wish to delete. In this example it will delete all Plans starting with Org.

## Delete APIs

Once you have setup the attributes in the Config file. You can run cleanupAPIs.py either from your preferred ide or directly from terminal.

``` python cleanupAPIs.py ```

## Delete Plans

Once you have setup the attributes in the Config file. You can run cleanupPlans.py either from your preferred ide or directly from terminal.

``` python cleanupAPIs.py ```
