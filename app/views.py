from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from app import app, db, lm, oid
from .forms import LoginForm,SignupForm,SigninForm,EntryForm,ReminderForm,DisplayReminderForm
from .models import User, Entry, Reminder
import datetime
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)


########################################################################

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
       
      session['email'] = newuser.email
      return redirect(url_for('profile')) 
      #return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
  

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

########################################################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/profile/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/profile',methods=['GET', 'POST'])
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
  
  if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')


##############################################################

@app.route('/diary', methods=['GET', 'POST'])
def diary():
  form = EntryForm()
  form1 = DisplayReminderForm()

  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
  
  if user is None:
    return redirect(url_for('signin'))
  

  if request.method == 'POST':
    if form.name.data!='':
      newentry = Entry(name=form.name.data,body=form.body.data, timestamp=datetime.datetime.utcnow(), author=user)
      db.session.add(newentry)
      db.session.commit()
      form.body.data=None
      form.name.data=None  

    

    year1 = form1.year.data
    month1 = form1.month.data
    day1 = form1.day.data
    
    if year1=='None':
      when=None
    else:    
      when = datetime.date(int(year1),int(month1),int(day1))

    return render_template('diary.html', form=form, form1=form1,user=user,list=user.entries.all(),when=when)
      

  elif request.method == 'GET':
    return render_template('diary.html', form=form, form1=form1,user=user,list=user.entries.all(),when=None)

###########################################

@app.route('/reminder', methods=['GET', 'POST'])
def reminder():
  form = ReminderForm()
  form1 = DisplayReminderForm()

  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
  
  if user is None:
    return redirect(url_for('signin'))
  

  if request.method == 'POST':
    year = form.year.data
    month = form.month.data
    day = form.day.data
    hour = form.hour.data
    minute = form.minute.data
    second = form.second.data
    #when = "%s-%s-%s %s:%s:%s" %(year,month,day,hour,minute,second)
    
    if year == 'None' or month == 'None' or day == 'None' or hour == 'None' or minute == 'None' or second == 'None':
      form.body.data=None
      
    else:  
      when = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
      newentry = Reminder(when=when,body=form.body.data, timestamp=datetime.datetime.utcnow(), author=user)
      db.session.add(newentry)
      db.session.commit()
      form.body.data=None

    year1 = form1.year.data
    month1 = form1.month.data
    day1 = form1.day.data
    
    if year1=='None':
      when=None
    else:    
      when = datetime.date(int(year1),int(month1),int(day1))
    
    return render_template('reminder.html', form=form, form1=form1,user=user,list=user.reminders.all(), when=when)

      

  elif request.method == 'GET':

    return render_template('reminder.html', form=form, form1=form1,user=user,list=user.reminders.all(),when=None)

###########################################

@app.route('/help')
def help():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('help.html')

###############################################

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('signin'))
    


