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


@pytest.mark.parametrize("url", ("/positive", "/create"))
def test_create(url, client):
    key = str(uuid.uuid4)
    checksum = hashlib.sha256(key.encode("utf-8")).hexdigest()
    hash = hashlib.sha256((key + checksum).encode("utf-8")).hexdigest()
    rv = client.post(
        url,
        data=json.dumps({"key": key, "checksum": checksum, "hash": hash}),
        headers={"Content-Type": "application/json"},
    )
    assert rv.status_code == 201, rv.data
    _, key, hash, checksum = session.query(
        Positive, Positive.key, Positive.hash, Positive.checksum
    ).one()
    assert key == "test"
    assert hash == "test"
    assert checksum == "test"


@pytest.mark.parametrize("url", ("/positive", "/create"))
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

    rv = client.get("/positive")
    assert rv.status_code == 200
    stored_keys = rv.json
    assert sorted(stored_keys) == sorted(random_keys)
