import hashlib
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


@pytest.mark.parametrize(
    ("url", "model"), (("/positive", Positive), ("/contact", Contact))
)
def test_create(url, model, client):
    key = str(uuid.uuid4())
    checksum = hashlib.sha256(key.encode("utf-8")).hexdigest()
    hash = hashlib.sha256((key + checksum).encode("utf-8")).hexdigest()
    rv = client.post(
        url,
        data=json.dumps({"key": key, "checksum": checksum, "hash": hash}),
        headers={"Content-Type": "application/json"},
    )
    assert rv.status_code == 201, rv.data
    query = session.query(model, model.key, model.hash, model.checksum)
    _, retrieved_key, retrieved_hash, retrieved_checksum = query.one()
    assert retrieved_key == key, rv.json
    assert retrieved_hash == hash, rv.json
    assert retrieved_checksum == checksum, rv.json


@pytest.mark.parametrize("url", ("/positive", "/contact"))
def test_get(url, client):
    random_keys = [str(uuid.uuid4()) for _ in range(10)]

    for random_key in random_keys:
        checksum = hashlib.sha256(random_key.encode("utf-8")).hexdigest()
        hash = hashlib.sha256(
            (random_key + checksum).encode("utf-8")
        ).hexdigest()
        rv = client.post(
            url,
            data=json.dumps(
                {"key": random_key, "checksum": checksum, "hash": hash}
            ),
            headers={"content-type": "application/json"},
        )
        assert rv.status_code == 201, rv.data

    rv = client.get(url)
    assert rv.status_code == 200
    stored_keys = rv.json
    assert sorted(stored_keys) == sorted(random_keys), rv.data
