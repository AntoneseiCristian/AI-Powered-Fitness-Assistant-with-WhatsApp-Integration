from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager, login_manager
from database import db
import auth
import main
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.landing'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    babel = Babel(app)

    app.register_blueprint(auth.auth)
    app.register_blueprint(main.main)

    return app
