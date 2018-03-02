from config import *
from datetime import datetime
import os
import sqlite3

attendance_table = 'attendance'
clients_table = 'clients'
events_table = 'events'
transactions_table = 'transactions'
teachers_table = 'teachers'
genders_table = 'genders'
membership_status_table = 'membership_status'

all_tables = [
	attendance_table,
	clients_table,
	events_table,
	transactions_table,
	teachers_table,
	genders_table,
	membership_status_table,
]

table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
count_query = "SELECT count(*) FROM {};"

config = Config.load()

conn = sqlite3.connect(config.database)
cur = conn.cursor()

def table_exists(table):
	query = table_query.format(table)
	result = cur.execute(query)
	rows = result.fetchall()
	return len(rows) > 0

def table_has_data(table):
	query = count_query.format(table)
	result = cur.execute(query)
	row = result.fetchone()
	return int(row[0]) > 0


def tables_exist():
	for table in all_tables:
		if table_exists(table) and table_has_data(table):
			return True
	return False

def attendance_after_epoch(cur, time):
	cur.execute("""
		SELECT c.FullName, count(*) as ClassCount
		FROM clients c, attendance a, events e
		WHERE a.Attendee = c.ID and a.Event = e.ID and a.TimeAttended > ?
		GROUP BY c.ID
		ORDER BY ClassCount desc;""", (time,))
	rows = cur.fetchall()
	json_resp = []
	for row in rows:
		json_resp.append( { 'name': row[0], 'attendance': row[1] } )
	return json_resp

def insert_attendance_record(record):
	cur.execute("""INSERT INTO attendance (
		Attendee,
		Event,
		ModifiedDate,
		Renewed,
		Status,
		TimeAttended,
		Transactions
	) VALUES (?, ?, ?, ?, ?, ?, ?);""",
		(record.get('Attendee'),
		record.get('Event'),
		epoch(record.get('ModifiedDate')),
		record.get('Renewed'),
		record.get('Status'),
		epoch(record.get('TimeAttended')),
		record.get('Transactions'))
	)
	cur.connection.commit()

def epoch(text):
	if text is None or len(text) == 0:
		return None
	date_object = datetime.strptime(
		text.split('.')[0],
		'%Y-%m-%dT%H:%M:%S')
	return int(date_object.strftime("%s"))

def gender(text):
	if text is None or len(text) == 0:
		return 0
	lower_case = text.lower()
	if lower_case == 'male':
		return 1
	if lower_case == 'female':
		return 2
	return 0

def membership_status(text):
	if text is None or len(text) == 0:
		return 0
	lower_case = text.lower()
	if lower_case == 'active':
		return 1
	if lower_case == 'cancelled':
		return 2
	if lower_case == 'expired':
		return 3
	if lower_case == 'freeze':
		return 4
	return 0

def phone_number(text):
	if text is None or len(text) == 0:
		return 0
	return int(text.replace('-', '').replace(' ', ''))

def insert_contact_record(record):
	cur.execute("""INSERT INTO clients (
		ID,
		FullName,
		Gender,
		Email,
		Birthdate,
		Membership,
		PerfectScanID,
		CreatedDate,
		StartDate,
		EnrollmentDate,
		LastAttended,
		Photo,
		PrimaryNumber
	) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
		(record.get('ID'),
		record.get('FullNameSimple'),
		gender(record.get('Gender')),
		record.get('Email'),
		epoch(record.get('Birthdate')),
		record.get('Membership'),
		record.get('PerfectScanID'),
		epoch(record.get('CreatedDate')),
		epoch(record.get('StartDate')),
		epoch(record.get('EnrollmentDate')),
		epoch(record.get('LastAttended')),
		record.get('Photo'),
		record.get('PrimaryNumber'))
	)
	cur.connection.commit()

def insert_transaction_record(record):
	cur.execute("""INSERT INTO transactions (
		CreatedDate,
		DurationDays,
		EachPayment,
		Expiry,
		FinalPayment,
		FirstPayment,
		ForfeitedAmount,
		ID,
		MembershipName,
		MembershipStatus,
		MembershipTotal,
		ModifiedDate,
		NumberofPayments,
		Ongoing,
		SessionsLeft,
		SessionsPurchased,
		TotalAmount
	) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
		(epoch(record.get('CreatedDate')),
		record.get('DurationDays'),
		record.get('EachPayment'),
		epoch(record.get('Expiry')),
		epoch(record.get('FinalPayment')),
		epoch(record.get('FirstPayment')),
		record.get('ForfeitedAmount'),
		record.get('ID'),
		record.get('MembershipName'),
		membership_status(record.get('MembershipStatus')),
		record.get('MembershipTotal'),
		epoch(record.get('ModifiedDate')),
		record.get('NumberofPayments'),
		record.get('Ongoing'),
		record.get('SessionsLeft'),
		record.get('SessionsPurchased'),
		record.get('TotalAmount'))
	)
	cur.connection.commit()

