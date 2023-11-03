from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, OrderForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/bookings')
@login_required
def bookings():
    id = current_user.id
    bookings =  db.session.scalar(db.select(Order).where(Order.user_id==id))
    for order in current_user.orders:
        print(order.event.name)
        print(order)
    print(current_user.orders)
    print(current_user.events)

    return render_template('bookings.html', orders=current_user.orders, )

@user_bp.route('/events')
@login_required
def events():
    id = current_user.id
    events =  db.session.scalar(db.select(Event).where(Event.user_id==id))
    for event in current_user.events:
        print(event.name)
        print(event)

    print(current_user.events)

    return render_template('userEvents.html', events=current_user.events, )