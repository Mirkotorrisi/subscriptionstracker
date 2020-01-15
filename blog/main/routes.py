from flask import render_template, request, Blueprint
from blog.models import Abbonati
import datetime, calendar
from blog import db
from sqlalchemy import desc
from flask_login import login_required



main = Blueprint('main', __name__)
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.datetime(year, month, day)

def end_near(scadenza):
    y = datetime.datetime.now()

    return  scadenza - y <= datetime.timedelta(days=4)


@main.route('/')
@login_required

def index():
    posts = Abbonati.query.order_by(Abbonati.scadenza)
    for post in posts:
        if  post.versato >= post.quota:
            post.versato -= post.quota
            post.scadenza = add_months(post.scadenza, 1)
        post.end_near = end_near(post.scadenza)
        db.session.commit()
    return render_template('index.html', title="Home", posts=posts)