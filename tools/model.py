from datetime import datetime
import db
import perfectmind

def insert_all_attendance():
  all_attendance = perfectmind.attendance()
  for record in all_attendance:
    db.insert_attendance_record(record)

def insert_all_clients():
  all_contacts = perfectmind.contacts()
  for record in all_contacts:
    db.insert_contact_record(record)

def insert_all_transactions():
  all_transactions = perfectmind.transactions()
  for record in all_transactions:
    db.insert_transaction_record(record)

def insert_all_teachers():
  all_teachers = perfectmind.teachers()
  for record in all_teachers:
    db.insert_teacher_record(record)

def insert_all_events():
  all_events = perfectmind.events()
  for record in all_events:
    db.insert_event_record(record)

def insert_all():
  insert_all_attendance()
  insert_all_clients()
  insert_all_transactions()
  insert_all_teachers()
  insert_all_events()

def beginning_of_month():
  now = datetime.now()
  return datetime(now.year, now.month, 1, 0, 0, 0)

def attendance(from_date):
  epoch = int(from_date.strftime("%s"))
  results = db.attendance_after_epoch(epoch)
  print(results)

if __name__ == '__main__':
  db.create()
  insert_all()
