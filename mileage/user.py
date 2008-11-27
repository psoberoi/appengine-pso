from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class MileageUser(db.Model):
    user = db.UserProperty()
    username = db.StringProperty()

def get_current_user():
    userid = users.get_current_user()
    if userid is None:
        return None
    user = MileageUser.all().filter('user =', userid).get()
    return user

class AddUserPage(webapp.RequestHandler):
    def assert_new_user(self):
        user = get_current_user()
        if user is not None:
            raise Exception('Error - user already exists')

    def get(self):
        self.assert_new_user()
        self.response.out.write("""\
        <html>
            <head><title>Mileage - Add a New User</title></head>
            <body>
                <form action="adduser" method="post">
                    Enter your Name:
                    <input type="text" name="username" />
                    <br/><br/>
                    <input type="submit" value="Create User" />
                </form>
            </body>
        </html>""")

    def post(self):
        self.assert_new_user()
        user = MileageUser()
        user.user = users.get_current_user()
        user.username = self.request.get('username')
        user.put()
        self.redirect('user/%s/' % user.key().id())

class UserPage(webapp.RequestHandler):
    def get(self, userid):
        userid = int(userid)
        user = get_current_user()
        if user is None or user.key().id() != userid:
            raise Exception('Error - visiting other users\' pages is not permitted')

        self.response.out.write("""\
        <html>
            <head><title>Mileage - User Home Page</title></head>
            <body>
                <h3>Welcome, %s!</h3>
                <b>Your Cars:</b>
                <ul>""" % user.username)
        for car in ['car1', 'car2']:
            self.response.out.write("""
                <li>%s</li>""" % car)
        self.response.out.write("""
                <li><a href="/mileage/addcar">Add Car<a/></li>
                </ul>
            </body>
        </html>
        """)

