import requests
import zipfile
import json
import io

def get_all_results(apiToken='CAd56GmSu02n04L1INwMYGOdaDzJXktCXiSGnUFJ', surveyId='SV_2i51uu8Vidq2zC5', fileFormat='csv', dataCenter='mqedu'):

    # Setting static parameters
    requestCheckProgress = 0
    progressStatus = "in progress"
    baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/".format(dataCenter)
    headers = {
        "content-type": "application/json",
        "x-api-token": apiToken,
        }

    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
    print("about to post request")
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    print(downloadRequestResponse.json())
    progressId = downloadRequestResponse.json()["result"]["id"]
    print(downloadRequestResponse.text)

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while requestCheckProgress < 100 and progressStatus != "complete":
        print("waiting for response")
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")

    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + progressId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    # Step 4: Unzipping the file
    with zipfile.ZipFile(io.BytesIO(requestDownload.content)) as myzip:
        myzip.extractall("data")
        print('Complete')
        print(myzip.namelist(), flush=True)
        return myzip.namelist()
 