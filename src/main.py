from flask import Flask
from flask import render_template, redirect, url_for, send_file, abort
from flaskwebgui import FlaskUI  # import FlaskUI
import os

app = Flask(__name__)


# TODO: auto copy next html files to templates folder
@app.route("/")
def index():
    return render_template("index.html")


# TODO: auto copy next static out on build to static folder
@app.route("/<path:path>")
def rewrite_next(path):
    if os.path.exists(f"./static/{path}"):
        return send_file(f"./static/{path}")
    return abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":

    # TODO: if env == dev then Flask if prod then FlaskUI
    if os.getenv("is_dev") == "True":
        app.run(host="0.0.0.0", debug=True, use_reloader=True)
    else:
        FlaskUI(app=app, server="flask").run()
