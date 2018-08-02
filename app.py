from flask import Flask, render_template, request, redirect
import csv
import os.path
import dataProcessing
from qualitricsApiDownloadsDATA import get_all_results

app = Flask(__name__) 

def parse_correlation_data():
    """Get correlation data from the csv and transform into list of tuples"""
    data = []
    with open('data/scaled-corr-matrix.csv', 'rt') as csvfile:
        corr_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in corr_reader:
            data.append(row)
    return (data ,)


@app.route('/')
def index():
    """Main index page. Re-routes to /data using a sample user ID as query string"""
    return redirect('/data?response_id=R_b437z8esnOET9yd', code=302)


@app.route('/data')
def get_survey_data():
    """Get data from qualtrics api, get response id from query string, process data and display results"""
    # make a call to the qualtrics API to update the user data files
    # uses qualtricsApiDownloadsDATA.py
    get_all_results(apiToken='CAd56GmSu02n04L1INwMYGOdaDzJXktCXiSGnUFJ', surveyId='SV_2i51uu8Vidq2zC5')

    # get the value of userID query string (i.e. ?response_id=some-value)
    response_id = request.args.get('response_id')

    # get correlation matrix data
    data = parse_correlation_data()

    # generate individual's symptom data and the group averages
    symptom_data = dataProcessing.main(response_id)

    return render_template("index.html", data=data, symptomData=symptom_data)

if __name__ == '__main__':
    app.run()

