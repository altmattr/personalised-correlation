from flask import Flask, render_template, request
import csv
import os.path
import dataProcessing
from qualitricsApiDownloadsDATA import get_all_results
app = Flask(__name__) 

def correlation_data_to_list():
    data = []
    with open('data/scaled-corr-matrix.csv', 'rt') as csvfile:
        corr_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in corr_reader:
            data.append(row)
    return data

def freq_data_to_list():
    symptom_data = []

    with open('data/freq.csv', 'rt') as freqfile:
        filereader = csv.reader(freqfile, delimiter=',',  quotechar='|')
        for row in filereader:
            symptom_data.append(row)
    
    return symptom_data


# route for index
@app.route('/')
def hello():
    data = correlation_data_to_list()
    symptom_data = freq_data_to_list()
    return render_template("index.html", data=data, symptomData=symptom_data)


@app.route('/data')
def get_survey_data():
    # make a call to the qualtrics API to update the user data files
    get_all_results(apiToken='CAd56GmSu02n04L1INwMYGOdaDzJXktCXiSGnUFJ', surveyId='SV_2i51uu8Vidq2zC5')

    # run data.py to update data based on new information
    dataProcessing.main()

    # get the value of userID query string (i.e. ?userID=some-value)
    userID = request.args.get('userID')

    # get all the survey response data
    survey_responses = []
    with open ('data/DSM MQ Data Survey 1.2.csv', 'rt') as responsescsv:
        reader = csv.reader(responsescsv, delimiter=',', quotechar='|')
        for row in reader:
            survey_responses.append(row)

    # find the individual response data based on query string
    i = len(survey_responses)-1
    id_index = -1
    while i >= 0:
        # find the respondent's row
        if survey_responses[i][0] == userID:
            id_index = i
            print(survey_responses[i])
            # get results
        i -= 1

    return 'OK'


if __name__ == '__main__':
    app.run()

