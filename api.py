import requests
import zipfile
import json
import io
import pandas as pd
import os
import glob
import re

def get_all_results(surveyId='SV_2i51uu8Vidq2zC5', fileFormat='csv'):
    # get the token and data center for this survey
    data = pd.read_csv("data/tokens.csv.secret", dtype='unicode')
    if (os.environ.get(surveyId)):
      print("token retrieved from env", flush=True)
      token = os.environ.get(surveyId)
    else:
      print("token retrieved from file", flush=True)
      print(data.loc[data["survey"] == surveyId]["token"].values[0], flush=True)
      token = data.loc[data["survey"] == surveyId]["token"].values[0].strip()
    # data center is always retrieved from file
    data_center = data.loc[data["survey"] == surveyId]["data_center"].values[0].strip()
    # regex is always retrieved from file
    regex = data.loc[data["survey"] == surveyId]["regex"].values[0].strip()

    # Setting static parameters
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
    print(progressId, flush=True)

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    requestCheckProgress = 0
    progressStatus = "in progress"
    while requestCheckProgress < 100 or progressStatus != "complete":
        print("waiting for response", flush=True)
        requestCheckUrl = baseUrl + progressId
        print(requestCheckUrl, flush=True)
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        print("response was", flush=True)
        print(requestCheckResponse.text, flush=True)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        progressStatus = requestCheckResponse.json()["result"]["status"]
        print("Download is " + str(requestCheckProgress) + " complete "+str(progressStatus), flush=True)

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + progressId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    with zipfile.ZipFile(io.BytesIO(requestDownload.content)) as myzip:
        myzip.extractall("tmp")
        print('Complete')
        print(myzip.namelist(), flush=True)
        ret = pd.read_csv('tmp/{0}'.format(myzip.namelist()[0]), dtype='unicode')
        cols = [c for c in ret.columns if (re.match(regex, c) or re.match('(?i)response ?_?id', c))]
        ret = ret[cols]
    globpatt = glob.glob('tmp/*')
    for f in globpatt:
      os.remove(f)
    return ret
 
def get_user_results(surveyId, responseId):
     # get the token and data center for this survey TODO: this code is repeated!!! factor it out somehow TODO: for real, this duplication already cost you 30 mins - fix it!
    data = pd.read_csv("data/tokens.csv.secret", dtype='unicode')
    if (os.environ.get(surveyId)):
      print("token retrieved from env", flush=True)
      token = os.environ.get(surveyId)
    else:
      print("token retrieved from file", flush=True)
      print(data.loc[data["survey"] == surveyId]["token"].values[0], flush=True)
      token = data.loc[data["survey"] == surveyId]["token"].values[0].strip()
    # data center is always retrieved from file
    data_center = data.loc[data["survey"] == surveyId]["data_center"].values[0].strip()
    # regex is always retrieved from file
    regex = data.loc[data["survey"] == surveyId]["regex"].values[0].strip()

    # Setting static parameters
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/responses/{2}".format(data_center, surveyId, responseId)
    headers = {
        "content-type": "application/json",
        "x-api-token": token,
        }

    print(baseUrl, flush=True)
    print("about to post request", flush=True)
    data = {}
    lookup = {}
    response = requests.request("GET", baseUrl, headers=headers)
    for key, value in response.json()["result"]["values"].items():
      doLooker = re.search("(.*)_DO", key)
      if (doLooker):
        questLooker = re.match("Q(\d*\.\d*)_.*", value[0])
        if (questLooker):
          length = len(value)
          print(length, flush=True)
          for i in range(1, length):
            data["Q{0}_Q{0}_{1}".format(questLooker.group(1), i)] = response.json()["result"]["values"]["{0}_{1}".format(doLooker.group(1),i)]
          lookup[doLooker.group(1)] = questLooker.group(1)
    print(lookup, flush=True)
    print(data, flush=True)
    return data

if __name__ == '__main__':
    get_all_results(surveyId="SV_6xtvNTckiy9wSi2")