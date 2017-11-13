import flask
import pickle
from RCC import RCC

app = flask.Flask(__name__)


@app.route("/")
def home_page():
    with open("home.html", 'r') as home_file:
        return home_file.read()


@app.route("/class", methods=["POST"])
def party():
    data = flask.request.get_json()
    rcc = RCC(data["comment"][2])
    pred = rcc.predict_comment(data["comment"][0], int(data["comment"][1]))
    results = {"pred": pred}
    print(results)
    return flask.jsonify(results)


if __name__ == '__main__':
    app.run()