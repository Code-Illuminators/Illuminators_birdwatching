import pytest
from Birdwatching import create_app
from Birdwatching.utils.databases import Base, init_db
from werkzeug.security import generate_password_hash
from Birdwatching.utils.databases import post_sql, get_user

@pytest.fixture()
def app():
    app = create_app()

    app.config["DATABASE_URL"] = "sqlite:///:memory:"

    init_db(app)
    from Birdwatching.utils.databases import engine

    # with app.app_context():
    #     Base.metadata.create_all(engine)

    yield app

    # with app.app_context():
    #     Base.metadata.drop_all(engine)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def login_user(client):
    def _login_user(username="user", password="password"):
        return client.post('/auth/login', data={"username": username, "password": password})
    return _login_user

