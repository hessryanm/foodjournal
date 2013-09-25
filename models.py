from google.appengine.ext import db

class UserRecord(db.Model):
  user_id = db.StringProperty()

class DayRecord(db.Model):
  user = db.ReferenceProperty(UserRecord)
  date = db.DateProperty()

class ItemRecord(db.Model):
  day = db.ReferenceProperty(DayRecord)
  item = db.TextProperty()
  amount = db.StringProperty()
  quality = db.IntegerProperty()