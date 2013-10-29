# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, request, jsonify
from flask.ext.login import login_user, current_user, logout_user
from flask.ext.restless import APIManager

from .utils import parse_datetime

from ..extensions import db, rest

from ..user import User
from ..radio import Station, Program, ScheduledProgram, StationAnalytic
from ..decorators import returns_json

#the web login api
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated():
        return jsonify(flag='success')

    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        user, authenticated = User.authenticate(username, password)
        if user and authenticated:
            if login_user(user, remember='y'):
                return jsonify(flag='success')

    current_app.logger.debug('login(api) failed, username: %s.' % username)
    return jsonify(flag='fail', msg='Sorry, try again.')


@api.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    return jsonify(flag='success', msg='Logged out.')


#the restless api
#needs to be called after app instantiation
def restless_routes():
    rest.create_api(Station, collection_name='station', methods=['GET'],
        exclude_columns=['owner','api_key','scheduled_programs'],
        include_methods=['status','current_program'])
    rest.create_api(Program, collection_name='program', methods=['GET'])
    rest.create_api(ScheduledProgram, collection_name='scheduledprogram', methods=['GET'],
        exclude_columns=['station'])

#need routes for:
    #next content
    #content on date
    #content between dates
    #phone to post diagnostics

#non CRUD-routes
#convenience methods for flask-restless wonky filter syntax
@api.route('/station/<int:station_id>/schedule', methods=['GET'])
@returns_json
def station_schedule(station_id):
    station = Station.query.filter_by(id=station_id).first_or_404()
    start = parse_datetime(request.args.get('start'))
    end = parse_datetime(request.args.get('end'))
    print start,end
    #TODO, investigate the proper ordering of these clauses for query speed
    if start and end:
        return ScheduledProgram.between(start,end).filter_by(station_id=station.id)
    elif start:
        return ScheduledProgram.after(start).filter_by(station_id=station.id)
    elif end:
        return ScheduledProgram.before(end).filter_by(station_id=station.id)
    elif request.args.get('all'):
        return ScheduledProgram.query.filter_by(station_id=station.id)
    else:
        return {'error':"Need to specify parameters 'start' or 'end' as ISO datetime or all=1"}
