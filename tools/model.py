from datetime import datetime
import db
import perfectmind

def insert_all_attendance(last_updated):
  all_attendance = perfectmind.attendance(last_updated)
  for record in all_attendance:
    db.insert_attendance_record(record)

def insert_all_clients(last_updated):
  all_contacts = perfectmind.contacts(last_updated)
  for record in all_contacts:
    db.insert_contact_record(record)

def insert_all_transactions(last_updated):
  all_transactions = perfectmind.transactions(last_updated)
  for record in all_transactions:
    db.insert_transaction_record(record)

def insert_all_teachers(last_updated):
  all_teachers = perfectmind.teachers(last_updated)
  for record in all_teachers:
    db.insert_teacher_record(record)

def insert_all_events(last_updated):
  all_events = perfectmind.events(last_updated)
  for record in all_events:
    db.insert_event_record(record)

def insert_all():
  last_updated = perfectmind.last_updated()
  db.create()
  insert_all_attendance(last_updated)
  insert_all_clients(last_updated)
  insert_all_teachers(last_updated)
  insert_all_events(last_updated)

def beginning_of_month():
  now = datetime.now()
  return datetime(now.year, now.month, 1, 0, 0, 0)

def attendance(cur, from_date):
  epoch = int(from_date.strftime("%s"))
  return db.attendance_after_epoch(cur, epoch)

if __name__ == '__main__':
  perfectmind.login()
  insert_all()
