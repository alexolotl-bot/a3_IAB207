from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, OrderForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the ticket order form
    orderForm = OrderForm()
    # create the comment form
    form = CommentForm()    
    return render_template('events/show.html', event=event, form=form, orderForm=orderForm)

@event_bp.route('/<id>/tickets', methods=['GET', 'POST'])
@login_required
def purchaseTickets(id):  
    orderForm = OrderForm()  
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if orderForm.validate_on_submit(): 
      num_tickets = orderForm.num_tickets.data
    
        # validate number of tickets
      if(event.total_tickets >= num_tickets):
         order = Order(num_tickets= num_tickets, event=event, user=current_user)
         db.session.add(order) 
         db.session.commit() 

         event.total_tickets -= num_tickets
         db.session.commit()
         #flashing a message which needs to be handled by the html
         flash('Order placed successfully!', 'success')
         print('Order placed successfully!', 'success')   
      else:
         flash("Not enough tickets available.")
         print("Not enough tickets available.")
         
   
   
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))

@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,description=form.description.data, datetime= form.datetime.data,
                  address = form.address.data, image=db_file_path,
                  total_tickets=form.total_tickets.data, user=current_user)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new travel event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

# @destbp.route('/<id>/comment', methods=['GET', 'POST'])  
# @login_required
# def comment(id):  
#     form = CommentForm()  
#     #get the event object associated to the page and the comment
#     event = db.session.scalar(db.select(Event).where(Event.id==id))
#     if form.validate_on_submit():  
#       #read the comment from the form
#       comment = Comment(text=form.text.data, event=event,
#                         user=current_user) 
#       #here the back-referencing works - comment.event is set
#       # and the link is created
#       db.session.add(comment) 
#       db.session.commit() 
#       #flashing a message which needs to be handled by the html
#       flash('Your comment has been added', 'success')  
#       # print('Your comment has been added', 'success') 
#     # using redirect sends a GET request to event.show
#     return redirect(url_for('event.show', id=id))