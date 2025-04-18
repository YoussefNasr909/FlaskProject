from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "b339f8784e4baa72e389743af5b2ddbfa4271aa615838d7fec426f1aa6530955"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/flaskproj"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # إضافة Bcrypt

# Import routes and models after app and db creation to avoid circular imports
import routes
import models