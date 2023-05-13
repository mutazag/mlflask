import urllib.request
import json
import os
import ssl

def gpt2(textinput, deployment):
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script

    body = str(textinput)
    payload = {
        "inputs": {
            "input_string": [body]
            }
        }
    
    try: 
        payloads = str.encode(json.dumps(payload))
    except Exception as e:
        print(e)
        return str(e)


    url = os.environ['gpt2url']
    api_key = os.environ['gpt2key']

    headers = {
        'Content-Type':'application/json',
        'Authorization':('Bearer '+ api_key)}
    if deployment != 'none':
        headers['azureml-model-deployment'] = deployment


    req = urllib.request.Request(url, payloads, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        result = json.loads(result)[0]["0"]

        depslot = response.headers['azureml-model-deployment']

        return({'response': result, 'deployment': depslot})
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return(error.code)