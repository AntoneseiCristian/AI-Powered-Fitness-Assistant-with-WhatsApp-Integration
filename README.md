# AI-Powered Fitness Assistant with WhatsApp Integration

This project is a Flask-based web application that serves as an AI-powered fitness assistant. It leverages the capabilities of Twilio's WhatsApp API to facilitate interaction with an AI model. The application is designed to provide fitness advice, answer health-related questions, and calculate the Body Mass Index (BMI) of a user.

## Features

- User authentication: The application includes a secure login system.
- AI interaction: Users can send messages to the AI model and receive responses.
- WhatsApp integration: The application integrates with WhatsApp via Twilio's API, enabling users to interact with the AI model directly from their WhatsApp account.
- BMI calculation: Users can calculate their BMI by providing their height and weight.
- Display of recommendations based on the calculated BMI.
- Multi-language support (English and Romanian).
- User profile management: users can save and update their profile information (name, height, age, gender, and activity level).
- The height field on the BMI calculation form is pre-filled with the user's height from their profile.
- Navigation updates: added a Profile button in the navbar on the index and history page

## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages using pip:
3. Set up a Twilio account and configure the WhatsApp sandbox.
4. Set up ngrok to expose your local server to the internet. This is necessary for the Twilio API to be able to send requests to your application.
5. Update the `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER` in the `config.py` file with your Twilio account details.
6. Run the application:
    run.py
7. Open your web browser and go to `http://127.0.0.1:5000/` to access the application.

### Prerequisites

- Python 3.10
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Babel
- Werkzeug
- Flask-WTF
- Twillio


## Usage

1. Register for an account or log in if you already have one.
2. Enter your weight (in kg) and height (in cm) in the provided fields.
3. Click the "Calculate BMI" button.
4. The application will display your BMI and a recommendation based on the result.
5. Navigate to the Profile page to save or update your profile information.
