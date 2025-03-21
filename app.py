from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'supersecretkey')

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

from routes import app as routes_app
app.register_blueprint(routes_app)

if __name__ == '__main__':
    app.run(debug=True)
