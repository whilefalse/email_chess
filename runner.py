from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def run(klass):
    application = webapp.WSGIApplication([klass.mapping()], debug=True)
    webapp.util.run_wsgi_app(application)
