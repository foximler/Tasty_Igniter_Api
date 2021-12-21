from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from project import db, create_app, models
from project.models import User

def create_db():
    db.create_all(app=create_app())

def signup_initial(email,name,passsword,password_verify):
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'parakeetsarejustllamas'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project/db.sqlite'
	db = SQLAlchemy()
	db.init_app(app)
	# code to validate and add user to database goes here
	if password != password_verify:
		return "Error Password Doesnt Match"
	# create a new user with the form data. Hash the password so the plaintext version isn't saved.
	new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
	with app.app_context():
		db.session.add(new_user)
		db.session.commit()

print("Generating Intial Database")
create_db()
print("Creating Admin Account")
print("Please Enter Email")
email = input()
print("Please Enter Account Name")
name = input()
print("Please Enter Password")
password = input()
print("Please Enter Password again to verify")
password_verify = input()
signup_initial(email,name,password,password_verify)
print("Initial User Made. Please Delete 'initialsetup.py'...")