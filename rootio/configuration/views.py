# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask import Blueprint, render_template, request, flash
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, current_user

from rootio.config import DefaultConfig
from ..content.forms import CommunityMenuForm
from ..content.models import CommunityMenu
from ..extensions import db
from ..radio.forms import StationForm, StationTelephonyForm, StationSipTelephonyForm, StationAudioLevelsForm, StationSynchronizationForm, StationTtsForm
from ..radio.models import Station, Network
from ..user.models import User
from ..utils import upload_to_s3, make_dir, save_uploaded_file

configuration = Blueprint('configuration', __name__, url_prefix='/configuration')


@configuration.route('/', methods=['GET'])
def index():
    # get all the user's networks and their stations
    networks = Network.query.outerjoin(Station).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/index.html', networks=networks, userid=current_user.id, now=datetime.now)


@configuration.route('/tts/', methods=['GET'])
def tts():
    stations = Station.query.all()
    # demo, override station statuses
    for s in stations:
        s.status = "on"

    # end demo
    return render_template('configuration/tts.html', stations=stations)


@configuration.route('/telephony/', methods=['GET', 'POST'])
def telephony():
    stations = Station.query.join(Network).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/stations_telephony.html', stations=stations)


@configuration.route('/telephony/<int:station_id>', methods=['GET', 'POST'])
def telephony_station(station_id):
    station = Station.query.filter_by(id=station_id).first_or_404()
    form = StationTelephonyForm(obj=station, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()
        flash(_('Station updated.'), 'success')

    return render_template('configuration/station_telephony.html', station=station, form=form)


@configuration.route('/telephony/add/', methods=['GET', 'POST'])
@login_required
def telephony_add():
    form = StationTelephonyForm(request.form)
    station = None

    if form.validate_on_submit():
        cleaned_data = form.data  # make a copy
        cleaned_data.pop('submit', None)  # remove submit field from list
        cleaned_data.pop('phone_inline', None)  # and also inline forms
        cleaned_data.pop('location_inline', None)
        station = Station(**cleaned_data)  # create new object from data

        db.session.add(station)
        db.session.commit()
        flash(_('Station added.'), 'success')
    elif request.method == "POST":
        flash(_('Validation error'), 'error')

    return render_template('configuration/station_telephony.html', station=station, form=form)


@configuration.route('/sip_configuration/<int:station_id>', methods=['GET', 'POST'])
@login_required
def sip_configuration(station_id):
    station = Station.query.filter_by(id=station_id).first_or_404()
    form = StationSipTelephonyForm(obj=station, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()
        flash(_('SIP details updated.'), 'success')

    return render_template('configuration/sip_configuration.html', station=station, form=form)


@configuration.route('/sip_telephony', methods=['GET', 'POST'])
def sip_telephony():
    stations = Station.query.join(Network).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/sip_telephony.html', stations=stations)


@configuration.route('/station_audio_level/<int:station_id>', methods=['GET', 'POST'])
def station_audio_level(station_id):
    station = Station.query.filter_by(id=station_id).first_or_404()
    form = StationAudioLevelsForm(obj=station, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()
        flash(_('Audio levels updated.'), 'success')

    return render_template('configuration/station_audio_level.html', station=station, form=form)


@configuration.route('/station_audio_levels', methods=['GET'])
def station_audio_levels():
    stations = Station.query.join(Network).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/station_audio_levels.html', stations=stations, active='stations')


@configuration.route('/ivr_menus', methods=['GET', 'POST'])
def ivr_menus():
    community_menus = CommunityMenu.query.join(Station).join(Network).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/ivr_menus.html', community_menus=community_menus)


@configuration.route('/ivr_menu', methods=['GET', 'POST'])
@login_required
def ivr_menu():
    form = CommunityMenuForm(request.form)
    community_menu = None
    station = form.station
    if request.method == 'POST':
        pass  # validate files here
    if form.validate_on_submit():
        station = request.form['station']
        cleaned_data = form.data  # make a copy
        cleaned_data.pop('submit', None)
        for key in request.files.keys():
            prompt_file = request.files[key]
            file_path = os.path.join("community-menu", station)
            uri = save_uploaded_file(prompt_file, file_path)
            cleaned_data[key] = uri

        community_menu = CommunityMenu(**cleaned_data)  # create new object from data

        db.session.add(community_menu)
        db.session.commit()

        flash(_('Configuration saved.'), 'success')

    elif request.method == "POST":
        flash(_(form.errors.items()), 'error')

    return render_template('configuration/ivr_menu.html', community_menu=community_menu, form=form, station=station)


# def save_uploaded_file(uploaded_file, directory, file_name=False):
#     date_part = datetime.now().strftime("%y%m%d%H%M%S")
#     if not file_name:
#         file_name = "{0}_{1}".format(date_part, uploaded_file.filename)
#
#     if DefaultConfig.S3_UPLOADS:
#         try:
#             location = upload_to_s3(uploaded_file, file_name)
#         except:
#             flash(_('Media upload error (S3)'), 'error')
#             raise
#     else:
#         upload_directory = os.path.join(DefaultConfig.CONTENT_DIR, directory)
#         make_dir(upload_directory)
#         file_path = os.path.join(upload_directory, file_name)
#         try:
#             uploaded_file.save(file_path)
#         except:
#             flash(_('Media upload error (filesystem)'), 'error')
#             raise
#         location = "{0}/{1}".format(directory, file_name)
#
#     return location


@configuration.route('/tts_settings', methods=['GET', 'POST'])
@login_required
def tts_settings():
    stations = Station.query.join(Network).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/tts_settings.html', stations=stations)


@configuration.route('/tts_setting/<int:station_id>', methods=['GET', 'POST'])
@login_required
def tts_setting(station_id):
    station = Station.query.filter_by(id=station_id).first_or_404()
    form = StationTtsForm(obj=station, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()
        flash(_('TTS settings updated.'), 'success')

    return render_template('configuration/tts_setting.html', station=station, form=form)


@configuration.route('/synchronization_settings', methods=['GET', 'POST'])
@login_required
def synchronization_settings():
    stations = Station.query.join(Network).join(User, Network.networkusers).filter(User.id == current_user.id).all()
    return render_template('configuration/synchronization_settings.html', stations=stations)


@configuration.route('/synchronization_setting/<int:station_id>', methods=['GET', 'POST'])
@login_required
def synchronization_setting(station_id):
    station = Station.query.filter_by(id=station_id).first_or_404()
    form = StationSynchronizationForm(obj=station, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(station)

        db.session.add(station)
        db.session.commit()
        flash(_('Synchronization settings updated.'), 'success')

    return render_template('configuration/synchronization_setting.html', station=station, form=form)
