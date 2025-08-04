from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bd_trab_user:password@localhost/bd_trab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bd_trab_user:password@localhost/bd_trab'
# IMPORTANT: This secret key is for development only.
# In a production environment, this should be set to a secure, unique value,
# preferably loaded from an environment variable.
app.config['SECRET_KEY'] = 'a-temporary-secret-key-for-testing'
db = SQLAlchemy(app)

from app import routes
