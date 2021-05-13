def test_welcome_api(app):
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Hello World!" in response.data
