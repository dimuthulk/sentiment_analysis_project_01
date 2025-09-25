from flask import Flask,render_template,request,redirect
from helper import preprocessing, vectorizer, get_prediction, tokens
from logger import logging


app = Flask(__name__)

logging.info("Application started")

data = dict()
reviews = []
positive = 0
negative = 0

@app.route("/")
def index():
    data['reviews'] = reviews
    data['positive'] = positive
    data['negative'] = negative
    logging.info("================ Open home Page ================")
    return render_template("index.html", data=data)

@app.route("/", methods=["POST"])
def my_post():
    text = request.form['text']
    logging.info(f"Received review: {text}")
    preprocessed_text = preprocessing(text)
    logging.info(f"Preprocessed text: {preprocessed_text}")
    vectorized_text = vectorizer(preprocessed_text, vocabulary=tokens)
    logging.info(f"Vectorized text: {vectorized_text}")
    prediction = get_prediction(vectorized_text)
    logging.info(f"Prediction: {prediction}")
    
    if prediction == 'positive':
        logging.info(f"Received positive review: {text}")
        global positive
        positive += 1
    else:
        global negative
        logging.info(f"Received negative review: {text}")
        negative += 1
    reviews.insert(0, text)
    return redirect(request.url)


if __name__ == "__main__":
    app.run()