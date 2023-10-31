from . import db
from datetime import datetime, date, time
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user_ref')
    events = db.relationship('Event', backref='creator')

    def __repr__(self):
        return f"Name: {self.name}"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    num_tickets = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    purchased_at = db.Column(db.DateTime, default=datetime.now())

    event = db.relationship('Event', backref='associated_event')
    user = db.relationship('User', backref='order_ref')

    def __repr__(self):
        return f"Order Ref: {self.id}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    address = db.Column(db.String(100))
    datetime = db.Column(db.DateTime)
    ticket_price = db.Column(db.Integer)
    total_tickets = db.Column(db.Integer)
    available_tickets = db.Column(db.Integer)
    category = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    status = db.Column(db.String(20), default='Open')

    user = db.relationship('User', backref='created_events')
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='related_orders')

    def __repr__(self):
        return f"Name: {self.name}"
    def set_status(self):
        if self.status == 'Cancelled':
            return 'Cancelled'
        elif self.available_tickets == 0:
            return 'Sold Out'
        elif self.datetime < datetime.now():
            return 'Inactive'
        else:
            return 'Open'
    

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"