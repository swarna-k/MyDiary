from flask.ext.wtf import Form 
from wtforms import StringField, BooleanField, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from models import User, Entry



class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True





class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Submit")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False


class EntryForm(Form):
  name = TextField("Entry name",  [validators.Required("Please enter the diary entry name")])
  body = TextAreaField("Entry",  [validators.Required("Please enter your diary entry")])
  submit = SubmitField("Create Entry")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class ReminderForm(Form):
  year = SelectField("/", choices=[('2015','2015'),('2016','2016'),('2017','2017'),('2018','2018'),('2019','2019'),('2020','2020'),('2021','2021'),('2022','2022')])
  month = SelectField("Date ", choices=[('01','January'),('02','February'),('03','March'),('04','April'),('05','May'),('06','June'),('07','July'),('08','August'),('09','September'),('10','October'),('11','November'),('12','December')])
  day = SelectField("/", choices=[('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31')])
  hour = SelectField("Time ", choices=[('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23')])
  minute = SelectField(":", choices=[('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','30'),('51','51'),('52','52'),('53','53'),('54','54'),('55','55'),('56','56'),('57','57'),('58','58'),('59','59')])
  second = SelectField(":", choices=[('00','00'),('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),('46','46'),('47','47'),('48','48'),('49','49'),('50','30'),('51','51'),('52','52'),('53','53'),('54','54'),('55','55'),('56','56'),('57','57'),('58','58'),('59','59')])
  body = TextAreaField("Task",  [validators.Required("Please enter your diary entry")])
  submit = SubmitField("Create Reminder")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def new(cls):
        # Instantiate the form
        form = cls()
        return form


class DisplayReminderForm(Form):
  year = SelectField("/", choices=[('2015','2015'),('2016','2016'),('2017','2017'),('2018','2018'),('2019','2019'),('2020','2020'),('2021','2021'),('2022','2022')])
  month = SelectField("Date ", choices=[('01','January'),('02','February'),('03','March'),('04','April'),('05','May'),('06','June'),('07','July'),('08','August'),('09','September'),('10','October'),('11','November'),('12','December')])
  day = SelectField("/", choices=[('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),('06','06'),('07','07'),('08','08'),('09','09'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31')])
  submit = SubmitField("Get Reminder")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)


  
  def new(cls):
        # Instantiate the form
        form = cls()
        return form