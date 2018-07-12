from flask import Flask, render_template
import csv
import os.path
app = Flask(__name__) 

data = []

symptomData = []

with open('data/corr-matrix.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

with open('data/freq.csv', 'rt') as freqfile:
    filereader = csv.reader(freqfile, delimiter=',',  quotechar='|')
    for row in filereader:
        symptomData.append(row)


# route for index
@app.route('/')
def hello():
    return render_template("index.html", data=data, symptomData=symptomData)
if __name__ == '__main__':
    app.run()