def is_float(testfloat):
	try:
		float(testfloat)
		return True
	except ValueError:
		return False

def is_int(testint):
	try:
		int(testint)
		return True
	except ValueError:
		return False
		

def get_name():
	import sqlite3
	conn = sqlite3.connect("tempData")
	c = conn.cursor()
	try:
		c.execute("SELECT * FROM host_connect_info")
		data = c.fetchall()

		if len(data) == 0:
			return None
		else:
			return data[0][3]
	except sqlite3.OperationalError:
		return None


#"sql12550679"