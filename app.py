from flask import Flask, render_template, request, redirect
import csv
import requests
import os.path
import dataProcessing
import pandas as pd
from api import get_all_results

app = Flask(__name__) 

def parse_correlation_data():
    """Get correlation data from the csv and transform into list of tuples"""
    data = []
    with open('data/scaled-corr-matrix.csv', 'rt') as csvfile:
        corr_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in corr_reader:
            data.append(row)
    return data

@app.route('/')
def index():
    """Main index page. Re-routes to /data using a sample user ID as query string"""
    return render_template("spiel.html")

@app.route('/data')
def get_survey_data():

    survey_id   = request.args.get('surveyId',    default="SV_2i51uu8Vidq2zC5")
    response_id = request.args.get('response_id', default="R_3k7VdqOhcAIj36U")

    # get correlation matrix data
    files = get_all_results(surveyId = survey_id)

    # generate individual's symptom data and the group averages
    symptom_data = dataProcessing.main(files[0], response_id)
    corr = parse_correlation_data()

    return render_template("index.html", data=corr, symptomData=symptom_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

