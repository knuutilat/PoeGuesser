from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    image_urls = []
    with open('amulets.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            image_urls.append(row[0])
    return render_template('index.html', image_urls=image_urls)