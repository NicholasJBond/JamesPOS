import mysql.connector
from tkinter import *
from tkinter import messagebox
import basic_operations
import sqlite3

class Connect:
	def __init__(self):
		self.root = Tk()
		self.root.title("Admin Access")
		self.root.geometry("500x500+0+0")

		Label(self.root, text="Host").place(anchor=CENTER, relx=0.5, rely=0.05)
		Label(self.root, text="Username").place(anchor=CENTER, relx=0.5, rely=0.25)
		Label(self.root, text="Password").place(anchor=CENTER, relx=0.5, rely=0.45)
		Label(self.root, text="Database Name").place(anchor=CENTER, relx=0.5, rely=0.65)
		Label(self.root, text="Database Name").place(anchor=CENTER, relx=0.5, rely=0.65)


		self.host_entry = Entry(self.root, width = 40)
		self.host_entry.place(anchor=CENTER, relx=0.5, rely=0.1)
		self.host_entry.insert(0, "s05ge.syd5.hostingplatform.net.au")
		self.host_entry.focus()


		self.username_entry = Entry(self.root, width = 40)
		self.username_entry.place(anchor=CENTER, relx=0.5, rely=0.3)

		self.password_entry = Entry(self.root, width = 40, show="*")
		self.password_entry.place(anchor=CENTER, relx=0.5, rely=0.5)

		self.databasename_entry = Entry(self.root, width = 40)
		self.databasename_entry.place(anchor=CENTER, relx=0.5, rely=0.7)

		Button(self.root, text="Go", command=self.returnkey).place(anchor=CENTER, relx=0.5, rely=0.9)



		self.host_entry.bind("<Double-Button-1>", lambda a: self.host_entry.delete(0, END))
		self.root.bind("<Return>", lambda i:self.returnkey())
		self.root.mainloop()
		return None

	def returnkey(self):
		if self.host_entry.get() == "":
			self.host_entry.focus()
		elif self.username_entry.get() == "":
			self.username_entry.focus()
		elif self.password_entry.get() == "":
			self.password_entry.focus()
		elif self.databasename_entry.get() == "":
			self.databasename_entry.focus()
		else:
			self.go()
	
		

	def go(self):
		self.connection_attempt = False
		try:
			self.conn = mysql.connector.connect(
				host=self.host_entry.get(),
				user=self.username_entry.get(),
				passwd=self.password_entry.get(),
				
			)
			self.connection_attempt = True
		except mysql.connector.errors.InterfaceError:
			messagebox.showerror(title="Error :(", message="Host Incorrect")
			self.host_entry.delete(0, END)
			self.host_entry.focus()

		except mysql.connector.errors.ProgrammingError:
			messagebox.showerror(title="Error :(", message="Username or Password Incorrect")
			self.username_entry.delete(0, END)
			self.password_entry.delete(0, END)
			self.username_entry.focus()

		if self.connection_attempt:
			self.connection_attempt = False
			try:
				self.conn = mysql.connector.connect(
					host=self.host_entry.get(),
					user=self.username_entry.get(),
					passwd=self.password_entry.get(),
					database=self.databasename_entry.get()
				)
				self.c = self.conn.cursor()
				messagebox.showinfo(title="Success :)", message="Successfully connected to database")
				self.connection_attempt = True
			except mysql.connector.errors.ProgrammingError:
				try:
					try:
						self.c=self.conn.cursor()
						self.c.execute(f"CREATE DATABASE {self.databasename_entry.get()}")
						self.conn = mysql.connector.connect(
							host=self.host_entry.get(),
							user=self.username_entry.get(),
							passwd=self.password_entry.get(),
							database=self.databasename_entry.get()
						)
						self.c=self.conn.cursor()
						self.c.execute("CREATE table user(id TEXT, name TEXT, password TEXT, permissions TEXT)")
						self.c.execute("CREATE table items(plu TEXT, description TEXT, type INT, category TEXT, points INT, price REAL, quantity REAL)")
						self.c.execute("CREATE table transactions(id int, date_s TEXT, time_s TEXT, total REAL, gst REAL, payment_method TEXT, loyalty_id TEXT, discounts REAL, amount_recieved REAL, location TEXT, user_id TEXT)")
						self.c.execute("CREATE table transaction_items(id int, plu TEXT, description TEXT, quantity REAL, total REAL, gst REAL, shelf_price REAL, points INT)")
						self.c.execute("CREATE table accounts(id TEXT, name int, value REAL, credit_limit REAL, points INT, email TEXT, phone TEXT)")
						self.c.execute("CREATE table settings(name TEXT, value TEXT)")
						self.c.execute("CREATE table general_ledger(id int, amount REAL, from_id TEXT, to_id TEXT, time_s TEXT, date_s TEXT, user_id TEXT)")
						self.c.execute("CREATE table general_ledger_place(place_id int, place_name TEXT, value REAL, location TEXT)")
						self.c.execute("CREATE table vender(id int, name TEXT, BSB TEXT, accoun_num TEXT, ABN INT, period TEXT, location TEXT, contact TEXT)")
						self.c.execute("CREATE table purchase_order(id int, date_s TEXT, time_s TEXT, total REAL, gst REAL, vender TEXT, user_id TEXT, status TEXT)")
						self.c.execute("CREATE table purchase_order_items(id int, plu TEXT, description TEXT, quantity REAL, price REAL)")
						self.c.execute("CREATE table vender_ledger_POs(PO_id int, vender_id TEXT, amount REAL, gst REAL, time_s TEXT, date_s TEXT, user_id TEXT, due_date TEXT)")
						self.c.execute("CREATE table assets(id int, value REAL, purchased_value REAL, name TEXT, owner TEXT, invoice TEXT, depreciation REAL, tax_depreciation REAL)")
						self.conn.commit()

						messagebox.showinfo(title="Success :)", message=f"A new database has been created with the name '{self.databasename_entry.get()}'.\nThis database is brand new and does not contain any information.\nIf you were attempting to connect to an established database, please try again with a differend database name.")
						self.connection_attempt = True

					except Exception as e:
						messagebox.showerror(title="Error :(", message=e)

				except mysql.connector.errors.ProgrammingError:
					messagebox.showerror(title="Error :(", message="Database Name Incorrect")
					self.databasename_entry.delete(0, END)
					self.databasename_entry.focus()
					self.connection_attempt = False

			if self.connection_attempt:
				try:
					self.c.execute("SELECT * FROM user WHERE permissions = '111111111111111111111111111111'")
					self.data = self.c.fetchall()
					
				except mysql.connector.errors.ProgrammingError:
					self.c=self.conn.cursor()
					self.c.execute("CREATE table user(id TEXT, name TEXT, password TEXT, permissions TEXT)")
					self.c.execute("CREATE table items(plu TEXT, description TEXT, type INT, category TEXT, points INT, price REAL, quantity REAL)")
					self.c.execute("CREATE table transactions(id INT, date_s TEXT, time_s TEXT, total REAL, gst REAL, payment_method TEXT, loyalty_id TEXT, discounts REAL, amount_recieved REAL, location TEXT, user_id TEXT)")
					self.c.execute("CREATE table transaction_items(id INT, plu TEXT, description TEXT, quantity REAL, total REAL, gst REAL, shelf_price REAL, points INT)")
					self.c.execute("CREATE table accounts(id INT, name TEXT, value REAL, credit_limit REAL, points INT, email TEXT, phone TEXT)")
					self.c.execute("CREATE table settings(name TEXT, value TEXT)")
					self.c.execute("CREATE table general_ledger(id INT, amount REAL, from_id TEXT, to_id TEXT, time_s TEXT, date_s TEXT, user_id TEXT)")
					self.c.execute("CREATE table general_ledger_place(place_id INT, place_name TEXT, value REAL, location TEXT)")
					self.c.execute("CREATE table vender(id INT, name TEXT, BSB TEXT, accoun_num TEXT, ABN INT, period TEXT, location TEXT, contact TEXT)")
					self.c.execute("CREATE table purchase_order(id INT, date_s TEXT, time_s TEXT, total REAL, gst REAL, vender TEXT, user_id TEXT, status TEXT)")
					self.c.execute("CREATE table purchase_order_items(id INT, plu TEXT, description TEXT, quantity REAL, price REAL)")
					self.c.execute("CREATE table vender_ledger_POs(PO_id INT, vender_id TEXT, amount REAL, gst REAL, time_s TEXT, date_s TEXT, user_id TEXT, due_date TEXT)")
					self.c.execute("CREATE table assets(id INT, value REAL, purchased_value REAL, name TEXT, owner TEXT, invoice TEXT, depreciation REAL, tax_depreciation REAL)")
					self.conn.commit()

				self.c.execute("SELECT * FROM user WHERE permissions = '111111111111111111111111111111'")
				if len(self.c.fetchall()) == 0:

					if messagebox.askquestion ("Create User", "Would you like to create an admin user?", icon = 'info') == "yes":
						try:

							self.c.execute("INSERT INTO user(id, name, password, permissions) VALUES(%s, %s, %s, %s)", ["0", "admin", "root", "111111111111111111111111111111"])
							self.conn.commit()
							messagebox.showwarning(title="Admin User", message="UserID = 0\nPassword = root\nIt is recommended that you delete this user once a new user with a more secure password is created")

						except Exception as e:
							messagebox.showerror(title="Error :(", message=e)



				self.vonn = sqlite3.connect("LocalData")
				self.v = self.vonn.cursor()

				self.v.execute("DROP TABLE if exists host_connect_info")
				self.v.execute("CREATE TABLE host_connect_info(host TEXT, username TEXT, password TEXT, databasename TEXT)")
				self.v.execute("INSERT INTO host_connect_info(host, username, password, databasename) VALUES(?, ?, ?, ?)", [self.host_entry.get(), self.username_entry.get(), self.password_entry.get(), self.databasename_entry.get()])
				self.vonn.commit()
				self.root.destroy()
				self.root.quit()
				return None