def insert_teacher_record(record):
	cur.execute("""INSERT INTO teachers (
		CreatedDate,
		Email,
		FullName,
		ID,
		JobTitle,
		MobilePhone,
		ModifiedDate,
		Position
	) VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
		(epoch(record.get('CreatedDate')),
		record.get('Email'),
		record.get('FullName'),
		record.get('ID'),
		record.get('JobTitle'),
		phone_number(record.get('MobilePhone')),
		epoch(record.get('ModifiedDate')),
		record.get('Position'))
	)
	cur.connection.commit()

def insert_event_record(record):
	cur.execute("""INSERT INTO events (
		CreatedDate,
		Details,
		EndTime,
		ID,
		Price,
		StartTime,
		Subject,
		Teacher
	) VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
		(epoch(record.get('CreatedDate')),
		record.get('Details'),
		epoch(record.get('EndTime')),
		record.get('Id'),
		record.get('Price'),
		epoch(record.get('StartTime')),
		record.get('Subject'),
		record.get('Teacher'))
	)
	cur.connection.commit()

def create():
	# Make sure the tables are not already populated.
	if tables_exist():
		return

	# Create the tables.
	cur.execute("""CREATE TABLE IF NOT EXISTS genders (
		id INTEGER,
		gender TEXT
	);""")

	cur.execute("INSERT INTO genders VALUES (1, 'Male');")
	cur.execute("INSERT INTO genders VALUES (2, 'Female');")

	cur.execute("""CREATE TABLE IF NOT EXISTS clients (
		ID TEXT,
		FullName TEXT,
		Gender INTEGER,
		Email TEXT,
		Birthdate INTEGER,
		Membership TEXT,
		PerfectScanID TEXT,
		CreatedDate INTEGER,
		StartDate INTEGER,
		EnrollmentDate INTEGER,
		LastAttended INTEGER,
		Photo TEXT,
		PrimaryNumber INTEGER
	);""")

	cur.execute("""CREATE TABLE IF NOT EXISTS membership_status (
		id INTEGER,
		status TEXT
	);""")

	cur.execute("INSERT INTO membership_status VALUES (1, 'Active');")
	cur.execute("INSERT INTO membership_status VALUES (2, 'Cancelled');")
	cur.execute("INSERT INTO membership_status VALUES (3, 'Expired');")
	cur.execute("INSERT INTO membership_status VALUES (4, 'Freeze');")

	cur.execute("""CREATE TABLE IF NOT EXISTS transactions (
		CreatedDate INTEGER,
		DurationDays INTEGER,
		EachPayment REAL,
		Expiry INTEGER,
		FinalPayment INTEGER,
		FirstPayment INTEGER,
		ForfeitedAmount REAL,
		ID TEXT,
		MembershipName TEXT,
		MembershipStatus INTEGER,
		MembershipTotal REAL,
		ModifiedDate INTEGER,
		NumberofPayments REAL,
		Ongoing BOOL,
		SessionsLeft INTEGER,
		SessionsPurchased INTEGER,
		TotalAmount REAL
	);""")

	cur.execute("""CREATE TABLE IF NOT EXISTS attendance (
		Attendee TEXT,
		Event TEXT,
		ModifiedDate INTEGER,
		Renewed BOOL,
		Status TEXT,
		TimeAttended INTEGER,
		Transactions TEXT
	);""")

	cur.execute("""CREATE TABLE IF NOT EXISTS events (
		CreatedDate INTEGER,
		Details TEXT,
		EndTime INTEGER,
		ID TEXT,
		Price	REAL,
		StartTime INTEGER,
		Subject	TEXT,
		Teacher	TEXT
	);""")


	cur.execute("""CREATE TABLE IF NOT EXISTS teachers (
		CreatedDate	INTEGER,
		Email TEXT,
		FullName TEXT,
		ID TEXT,
		JobTitle TEXT,
		MobilePhone INTEGER,
		ModifiedDate INTEGER,
		Position TEXT
	);""")

	cur.connection.commit()

if __name__ == '__main__':
  create()

