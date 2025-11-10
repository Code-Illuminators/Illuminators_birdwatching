from Birdwatching.utils.databases import insert_user


def test_register(client, app):
    response = client.post('/auth/register', data={
        'username': 'user1',
        'password': 'password',
    })
    assert response.status_code == 302

def test_register_get(client, app):
    response = client.get('/auth/register')
    assert response.status_code == 200

def test_user_exists(client, app):
    with app.app_context():
        from werkzeug.security import generate_password_hash
        password = generate_password_hash('password')
        insert_user('user1', password)

    response = client.post('/auth/register', data={
        'username': 'user1',
        'password': 'password',
    })
    assert response.status_code == 200


def test_login(client, app):
    with app.app_context():
        from werkzeug.security import generate_password_hash
        password = generate_password_hash('password')
        insert_user('user1', password)
    response = client.post('/auth/login', data={
        'username': 'user1',
        'password': 'password',
    })
    print(response.data)
    with client.session_transaction() as session:
        assert 'user_id' in session
        assert 'username' in session
        assert 'user_role' in session
    assert response.status_code == 302

def test_invalid_login(client, app):
    print("create wrong user1")
    with app.app_context():
        from werkzeug.security import generate_password_hash
        password = generate_password_hash('password')
        insert_user('user1', password)
    print("login wrong user1")
    response = client.post('/auth/login', data={
        'username': 'user123',
        'password': 'password',
    })
    print(response.data)
    assert response.data



def test_logout(client, app):
    with app.app_context():
        from werkzeug.security import generate_password_hash
        password = generate_password_hash('password')
        insert_user('user1', password)
    response = client.post('/auth/login', data={
        'username': 'user1',
        'password': 'password',
    })
    print(response.data)
    with client.session_transaction() as session:
        assert 'user_id' in session
        assert 'username' in session
        assert 'user_role' in session
    response = client.get('/auth/logout')
    assert response.status_code == 302
