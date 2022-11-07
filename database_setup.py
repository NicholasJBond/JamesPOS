import mysql.connector
from tkinter import *
from tkinter import messagebox


class ConnectToHost:

	def submit_command(self):
		if self.hostE.get() != "":
			if self.userE.get() != "":
				if self.passwdE.get() != "":
					self.host = self.hostE.get()
					self.user = self.userE.get()
					self.passwd = self.passwdE.get()
					try:
						conn = mysql.connector.connect(
							host=self.host,
							user=self.user,
							passwd=self.passwd,
							
						)
						self.host_details=[self.host, self.user, self.passwd]
						self.root.destroy()
						
						self.root.quit()
						
					except mysql.connector.errors.InterfaceError:
						messagebox.showerror(title="Error :(", message="Cannot connect to host")
						self.hostE.delete(0, END)
						self.hostE.focus()

					except mysql.connector.errors.ProgrammingError:
						messagebox.showerror(title="Error :(", message="Incorrect username or password")
						self.userE.delete(0, END)
						self.passwdE.delete(0, END)
						self.userE.focus()

					except:
						messagebox.showerror(title="Error :(", message=":( Something went wrong")
					
					

				else:
					self.passwdE.focus()
			else:
				self.userE.focus()
		else:
			self.hostE.focus()
			

		
		return True
	def __init__(self):
		self.x = 0
		self.root = Tk()
		self.root.geometry("500x500")
		self.root.title("Connect to host")

		self.hostL = Label(self.root, text="Host")
		self.hostL.place(anchor=CENTER, relx = 0.5, rely=0.2)
		self.hostE = Entry(self.root, width=25)
		self.hostE.place(anchor=CENTER, relx = 0.5, rely=0.25)
		self.hostE.focus()

		self.userL = Label(self.root, text="Username")
		self.userL.place(anchor=CENTER, relx = 0.5, rely=0.4)
		self.userE = Entry(self.root, width=25)
		self.userE.place(anchor=CENTER, relx = 0.5, rely=0.45)

		self.a = 5

		self.passwdL = Label(self.root, text="Password")
		self.passwdL.place(anchor=CENTER, relx = 0.5, rely=0.6)
		self.passwdE = Entry(self.root, width=25, show="•", font=("Arial", 15))
		self.passwdE.place(anchor=CENTER, relx = 0.5, rely=0.65)
		self.submit = Button(self.root, text="Submit", command = lambda:self.submit_command())
		self.submit.place(anchor=CENTER, relx = 0.5, rely = 0.8)
		self.root.bind("<Return>", lambda a:self.submit_command())
		self.root.mainloop()
	
