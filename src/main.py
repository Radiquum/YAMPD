from flask import Flask
from flask import render_template, send_file, abort
from flaskwebgui import FlaskUI  # import FlaskUI
import os
import sys
from flask_socketio import SocketIO
from engineio.async_drivers import threading

from api import apiPack, apiPacks, apiDownload


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = Flask(
    __name__,
    static_folder=resource_path("static"),
    template_folder=resource_path("templates"),
)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

app.register_blueprint(apiPack)
app.register_blueprint(apiPacks)
app.register_blueprint(apiDownload)


if os.getenv("is_dev") == "True":
    from flask_cors import CORS

    CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:path>")
def rewrite_next(path):
    if os.path.exists(f"{resource_path("static")}/{path}"):
        return send_file(f"{resource_path("static")}/{path}")
    if os.path.exists(f"{resource_path("templates")}/{path}.html"):
        return render_template(f"{path}.html")
    return abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


if __name__ == "__main__":

    if os.getenv("is_dev") == "True":
        socketio.run(app, host="0.0.0.0", debug=True, use_reloader=True)
        # app.run(host="0.0.0.0", debug=True, use_reloader=True)
    else:
        # FlaskUI(app=app, server="flask").run()
        FlaskUI(
            app=app, socketio=socketio, server="flask_socketio", width=800, height=600
        ).run()
