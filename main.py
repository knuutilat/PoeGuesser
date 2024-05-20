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
  result = None  # Variable to store guess check result

  if request.method == "POST":
    for key, value in request.form.items():
      if key.startswith("text-input-"):  # Check if key starts with the desired prefix
        guess_id = key.split("-")[-1]
        guess = value
        result = check_guess(guess, guess_id, "temp.csv")  # Replace with actual CSV path
        break  # Stop after finding the first text input

  return render_template('index.html', image_urls=image_urls, image_ids=image_ids, zip=zip, guess=guess, result=result)


def check_guess(guess, guess_id, csv_file):
  # Open the CSV file in read mode
  with open(csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    # Skip header row (optional, adjust based on your CSV)
    next(reader, None)
    # Loop through each row in the CSV
    for row in reader:
      # Check if the user input (extracted number from guess_id) matches the row number (index starts from 0)
      if int(guess_id) == int(row[0]):  # row[1] accesses the second column value
        # Match found! Process the row data (optional)
        matched_row = row
        print(f"Match found! Name: {row[2]} Row Index:{row[0]}")
        break
        
    if matched_row:
        if guess.lower() == matched_row[2].lower():
            print("Correct answer")
        else:
            print("Wrong answer")
  return False  # No match found
