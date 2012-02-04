'''
Created on 24.5.2009

@author: pietarike
'''
from google.appengine.ext import db
from piet.model.department import Department

class Employee(db.Model):
  firstname = db.StringProperty(required=True)
  lastname = db.StringProperty(required=True)
  department_ref = db.ReferenceProperty(Department)