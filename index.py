#!/usr/bin/env python

import os
from google.appengine.ext.webapp import template
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import mail

def html_response(handler, page, templatevalues=None):
    #Renders an HTML response using a provided template page and values
    path = os.path.join(os.path.dirname(__file__), page)
    handler.response.headers["Content-Type"] = "text/html"
    handler.response.out.write(template.render(path, templatevalues))

class Applicant(db.Model):
    first = db.StringProperty()
    last = db.StringProperty()
    email = db.StringProperty()
    applied_on = db.DateTimeProperty(auto_now_add=True)

class HomeHandler(webapp.RequestHandler):
    #Handles requests to the front page
    def get(self):
        html_response(self,'templates/index.html')
    
    def post(self):
        entry = self.request.get('entry')
        commands = ['about','apply','help']
        arguments = entry.split()
        if len(arguments) > 0:
            command = arguments[0]
        else:
            command = ''
        if command in commands:
            if (command == "help") and (len(arguments) == 1):
                message = """To apply, type "apply" followed your name and email. For example: apply Thomas Anderson theone@gmail.com. If you're still lost, shoot us an email at team@hackpackit.com."""
            elif command == "about":
                message = "We are a startup firm, filling contracts for other businesses and starting our own."
            elif command == "apply":
                if len(arguments) == 4:
                    applicant = Applicant()
                    applicant.first = arguments[1]
                    applicant.last = arguments[2]
                    applicant.email = arguments[3]
                    applicant.put()
                    mail.send_mail(sender="Hackpack Signup <umchaselee@gmail.com>",
                        to="Alex Schiff <alex@fetchnotes.com>, Chase Lee <umchaselee@gmail.com>",
                        subject="%s %s has applied to Hackpack! #woot" % (applicant.first,applicant.last),
                        body="""Our newest applicant:
                                Name: %s %s 
                                Email: %s
                                Have a sexy day!""" % (applicant.first,applicant.last,applicant.email))
                    message = "Thanks for applying %s %s. We will contact you soon at %s." % (applicant.first,applicant.last,applicant.email)
                elif len(arguments) == 1:
                    message = "Usage: apply &ltfirst name&gt &ltlast name&gt &ltemail&gt"
                else:
                    message = """Invalid arguments<br />
                                 Sends your application to the Hackpack<br />
                                 apply &ltfirst name&gt &ltlast name&gt &ltemail&gt<br /><br />
                                 Options: coming soon..."""
            else:
                message = "That's dumb. You didn't enter anything that worked. Shouldn't you know how to use a terminal?"
        else:
            message = "That's dumb. You didn't enter anything that worked. Shouldn't you know how to use a terminal?"
        response = {}
        response['message'] = message
        html_response(self,'templates/index.html',response)
        
class NotFoundHandler(webapp.RequestHandler):
    #Handles requests to pages that don't exist
    def get(self):
        self.response.out.write("There's no page here!")


def main():
    application = webapp.WSGIApplication([('/', HomeHandler),('.*',NotFoundHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()    