class CreateDatabase:
	def __init__(self, host, user, passwd):
		self.root = Tk()
		self.root.geometry("500x500")
		self.root.title("Create Database")
		self.host=host
		self.user=user
		self.passwd=passwd
		self.conn = mysql.connector.connect(
			host=self.host,
			user=self.user,
			passwd=self.passwd,
			
		)
		self.c = self.conn.cursor()
		self.label = Label(self.root, text="Configure Databse", font=("Arial", 25))
		self.label.place(anchor=CENTER, relx=0.5, rely=0.075)

		self.create_database_button = Button(self.root, text="Select/Create Database", command = self.create_database, height=3, width=25)
		self.create_database_button.place(anchor=CENTER, relx = 0.5, rely=0.2)

		self.create_tables_button = Button(self.root, text="Create Tables", command = self.create_table, height=3, width=25)
		self.create_tables_button.place(anchor=CENTER, relx = 0.5, rely=0.35)

		self.create_admin_button = Button(self.root, text="Create Admin User", command = self.create_admin, height=3, width=25)
		self.create_admin_button.place(anchor=CENTER, relx = 0.5, rely=0.5)

		self.alert_entry = Entry(self.root, fg="red", font=("Arial", 20))
		self.alert_entry.place(anchor=CENTER, relx=0.5, rely =0.8)
		self.alert_entry.configure(state=DISABLED)

		self.close_button = Button(self.root, text="❌", command=self.close)
		self.close_button.place(anchor=CENTER, relx=0.5, rely=0.9)



		self.root.mainloop()

	def close(self):
		self.root.destroy()
		self.root.quit()
	def create_database(self):
		
		
		try:
			self.c.execute("CREATE DATABASE JamesPOS")

		except mysql.connector.errors.DatabaseError:
			pass

		self.alert_entry.configure(state=NORMAL)
		self.alert_entry.delete(0, END)
		self.alert_entry.insert(0, "Connecting to Databse")
		self.alert_entry.configure(state=DISABLED)
		self.database = "JamesPOS"

		try:
			self.conn = mysql.connector.connect(
				host=self.host,
				user=self.user,
				passwd=self.passwd,
				database=self.database
				
			)
			self.c = self.conn.cursor()
			self.alert_entry.configure(state=NORMAL)
			self.alert_entry.delete(0, END)
			self.alert_entry.insert(0, "Connection Successful!")
			self.alert_entry.configure(state=DISABLED)

		except:
			self.alert_entry.configure(state=NORMAL)
			self.alert_entry.delete(0, END)
			self.alert_entry.insert(0, "Error! Could not connect")
			self.alert_entry.configure(state=DISABLED)
	 
		return True
	def create_table(self):
		
		try:
			self.c.execute("CREATE table user(id TEXT, name TEXT, password TEXT, permissions TEXT)")
			self.c.execute("CREATE table items(plu TEXT, description TEXT, type INT, category TEXT, points INT, price REAL, quantity REAL)")
			self.c.execute("CREATE table transactions(id INT, date_s TEXT, time_s TEXT, total REAL, payment TEXT, account TEXT, reward TEXT, total_rewards INT)")
			self.c.execute("CREATE table transaction_details(id INT, plu TEXT, description TEXT, quantity REAL, price REAL, points INT)")
			self.c.execute("CREATE table accounts(id INT, name TEXT, value REAL, credit_limit REAL, email TEXT, phone TEXT)")
			self.c.execute("CREATE table rewards(id INT, name TEXT, value REAL, phone TEXT, email TEXT)")
			self.c.execute("CREATE table settings(name TEXT, value TEXT)")
			self.alert_entry.configure(state=NORMAL)
			self.alert_entry.delete(0, END)
			self.alert_entry.insert(0, "Success")
			self.alert_entry.configure(state=DISABLED)

		except mysql.connector.errors.ProgrammingError:
			
			try:
				self.c.execute("INSERT INTO user(id, name, password, permissions) VALUES(%s, %s, %s, %s)", ["a", "a", "a", "a"])
				self.c.execute("DELETE FROM user WHERE id ='a'")
				self.conn.commit()
				self.alert_entry.configure(state=NORMAL)
				self.alert_entry.delete(0, END)
				self.alert_entry.insert(0, "Success")
				self.alert_entry.configure(state=DISABLED)

			except:
				self.alert_entry.configure(state=NORMAL)
				self.alert_entry.delete(0, END)
				self.alert_entry.insert(0, "No Database Selected")
				self.alert_entry.configure(state=DISABLED)
	def create_admin(self):
		
		try:
			self.c.execute("SELECT * FROM user WHERE id = 0")
			self.admin_user = self.c.fetchall()
			if self.admin_user == []:
				self.c.execute("INSERT INTO user(id, name, password, permissions) VALUES(%s, %s, %s, %s)", ["0", "admin", "root", "111111111111111111111111111111"])
				self.conn.commit()
				messagebox.showinfo(title = "Admin User", message="ID = 0\nNAME = admin\nPASSWORD = root")
			else:
				self.c.execute("UPDATE user SET permissions = %s WHERE id = %s", ["111111111111111111111111111111", "0"])
				self.conn.commit()
				messagebox.showinfo(title = "Admin User", message=f"ID = 0\nNAME = {self.admin_user[0][1]}\nPASSWORD = {self.admin_user[0][2]}")
		except:
			messagebox.showinfo(message="Error: Try selecting a databse or making a table")
		
		return True

def connect():
	
	connect_window = ConnectToHost()
	
	return connect_window.host_details

def create(host, user, passwd):
	create_window = CreateDatabase(host ,user , passwd)




