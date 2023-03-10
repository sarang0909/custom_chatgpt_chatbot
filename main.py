"""A main script to run Chatbot.

"""

from flask import Flask, render_template, request
from src.nlp_core import NLPCore


app = Flask(__name__)
nlp_core = NLPCore()


@app.route("/")
def home():
    """A base method for web app"""

    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    """A method to get bot response

    Returns:
        str : A bot response to a query
    """
    user_text = request.args.get("msg")
    website_name = request.args.get("websiteName")
    nlp_core.set_website_name(website_name)
    return str(nlp_core.core_method(user_text))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
