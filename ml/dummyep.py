import urllib.request
import json
import os
import ssl

def ml_endpoint(textinput, deployment):
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data = {'data': textinput}

    # body = str.encode(json.dumps(data))
    body = str.encode(textinput)

    # dummyepurl
    url = os.environ['dummyepurl']
    # dummyepkey
    api_key = os.environ['dummyepkey']

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {
        'Content-Type':'application/json',
        'Authorization':('Bearer '+ api_key)}
    if deployment != 'none':
        headers['azureml-model-deployment'] = deployment

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        depslot = response.headers['azureml-model-deployment']

        return({'response': result, 'deployment': depslot})
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return(error.code)