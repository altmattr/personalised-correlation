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


@app.route('/')
def index():
    return 'hello'


@app.route('/data')
def get_survey_data():
    #TODO: crash gracefully

    # make a call to the qualtrics API to update the user data files
    get_all_results(apiToken='CAd56GmSu02n04L1INwMYGOdaDzJXktCXiSGnUFJ', surveyId='SV_2i51uu8Vidq2zC5')

    # get the value of userID query string (i.e. ?response_id=some-value)
    response_id = request.args.get('response_id')

    data = correlation_data_to_list()

    symptom_data = dataProcessing.main(response_id)

    return render_template("index.html", data=data, symptomData=symptom_data)

if __name__ == '__main__':
    app.run()

