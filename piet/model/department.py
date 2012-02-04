'''
Created on 23.5.2009

@author: pietarike
'''

from google.appengine.ext import db

class Department(db.Model):
  name = db.StringProperty(required=True)
  description = db.StringProperty()
  