"""Contact graph API."""

import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    name = request.args.get("name", "World")
    return json.dumps({"message": f"Hello, {name}"})
