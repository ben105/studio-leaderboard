from config import *
import studio
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
	print(rows)
	return len(rows) > 0

def table_has_data(table):
	query = count_query.format(table)
	result = cur.execute(query)
	row = result.fetchone()
	print(row)
	return int(row[0]) > 0


def tables_exist():
	for table in all_tables:
		print("Iterating over table: " + table)
		if table_exists(table) and table_has_data(table):
			raise Exception('{} table still has data in it, clear data before continuing.'.format(table))

def create_db():
	# Make sure the tables are not already populated.
	tables_exist()

	# Create the tables.
	cur.execute("""CREATE TABLE IF NOT EXISTS genders (
		id INTEGER,
		gender TEXT
	);""")

	cur.execute("INSERT INTO genders VALUES (1, 'Male');")
	cur.execute("INSERT INTO genders VALUES (2, 'Female');")

	cur.execute("""CREATE TABLE IF NOT EXISTS clients (
		client_id TEXT,
		full_name TEXT,
		gender INTEGER,
		email TEXT,
		birthdate INTEGER,
		membership TEXT,
		perfect_scan_id TEXT,
		created_date INTEGER,
		start_date INTEGER,
		enrollment_date INTEGER,
		last_attended INTEGER,
		photo TEXT,
		primary_number INTEGER
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
	create_db()
