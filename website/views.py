from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    # validating the event status and updating if needed 
    for event in events:
        event.set_status()
        db.session.commit()
    return render_template('index.html', events=events)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.category.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))