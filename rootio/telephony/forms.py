# from wtforms import Form
from flask.ext.babel import gettext as _
from flask.ext.wtf import Form
from wtforms import SubmitField, RadioField, StringField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import AnyOf, Required

from .constants import PHONE_NUMBER_TYPE
from .models import PhoneNumber, Gateway
from ..extensions import db

PhoneNumberFormBase = model_form(PhoneNumber,
                                 db_session=db.session,
                                 base_class=Form,
                                 exclude=[
                                     'areacode',
                                     'created_at',
                                     'updated_at',
                                     'person',
                                     'station_cloud',
                                     'station_transmitter',
                                     'stations',
                                 ])


class PhoneNumberForm(PhoneNumberFormBase):
    number = StringField(_('Phone Number'), [Required()], default=" ")
    number_type = RadioField(_("Type"),
                             [AnyOf([str(val) for val in PHONE_NUMBER_TYPE.keys()])],
                             choices=[(str(val), label) for val, label in PHONE_NUMBER_TYPE.items()])
    submit = SubmitField(_('Save'))


GatewayFormBase = model_form(Gateway,
                             db_session=db.session,
                             base_class=Form,
                             exclude=[
                                 'created_at',
                                 'updated_at',
                             ])


class GatewayForm(GatewayFormBase):
    name = StringField()
    number_top = db.Column(db.Integer)
    number_bottom = db.Column(db.Integer)
    sofia_string = StringField()
    extra_string = StringField()
    submit = SubmitField(_('Save'))
