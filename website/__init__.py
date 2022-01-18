from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app(CONFIG):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['database_uri']
    app.config['SECRET_KEY'] = CONFIG['secret_key']

    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    login_manager = LoginManager()
    login_manager.loin_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app