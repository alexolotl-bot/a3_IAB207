
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

# Create a new event
# some started code modified from tute demo code
ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventForm(FlaskForm):
  name = StringField('Name', validators=[InputRequired()])
  date = DateField("Date", validators=[InputRequired()])
  time = TimeField("Time", validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  
  num_tickets = IntegerField('Number of Tickets', validators=[InputRequired()])


  #   still need to add
#   date/time
#   location/address?
#   event category
#   total number of tickets
    # need to modify for ticket pricing  
    # currency = StringField('Currency', validators=[InputRequired()])
  submit = SubmitField("Create")

# Purchase tickets for an event
class TicketForm(FlaskForm):
#    price = IntegerField("Price")
#    number of tickets 
# not sure what else tickets would have 
# price/ total prices
   submit = SubmitField('Purchase')
