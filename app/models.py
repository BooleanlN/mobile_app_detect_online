from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import db,login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

user_role = db.Table('userRole',db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
role_previlage = db.Table('rolePrevilage',db.Column('role_id',db.Integer,db.ForeignKey('role.id')),
                     db.Column('previlage', db.Integer, db.ForeignKey('previlage.id')))
class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    history = db.relationship('History',backref='author',lazy='dynamic')
    roles = db.relationship('Role',secondary=user_role,backref=db.backref('users',lazy='dynamic'),lazy='dynamic')
    def __repr__(self):#返回一个可以用来表示对象的可打印字符串
        return '<User {}>'.format(self.username)
    def set_password(self,password):
        self.password_hash = generate_password_hash(password=password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def check_email(self,email):
        return  not self.email == email
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    previlages = db.relationship('Previlage',secondary=role_previlage,backref=db.backref('roles',lazy='dynamic'),lazy='dynamic')
    def __repr__(self):
        return '<Role {}>'.format(self.description)
class Previlage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))

    def __repr__(self):
        return '<Previlage {}>'.format(self.description)