from flask import Flask, render_template
import csv
import os.path
app = Flask(__name__) 

data = []

with open('corr-matrix.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)


# route for index
@app.route('/')
def hello():
    return render_template("index.html", data=data)
if __name__ == '__main__':
    app.run()