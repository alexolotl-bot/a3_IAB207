from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

    # relation to call for user's tickets
    orders = db.relationship('Order', backref='user' ) 

    # relation to call for user's created events?
    events = db.relationship('Event', backref='user')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
# User Ticket Order Table
class Orders(db.Model):
    __tablename__ = 'orders' 
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # unsure if needed 
    user_id = db.Column(db.Interger, db.ForeignKey('users.id'))
    # event_id = db.Column(db.Interger, db.ForeignKey('events.id'))

    # relation to call user.orders
    # user = db.relationship('User', backref='user')
    # event = db.relationship('Event', backref='event')

    # relation to call for getting specific ticket ids?
    tickets = db.relationship('Ticket', backref='ticket')


    # string print method
    def __repr__(self):
        return f"Order Ref: {self.id}"

# Ticket Table
class Ticket(db.Model, UserMixin):
    __tablename__ = 'tickets' 
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Interger, db.ForeignKey('users.id'))
    event_id = db.Column(db.Interger, db.ForeignKey('events.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))


    # relation to call 
    # user = db.relationship('User', backref='user')
    # event = db.relationship('Event', backref='event')
    
    # string print method
    def __repr__(self):
        return f"ID: {self.id}"

# need to rework for our system 
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    # date/time 
    date = db.Column(db.DateTime)

    #TICKETS 
    price = db.Column(db.String(3))
    # price = db.Column(db.Interger, default=0)

    total_tickets = db.Column(db.Integer)

    # how do we want to categories the food events?? 
    category = db.Column(db.String(400))

    # Creator of event
    user_id = db.Column(db.Interger, db.ForeignKey('users.id'))

    # ... Create the Comments db.relationship
	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')

    # relation to call for getting event tickets
    tickets = db.relationship('Ticket', backref='ticket')

	# string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"