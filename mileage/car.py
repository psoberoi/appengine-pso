from __future__ import absolute_import

from google.appengine.ext import db
from google.appengine.ext import webapp

import mileage.user

class MileageVehicle(db.Model):
    make = db.StringProperty()
    model = db.StringProperty()
    year = db.IntegerProperty()
    description = db.StringProperty()
    users = db.ListProperty(db.Key)
    public = db.BooleanProperty()

def get_valid_user():
    user = mileage.user.get_current_user()
    if user is None:
        raise Exception('Error - user does not exist')
    return user

class AddCarPage(webapp.RequestHandler):
    def get(self):
        get_valid_user()
        self.response.out.write("""\
        <html>
            <head><title>Mileage - Add a New Car</title></head>
            <body>
                <form action="addcar" method="post">
                    Make: <input type="text" name="make" />
                    Model: <input type="text" name="model" />
                    Year: <input type="text" name="year" />
                    <br/>
                    Description: <input type="text" name="description" size="60"/>
                    <br/>
                    <input type="checkbox" name="public" />Public
                    <br/><br/>
                    <input type="submit" value="Add Car" />
                </form>
            </body>
        </html>""")

    def post(self):
        user = get_valid_user()
        car = MileageVehicle()
        car.make = self.request.get('make')
        car.model = self.request.get('model')
        car.year = int(self.request.get('year'))
        car.description = self.request.get('description')
        car.public = (self.request.get('public') == 'on')
        car.users = [user.key()]
        car.put()
        self.redirect('car/%d/' % car.key().id())

class CarPage(webapp.RequestHandler):
    def get(self, carid):
        user = get_valid_user()
        self.response.out.write("""\
        <html>
            <head><title>Mileage - Car Page</title></head>
            <body>
            hello
            </body>
        </html>""")

