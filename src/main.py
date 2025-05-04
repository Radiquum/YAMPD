from flask import Flask
from flask import render_template, redirect, url_for, send_file, abort
from flaskwebgui import FlaskUI  # import FlaskUI
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:path>")
def rewrite_next(path):
    if os.path.exists(f"./static/{path}"):
        return send_file(f"./static/{path}")
    return abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # If you are debugging you can do that in the browser:
    app.run(host="0.0.0.0", debug=True, use_reloader=True)
    # If you want to view the flaskwebgui window:
#   FlaskUI(app=app, server="flask").run()
