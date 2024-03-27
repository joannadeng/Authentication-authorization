from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
   """connect to a database"""
   db.app = app
   db.init_app(app)
     

class User(db.Model):
   """create a user model"""

   __tablename__ = 'users'

   username = db.Column(db.String(20), primary_key=True)
   password = db.Column(db.Text, nullable = False)
   email = db.Column(db.String(50),nullable=False,unique=True)
   first_name = db.Column(db.String(30),nullable = False)
   last_name = db.Column(db.String(30),nullable = False)
   # is_admin = db.Column(db.Boolean,default = False)

   @classmethod
   def register(cls,username,password,email,first_name,last_name):
      """register user with/hashed password & return a new user"""

      hashed = bcrypt.generate_password_hash(password)
      # turn byteString into normal string

      hashed_utf8 = hashed.decode('utf8')

      return cls(username=username,password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)

   @classmethod 
   def authenticate(cls,username,password):
      """validate if the user exists or password is correct, return user if true,
      else return false"""

      u = User.query.filter_by(username = username).first()
      if u and bcrypt.check_password_hash(u.password,password):
         return u
      else:
         return False

   feedbacks = db.relationship('Feedback', cascade="all, delete", backref='user') 
   # cascade delete not working


class Feedback(db.Model):
   """create a feedback"""

   __tablename__ = 'feedbacks'

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.String(100),nullable = False)
   content = db.Column(db.Text,nullable = False)
   username = db.Column(db.String(20), db.ForeignKey('users.username'),nullable=False)

 
