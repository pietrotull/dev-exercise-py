import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from piet.model.department import Department
from piet.model.employee import Employee

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()  
    if user:  
      self.response.out.write(template.render('templates/main.html', {}))
    else:
      self.redirect(users.create_login_url(self.request.uri))

class DepartmentPage(webapp.RequestHandler):
  def get(self):
      
    deps = db.GqlQuery('SELECT * FROM Department ORDER BY name')
      
    values = {
              'deps': deps
              }
    
    self.response.out.write(
      template.render('templates/department.html', values))
    
  def post(self):
    dep = Department(name=self.request.get('name'),
                     description=self.request.get('description'))
    dep.put()
    self.redirect('/department')
      
class EmployeePage(webapp.RequestHandler):
  def get(self):

    deps = db.GqlQuery('SELECT * FROM Department ORDER BY name ASC')
    emps = db.GqlQuery('SELECT * FROM Employee ORDER BY lastname ASC')
      
    values = {
              'deps': deps,
              'emps': emps
              }
    
    self.response.out.write(
      template.render('templates/employee.html', values))
    
    
  def post(self):
    emp = Employee(firstname=self.request.get('firstname'), 
                   lastname=self.request.get('lastname'), 
                   department_ref=Department.get(self.request.get('department_key')))
        
    emp.put()
    self.redirect('/employee')

class DetailsPage(webapp.RequestHandler):
  def get(self):
    depkey = self.request.get('key')
    dep = Department.get(depkey)
    emps = db.GqlQuery('SELECT * FROM Employee WHERE department_ref = :1', dep)
    values = {
              'dep': dep,
              'emps': emps 
              }
    self.response.out.write(template.render('templates/details.html', values))


class EditDepartmentPage(webapp.RequestHandler):
  def get(self):
    dep = Department.get(self.request.get('key'))
    values = {'dep': dep}
    self.response.out.write(template.render('templates/editdepartment.html', values))
    
  def post(self):
    
    dep = Department.get(self.request.get('key'))
  
    dep.name = self.request.get('name') 
    dep.description = self.request.get('description')
    dep.put()
    
    message = 'Changes saved'
    values = {'dep': dep,
              'message': message }

    self.response.out.write(template.render('templates/editdepartment.html', values))
    
class EditEmployeePage(webapp.RequestHandler):
  def get(self):
    emp = Employee.get(self.request.get('key'))
    deps = Department.all()
    values = {
              'emp': emp,
              'deps': deps
              }
    self.response.out.write(template.render('templates/editemployee.html', values))
    
  def post(self):
    emp = Employee.get(self.request.get('key'))
    emp.firstname = self.request.get('firstname') 
    emp.lastname = self.request.get('lastname')
    
    dep = Department.get(self.request.get('department_key'))
    emp.department_ref = dep
    emp.put()
    
    message = 'Changes saved' 
    deps = Department.all()
    values = {
              'emp': emp,
              'deps': deps,
              'message': message
              }
    
    self.response.out.write(template.render('templates/editemployee.html', values))
    
class DelDepartmentPage(webapp.RequestHandler):
  def get(self):
    dep = Department.get(self.request.get('key'))
    dep.delete()
    self.redirect('/department')
    
class DelEmployeePage(webapp.RequestHandler):
  def get(self):
    emp = Employee.get(self.request.get('key'))
    emp.delete()
    self.redirect('/employee')    
    
      
class ErrorPage(webapp.RequestHandler):
  def get(self):
      
    self.response.out.write(
      template.render('templates/errorpage.html', {}))      
    
application = webapp.WSGIApplication([('/', MainPage), 
                                      ('/department', DepartmentPage),
                                      ('/employee', EmployeePage),
                                      ('/details', DetailsPage),
                                      ('/editdepartment', EditDepartmentPage),
                                      ('/editemployee', EditEmployeePage),
                                      ('/deldepartment', DelDepartmentPage),
                                      ('/delemployee', DelEmployeePage),
                                      ('/.*', ErrorPage)],
                                     debug=True)
    

def main():
  run_wsgi_app(application)
  
if __name__ == "__main__":
  main()

