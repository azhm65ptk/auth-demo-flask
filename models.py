from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Tweet(db.Model):
    __tablename__='tweets'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    text= db.Column(db.Text, nullable= False)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))

    user= db.relationship('User', backref='tweets')

    
class User(db.Model):
    __tablename__ ='users'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)

    username= db.Column(db.Text, nullable= False, unique= True)

    password= db.Column(db.Text, nullable= False)

    @classmethod
    def register(cls, username,pwd):
        '''register user with hashed pwd and return user'''

        hashed=bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal (unicdoe utf8) string
        hashed_utf8=hashed.decode('utf8')

        #return instance of user with username and hased pwd

        return cls(username=username, password=hashed_utf8 )

    @classmethod
    def authenticate(cls,username, pwd):
        """validate that user exists and pwd is correct"""

        u= User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else: 
            return False

