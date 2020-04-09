"""Contact graph API."""

import json
import os

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask, Response, jsonify, request

CONN_STRING = os.environ["DATABASE_URL"]
db = create_engine(CONN_STRING)
Session = sessionmaker(bind=db)
session = Session()

app = Flask(__name__)

Base = declarative_base()


class Positive(Base):
    """Table of keys that have tested positive."""

    __tablename__ = "positive"
    key = Column(String, primary_key=True)


class Contact(Base):
    """Table of keys that have been in contact with a positive case."""

    __tablename__ = "contact"
    key = Column(String, primary_key=True)


Base.metadata.create_all(db)


@app.route("/positive", methods=["POST"])
def create_positive():
    """Create a new record of a positive test mapping to the given key."""
    body = request.json
    if "key" not in body:
        response = {
            "error": {
                "code": 400,
                "title": "ValidationError",
                "detail": "'key' field is required",
            }
        }
        return response, 400
    positive = Positive(key=body["key"])
    session.add(positive)
    session.commit()
    return Response(status=201)


@app.route("/positive", methods=["GET"])
def get_positives():
    """Get all the available positive records."""
    response = [key for _, key in session.query(Positive, Positive.key).all()]
    return jsonify(response)


@app.route("/contact", methods=["POST"])
def create_contact():
    """Create a new record of contact with a positive test."""
    body = request.json
    if "key" not in body:
        response = {
            "error": {
                "code": 400,
                "title": "ValidationError",
                "detail": "'key' field is required",
            }
        }
        return jsonify(response), 400
    contact = Contact(key=body["key"])
    session.add(contact)
    session.commit()
    return Response(status=201)


@app.route("/contact", methods=["GET"])
def get_contactS():
    """Get all the availabe records of contact."""
    response = [key for _, key in session.query(Contact, Contact.key).all()]
    return jsonify(response)
