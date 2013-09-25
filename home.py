import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *
import datetime
import copy
import json
from timezone import USTimeZone
    
def get_date(request):
  if request.date is not None:
    return request.date

  mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
  date = datetime.datetime.now(mountain).date()
    
  return date
  
def get_user():
  google_user = users.get_current_user()
  user = UserRecord.gql("WHERE user_id = :1", google_user.user_id())
  user = user.get()
  if user is None:
    user = UserRecord()
    user.user_id = google_user.user_id()
    user.put()
  return user  

def get_day(user, date):
  day = DayRecord.all().filter("date =", date).filter("user =", user.key()).fetch(1)
  if len(day) == 0:
    day = DayRecord()
    day.user = user
    day.date = date
    day.put()
  else:
    day = day[0]
  
  return day

class MainPage(webapp2.RequestHandler):
  def get(self):
    
    user = get_user()
      
    date = get_date(self.request)

    day = get_day(user, date)

    items = ItemRecord.all().filter("day =", day.key()).fetch(50)

    self.response.out.write(template.render("templates/index.html", {'items': items, 'today': date}))
    
  def post(self):
    user = get_user()
    date = get_date(self.request)
    day = get_day(user, date)

    item = ItemRecord()
    item.day = day
    item.item = self.request.params['item']
    item.amount = self.request.params['amount']
    item.quality = int(self.request.params['quality'])
    item.put()

    self.redirect("/")
    
app = webapp2.WSGIApplication([
  ('/', MainPage), 
  # ('/submit', SubmitPage)
  ], 
debug=True)