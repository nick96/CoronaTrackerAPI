"""Contact graph API."""

import json
import os

from flask import Flask, request
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

CONN_STRING = os.environ["DATABASE_URL"]
db = create_engine(CONN_STRING)
Session = sessionmaker(bind=db)
session = Session()

app = Flask(__name__)

Base = declarative_base()


# class Positive(Base):
#     """Table of keys that have tested positive."""

#     __tablename__ = "positive"
#     key = Column(String, primary_key=True)


# class Contact(Base):
#     """Table of keys that have been in contact with a positive case."""

#     __tablename__ = "contact"
#     key = Column(String, primary_key=True)


class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    count = Column(Integer)


Base.metadata.create_all(db)


@app.route("/hello", methods=["GET"])
def hello_get():
    name_filter = request.args.get("name")
    if name_filter is None:
        query = session.query(Name, Name.name, Name.count)
    else:
        query = session.query(Name, Name.name, Name.count).filter_by(name=name_filter)
    response = []
    for _, name, count in query.all():
        response.append({"name": name, "count": count})
    return json.dumps(response)


@app.route("/hello", methods=["POST"])
def hello_post():
    name_param = request.args.get("name")
    if name_param is None:
        response = {
            "error": {
                "code": 400,
                "title": "ValidationError",
                "detail": "URL params must contain 'name'",
            }
        }
        return json.dumps(response), 400
    name = session.query(Name).filter_by(name=name_param).one_or_none()
    if name is None:
        name = Name(name=name_param, count=0)
    name.count += 1
    session.add(name)
    session.commit()
    return {"name": name.name, "count": name.count}, 201
