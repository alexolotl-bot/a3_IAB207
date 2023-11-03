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
        try:
            id = session['user_name']
        except Exception as e:
            user_name=""
        args=[Event.status!="cancel"]
        category=request.args.get('category',"")
        event_name=request.args.get('event_name',"")
        if category:
            args.append(Event.category==category)
        if event_name:
            args.append(Event.name.like("%{}%".format(event_name)))

        records = Event.query.filter(*args).all()
        events = []
        _events = []
        count = 1
        for record in records:
            name = record.name
            image = os.path.join("/static", "images", record.image)
            datetime = record.datetime
            status = record.status
            price = record.ticket_price
            description = record.description[:30] + "...."
            _events.append({
                "id": record.id,
                "name": name,
                "image": image,
                "datetime": datetime,
                "status": status,
                "price": price,
                "description": description,
            })
            if count % 2 == 0:
                events.append(_events)
                _events = []
            count += 1
        if _events:
            events.append(_events)
        return render_template('EventPage.html', user_name=user_name, events=events,event_name=event_name,category=category)

def detail(self):
        user_name = ""
        try:
            user_name = session['user_name']
        except Exception:
            pass
        _id = request.args.get('id')
        record = Event.query.filter(Event.id == _id).first()
        name = record.name
        img_src = os.path.join("/static", "images", record.image)
        event_date = record.event_date
        status = record.status
        price = record.price
        category = record.category
        location = record.location
        description = record.description
        event = {
            "id": record.id,
            "name": name,
            "img_src": img_src,
            "category": category,
            "location": location,
            "event_date": event_date,
            "status": status,
            "price": price,
            "description": description
        }
        comment_records=Comment.query.filter(Comment.event_id==_id).all()

        return render_template('EventDetailsPage.html', user_name=user_name, event=event,comment_records=comment_records)


@user_bp.route('/myevent')
@login_required
def myevent():
    id = current_user.id
    events =  db.session.scalar(db.select(Event).where(Event.user_id==id))
    for event in current_user.events:
        print(event.name)
        print(event)

    print(current_user.events)

    return render_template('MyEvent.html', events=current_user.events)
