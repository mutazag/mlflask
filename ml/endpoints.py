import os 
import urllib.request
import json

def getDeployments(endpointName='maggpt2'):

    tenantid = os.environ['tenantid']
    client_id = os.environ['clientid']
    client_secret = os.environ['clientsecret']

    url = f"https://login.microsoftonline.com/{tenantid}/oauth2/token"

    payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&resource=https%3A%2F%2Fmanagement.azure.com'
    print(payload.encode('utf-8'))
    req = urllib.request.Request(url, payload.encode('utf-8'))
    response = urllib.request.urlopen(req)
    result = response.read()
    token = json.loads(result.decode('utf-8'))['access_token']

    # online deployment
    subscriptionId = os.environ['subscriptionId']
    resourceGroupName = os.environ['resourceGroupName']
    workspaceName = os.environ['workspaceName']
    # endpointName = os.environ['endpointName']

    depurl = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/onlineEndpoints/{endpointName}/deployments?api-version=2023-04-01-preview'

    headers = {
        'Content-Type':'application/json',
        'Authorization':('Bearer '+ token),
        'api-version':'2023-04-01-preview'
    }

    req = urllib.request.Request(depurl, None, headers)
    response = urllib.request.urlopen(req)
    result = response.read()
    deployments = json.loads(result.decode('utf-8'))
    dep_names = [ deployment['name'] for deployment in deployments['value']]
    return dep_names