"""
Contact graph API.

- Each person has a random key
- Hash the key using a cryptographically random hash
- Give person hash of key + checksum and the checksum itself
- If test positive, broadcast key
- User checks if hashes match key + checksum
- Need both the checksum (given at time of contact) and key to prove contact
"""

import json
import os
from datetime import datetime

from sqlalchemy import Column, DateTime, String, create_engine, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask, Response, jsonify, request
from marshmallow import Schema, ValidationError, fields

CONN_STRING = os.environ["DATABASE_URL"]
db = create_engine(CONN_STRING)
Session = sessionmaker(bind=db)
session = Session()

app = Flask(__name__)

Base = declarative_base()


class PositiveSchema:
    class Request(Schema):
        key = fields.Str(required=True)
        hash = fields.Str(required=True)
        checksum = fields.Str(required=True)


class ContactSchema(Schema):
    class Request(Schema):
        key = fields.Str(required=True)
        hash = fields.Str(required=True)
        checksum = fields.Str(required=True)


class Positive(Base):
    """Table of keys that have tested positive."""

    __tablename__ = "positive"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    hash = Column(String, unique=True)
    checksum = Column(String, unique=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)


class Contact(Base):
    """Table of keys that have been in contact with a positive case."""

    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    hash = Column(String, unique=True)
    checksum = Column(String, unique=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)


@app.route("/positive", methods=["POST"])
def create_positive():
    """Create a new record of a positive test mapping to the given key."""
    try:
        body = PositiveSchema.Request().load(request.json)
    except ValidationError as e:
        response = {
            "error": {
                "code": 400,
                "title": "ValidationError",
                "details": e.messages,
            }
        }
        return response, 400
    positive = Positive(
        key=body["key"], checksum=body["checksum"], hash=body["hash"]
    )
    try:
        session.add(positive)
        session.commit()
    except IntegrityError as e:
        app.logger.info("%s already exists in the databse: %s", body["key"], e)
        response = {
            "error": {
                "code": 400,
                "title": "IntegrityError",
                "details": [f"'{body['key']}' has already been submitted"],
            }
        }
        return response, 400
    return Response(status=201)


@app.route("/positive", methods=["GET"])
def get_positives():
    """Get all the available positive records."""
    response = [key for _, key in session.query(Positive, Positive.key).all()]
    return jsonify(response)


@app.route("/contact", methods=["POST"])
def create_contact():
    """Create a new record of contact with a positive test."""
    try:
        body = ContactSchema.Request().load(request.json)
    except ValidationError as e:
        response = {
            "error": {
                "code": 400,
                "title": "ValidationError",
                "details": e.messages,
            }
        }
        return response, 400
    contact = Contact(
        key=body["key"], hash=body["hash"], checksum=body["checksum"]
    )
    try:
        session.add(contact)
        session.commit()
    except IntegrityError as e:
        app.logger.info("%s already exists in the databse: %s", body["key"], e)
        response = {
            "error": {
                "code": 400,
                "title": "IntegrityError",
                "details": [f"'{body['key']}' has already been submitted"],
            }
        }
        return response, 400
    return Response(status=201)


@app.route("/contact", methods=["GET"])
def get_contacts():
    """Get all the availabe records of contact."""
    response = [key for _, key in session.query(Contact, Contact.key).all()]
    return jsonify(response)
