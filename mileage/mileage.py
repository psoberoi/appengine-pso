import wsgiref.handlers

from google.appengine.ext import webapp

import mileage.user
import mileage.car

# URL Scheme:
#
# / - if user exists, redirect to user's home page
#     else, create user.
# /adduser - add a new user
# /user/<id>/ - user's home page.  lists car summary
# /user/<id>/edit - edit user details
# /addcar - add new car
# /car/<id>/ - car detail - shows refuelings, and current mileage
# /car/<id>/edit - edit car details (including adding users)
# /car/<id>/refuel - get/post here to add refueling
# /car/<id>/refuel/<id>/ - show a particular refueling entry
# /car/<id>/refuel/<id>/edit - edit a refueling entry

class MainPage(webapp.RequestHandler):
    def get(self):
        user = mileage.user.get_current_user()
        if user is None:
            self.redirect('adduser')
        else:
            self.redirect('user/%s/' % user.key().id())

def main():
    app = webapp.WSGIApplication([
                (r'/mileage/', MainPage),
                (r'/mileage/adduser', mileage.user.AddUserPage),
                (r'/mileage/addcar', mileage.car.AddCarPage),
                (r'/mileage/user/(\d+)/', mileage.user.UserPage),
                (r'/mileage/car/(\d+)/', mileage.car.CarPage),
            ], debug=True
    )
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    main()
