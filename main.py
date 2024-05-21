from flask import Flask, render_template, request, jsonify
from itertools import count
import csv


app = Flask(__name__)
app.debug = True

correct_answers = 0
answered_correctly = set()


@app.route('/', methods=["GET", "POST"])
def index():
    image_urls = []
    image_ids = []
    total_items = 0
    with open('temp.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            image_urls.append(row[1])
            image_ids.append(row[0])
            total_items += 1

    guess = None
    result = None
    if request.method == "POST":
        for key, value in request.form.items():
            if key.startswith("text-input-"):
                guess_id = key.split("-")[-1]
                guess = value
                result = check_guess(guess, guess_id, "temp.csv")
                break

        return jsonify({
            'correct_answers': correct_answers,
            'total_items': total_items,
            'result': result
        })
    return render_template('index.html', image_urls=image_urls, image_ids=image_ids, zip=zip, guess=guess, result=result, correct_answers=correct_answers, total_items=total_items)


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

            if guess.lower() == matched_row[2].lower() and guess_id not in answered_correctly:
                print("Correct answer")
                global correct_answers
                correct_answers += 1
                answered_correctly.add(guess_id)
                return {'isCorrect': True, 'imageId': guess_id}

    return False


@app.route('/check_answer/<guess_id>', methods=["POST"])
def check_answer(guess_id):
    try:
        int(guess_id)
    except ValueError:
        return jsonify({'isCorrect': False, 'message': 'Invalid image ID'}), 400

    with open('temp.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if int(guess_id) == int(row[0]):
                correct_answer = row[2].lower()
                break
        else:
            return jsonify({
                'isCorrect': False,
                'message': 'Error: Answer not found'}), 500

    data = request.get_json()
    user_guess = data.get('user_guess', '')

    is_correct = user_guess.lower() == correct_answer.lower()

    response = {'isCorrect': is_correct}
    if not is_correct:
        response['message'] = f"Incorrect. The answer is '{
            correct_answer}', your answer '{user_guess}'"

    return jsonify(response)
