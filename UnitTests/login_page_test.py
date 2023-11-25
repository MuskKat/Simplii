import unittest
from flask import Flask
#from src.controller.user_controller import create_user, login_control, get_loggedIn_User

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False

    def test_login_method(self):
        with self.app.test_client() as client:
            response = client.get('/login')
            self.assertEqual(response.status_code, 404)

    def test_login_post_method_valid(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username="testuser",
                password="testpassword"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 404)

    def test_login_post_method_invalid(self):
        with self.app.test_client() as client:
            response = client.post('/login', data=dict(
                username="invaliduser",
                password="invalidpassword"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 404)

    def test_signup_method(self):
        with self.app.test_client() as client:
            response = client.post('/signup', data=dict(
                username="newuser",
                password="newpassword",
                email="newuser@example.com",
                fullname="New User"
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 404)

    def test_logout_method(self):
        with self.app.test_client() as client:
            response = client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
