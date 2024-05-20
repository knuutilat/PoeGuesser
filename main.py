from flask import Flask, render_template, request
from itertools import count
import csv


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    image_urls = []
    image_ids = []
    with open('temp.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            image_urls.append(row[1])
            image_ids.append(row[0])

    guess = None
    result = None

    if request.method == "POST":
        for key, value in request.form.items():
            if key.startswith("text-input-"):
                guess_id = key.split("-")[-1]
                guess = value
                result = check_guess(guess, guess_id, "temp.csv")
                break

    return render_template('index.html', image_urls=image_urls, image_ids=image_ids, zip=zip, guess=guess, result=result)


def check_guess(guess, guess_id, csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:

            if int(guess_id) == int(row[0]):
                matched_row = row
                print(f"Match found! Name: {row[2]} Row Index:{row[0]}")
                break

        if matched_row:
            if guess.lower() == matched_row[2].lower():
                print("Correct answer")
            else:
                print("Wrong answer")
    return False
