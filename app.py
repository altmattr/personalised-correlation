from flask import Flask, render_template, request, redirect
import csv
import requests
import os.path
import os
import dataProcessing
import pandas as pd
from api import get_all_results, get_user_results, get_tokens

app = Flask(__name__) 

@app.route('/')
def index():
    """Main index page. Re-routes to /data using a sample user ID as query string"""
    return render_template("spiel.html")

@app.route('/connection_check')
def connection_check():
    survey_id   = request.args.get('surveyId',    default="none")
    print("about to call get_all_results", flush=True)
    files = get_all_results(surveyId=survey_id, fileFormat="csv")
    print(files[0], flush = True)
    return render_template("spiel.html")

@app.route('/data_2d')
def two_d_vis():

    survey_id   = request.args.get('surveyId',    default="SV_2i51uu8Vidq2zC5")
    response_id = request.args.get('response_id', default="")
    response_t1 = request.args.get('responseT1', default=None)
    print(response_id, flush=True)

    user_results = get_user_results(survey_id, response_id)
    nodes = pd.read_csv('static/data/nodes.csv')
    links = pd.read_csv('static/data/forces.csv')
    (token, data_center, regex, parent) = get_tokens(survey_id)

    for i, row in nodes.iterrows():
      print(nodes.loc[i,"name"], flush=True)
      try: # if we don't have that response_id, just give 0
        nodes.loc[i,'response'] = user_results[nodes.loc[i,"name"]]
      except KeyError:
        nodes.loc[i, 'response'] = 0

    return render_template("two_d.html", nodes=nodes.to_csv(), links=links.to_csv(), response_t1=response_t1, parent=parent)

@app.route('/update_2d')
def update_data(survey_id=""):
    # survey id is set if we are warming up, then no request or response possible.
    
    if (survey_id == ""):
      survey_id   = request.args.get('surveyId',    default="SV_2i51uu8Vidq2zC5")

    # get correlation matrix data
    data = get_all_results(surveyId=survey_id, fileFormat="csv")
    print("results got")

    # generate individual's symptom data and the group averages
    (nodes, links) = dataProcessing.main(data)
    
    if (survey_id == ""):
      return render_template("two_d.html", nodes=nodes.to_csv(), links=links.to_csv())
    else:
      return None

@app.route('/demo_2d')
def two_d_demo():
  response_id = request.args.get('response_id', default="R_3IcolP1ze4SFUU2")
  (nodes, links) = dataProcessing.main(pd.read_csv('data/demo.csv'), response_id, ".*")

  return render_template("two_d.html", nodes=nodes.to_csv(), links=links.to_csv())

if __name__ == '__main__':
    # warm up the data
    update_data(survey_id='SV_6xtvNTckiy9wSi2')

    port = os.environ.get("PORT")
    if (port == None):
        port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)

