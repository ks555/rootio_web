#flask-admin views

from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView

from ..extensions import db

from ..radio.models import *
from ..telephony.models import *

class AdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.role_code == 0
        else:
            return False

def admin_routes(admin):
    admin.add_view(AdminView(PhoneNumber, db.session))
    admin.add_view(AdminView(Message, db.session))
    admin.add_view(AdminView(Call, db.session))

    admin.add_view(AdminView(Person, db.session))
    admin.add_view(AdminView(Location, db.session))
    admin.add_view(AdminView(Station, db.session))
    admin.add_view(AdminView(Program, db.session))
    admin.add_view(AdminView(Episode, db.session))