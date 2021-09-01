import requests
import zipfile
import json
import io
import pandas as pd
import os
import glob

def get_all_results(surveyId='SV_2i51uu8Vidq2zC5', fileFormat='csv'):
    # get the token and data center for this survey
    data = pd.read_csv("data/tokens.csv")
    if (os.environ.get(surveyId)):
      print("token retrieved from env")
      token = os.environ.get(surveyId)
    else:
      print("token retrieved from file")
      token = data.loc[data["survey"] == surveyId]["token"][0].strip()
    # data center is always retrieved from file
    data_center = data.loc[data["survey"] == surveyId]["data_center"][0].strip()

    # Setting static parameters
    requestCheckProgress = 0
    progressStatus = "in progress"
    baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": token,
        }

    print(baseUrl, flush=True)
    print(headers, flush=True)
    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
    print("about to post request", flush=True)
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["id"]
    print(progressId, flush=True);

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while requestCheckProgress < 100 and progressStatus != "complete":
        print("waiting for response", flush=True)
        requestCheckUrl = baseUrl + progressId
        print(requestCheckUrl, flush=True)
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        print("response was", flush=True)
        print(requestCheckResponse.text, flush=True)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete", flush=True)

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + progressId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    with zipfile.ZipFile(io.BytesIO(requestDownload.content)) as myzip:
        myzip.extractall("tmp")
        print('Complete')
        print(myzip.namelist(), flush=True)
        ret = pd.read_csv('tmp/{0}'.format(myzip.namelist()[0]))
    globpatt = glob.glob('tmp/*')
    for f in globpatt:
      os.remove(f)
    return ret
 