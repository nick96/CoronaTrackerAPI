import json
import uuid

import pytest

from app import Contact, Positive, app, session


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def before_each():
    session.query(Positive).delete()
    session.query(Contact).delete()


def test_create_positive(client):
    rv = client.post(
        "/positive",
        data=json.dumps({"key": "test"}),
        headers={"Content-Type": "application/json"},
    )
    assert rv.status_code == 201, rv.data
    _, key = session.query(Positive, Positive.key).one()
    assert key == "test"


def test_get_positives(client):
    random_keys = [str(uuid.uuid4()) for _ in range(10)]

    for random_key in random_keys:
        rv = client.post(
            "/positive",
            data=json.dumps({"key": random_key}),
            headers={"content-type": "application/json"},
        )
        assert rv.status_code == 201, rv.data

    rv = client.get("/positive")
    assert rv.status_code == 200
    stored_keys = rv.json
    assert sorted(stored_keys) == sorted(random_keys)


def test_create_contact(client):
    rv = client.post(
        "/contact",
        data=json.dumps({"key": "test"}),
        headers={"content-type": "application/json"},
    )
    assert rv.status_code == 201, rv.data
    _, key = session.query(Contact, Contact.key).one()
    assert key == "test"


def test_get_contacts(client):

    random_keys = [str(uuid.uuid4()) for _ in range(10)]

    for random_key in random_keys:
        rv = client.post(
            "/contact",
            data=json.dumps({"key": random_key}),
            headers={"content-type": "application/json"},
        )
        assert rv.status_code == 201, rv.data

    rv = client.get("/contact")
    assert rv.status_code == 200
    stored_keys = rv.json
    assert sorted(stored_keys) == sorted(random_keys)
