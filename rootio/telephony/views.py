from flask import g, Blueprint, render_template, request, flash, Response, json
from flask.ext.login import login_required

from .models import PhoneNumber, Message, Call
from .forms import PhoneNumberForm

from ..extensions import db

telephony = Blueprint('telephony', __name__, url_prefix='/telephony')

@telephony.route('/', methods=['GET'])
def index():
    return render_template('telephony/index.html')


@telephony.route('/phonenumber/', methods=['GET'])
def phonenumbers():
    phonenumbers = PhoneNumber.query.all()
    return render_template('telephony/phonenumbers.html', phonenumbers=phonenumbers, active='phonenumbers')


@telephony.route('/phonenumber/<int:phonenumber_id>', methods=['GET', 'POST'])
def phonenumber(phonenumber_id):
    phonenumber = PhoneNumber.query.filter_by(id=phonenumber_id).first_or_404()
    form = PhoneNumberForm(obj=phonenumber, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(phonenumber)

        db.session.add(phonenumber)
        db.session.commit()
        flash('Phone Number updated.', 'success')

    return render_template('telephony/phonenumber.html', phonenumber=phonenumber, form=form)


@telephony.route('/phonenumber/add/', methods=['GET', 'POST'])
@login_required
def phonenumber_add():
    form = PhoneNumberForm(request.form)
    phonenumber = None

    if form.validate_on_submit():
        cleaned_data = form.data #make a copy
        cleaned_data.pop('submit',None) #remove submit field from list
        phonenumber = PhoneNumber(**cleaned_data) #create new object from data

        db.session.add(phonenumber)
        db.session.commit()
        flash('Phone Number added.', 'success') 
    elif request.method == "POST":
        flash('Validation error','error')

    return render_template('telephony/phonenumber.html', phonenumber=phonenumber, form=form)


@telephony.route('/calls/', methods=['GET'])
def calls():
    return render_template('telephony/calls.html', active='calls')

@telephony.route('/messages/', methods=['GET'])
def messages():
    return render_template('telephony/messages.html', active='messages')