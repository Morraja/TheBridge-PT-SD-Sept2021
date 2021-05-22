"""
Main file for GeNLP.

Author: Esteban M. Sanchez Garcia
LinkedIn: linkedin.com/in/estebanmsg/
GitHub: github.com/esan94
Medium: medium.com/@emsg94
Kaggle: kaggle.com/esan94
"""


import flask
import pickle
from nltk import download

from model import preprocessing_text_data


download("averaged_perceptron_tagger")
download("punkt")
download("wordnet")

app = flask.Flask(__name__, static_folder="static")

SESSION = dict()


@app.route("/", methods=("GET", "POST"))
def main():
    """
    Main route for GeNLP app.
    ---
    responses:
      500:
        description: Error in GeNLP.
      200:
        description: OK.

    """

    if flask.request.method == "POST":
        SESSION["get_genres"] = flask.request.form.get("get_genres", False)
        SESSION["synopsis"] = flask.request.form.get("synopsis", "")

        # Text preprocessing.
        preprocessed_text = preprocessing_text_data(SESSION["synopsis"])

        # Load models.
        count_vect = pickle.load(open("pickles/count_vectorizer.pkl", "rb"))
        model = pickle.load(open("pickles/onevsrestcomplementnb.pkl", "rb"))
        classes = pickle.load(open("pickles/classes.pkl", "rb"))
        
        x_train = count_vect.transform([preprocessed_text])
        predicted = model.predict_proba(x_train)
        top3 = sorted(range(len(predicted[0])), key=predicted[0].__getitem__)[-3:][::-1]
        final_top3_predictions = " ".join([classes[t3] for t3 in top3])
        SESSION["pred_genres"] = final_top3_predictions

    else:
        SESSION.clear()

    genre_message = True if SESSION.get("get_genres", False) else False
    genres = SESSION.get("pred_genres")
    synopsis = SESSION.get("synopsis", "")

    return flask.render_template("items/main.html", gen_mes=genre_message,
                                 synopsis=synopsis, genres=genres)
