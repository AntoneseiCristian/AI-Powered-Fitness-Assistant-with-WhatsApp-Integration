import unittest
from app import app, db, User
from flask_login import login_user
from werkzeug.security import generate_password_hash

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.ctx = app.app_context()  # Create an application context
        self.ctx.push()  # Push the application context onto the stack
        db.create_all()

        # Create a test user
        hashed_password = generate_password_hash('testpassword', method='sha256')
        test_user = User(username='testuser', password=hashed_password)
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        # Clean up the database
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_landing_page(self):
        # Test that the landing page loads correctly
        response = self.app.get('/landing', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Test logging in
        response = self.app.post('/landing', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
        self.assertIn(b'Welcome to the BMI App', response.data)

    def test_invalid_login(self):
        # Test logging in with invalid credentials
        response = self.app.post('/landing', data=dict(username='invalid', password='invalid'), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_registration(self):
        # Test user registration
        response = self.app.post('/register', data=dict(username='newuser', password='newpassword', confirm_password='newpassword'), follow_redirects=True)
        self.assertIn(b'Registration successful. You can now log in.', response.data)

    def test_bmi_calculation(self):
        # Log in as the test user
        self.app.post('/landing', data=dict(username='testuser', password='testpassword'), follow_redirects=True)

        # Submit the BMI calculation form
        response = self.app.post('/', data=dict(weight=70, height=170), follow_redirects=True)

        # Check if the response data contains the expected result
        self.assertIn(b'Your BMI is', response.data)


if __name__ == '__main__':
    unittest.main()
