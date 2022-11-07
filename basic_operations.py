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

table_name = "sql12550679"