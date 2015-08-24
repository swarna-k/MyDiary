from app import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
  
  id = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
  entries = db.relationship('Entry', backref='author', lazy='dynamic')
  reminders = db.relationship('Reminder', backref='author', lazy='dynamic')

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  def __repr__(self):
        return '<User %r>' % (self.firstname)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Entry %r>' % (self.body)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    when = db.Column(db.DateTime)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Reminder %r>' % (self.body)


