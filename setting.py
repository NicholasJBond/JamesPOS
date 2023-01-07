import mysql.connector
from tkinter import *
from tkinter import messagebox
import basic_operations
import sqlite3

class LocalSettings():
	def __init__(self):
		self.root = Tk()
		self.root.title("Local Settings")
		self.root.geometry("500x500+0+0")
		self.vonn =sqlite3.connect("LocalData")
		self.v = self.vonn.cursor()

		Label(self.root, text = "Local Settings", font=("Arial", 25)).place(anchor = CENTER, relx = 0.5, rely = 0.1)
		self.register_name = Entry(self.root)
		self.register_name.place(anchor = CENTER, relx = 0.5, rely = 0.25)
		
		self.initialisation_button =Button(self.root, text = "Initialise Register", command = self.registerinit)
		self.initialisation_button.place(anchor = CENTER, relx = 0.5, rely = 0.32)
		self.check_initialisation()

		self.close_button = Button(self.root, text="❌", command=self.close)
		self.close_button.place(anchor=CENTER, relx=0.5, rely=0.9)

		

		

	
		self.root.bind("<KeyPress>", lambda a: self.check_entry())
		self.root.mainloop()
		return None

	def check_initialisation(self):
		self.v.execute("CREATE TABLE IF NOT EXISTS settings(name TEXT, value TEXT)")
		self.v.execute("SELECT * FROM settings WHERE name = ?", ["registerid"])
		self.data = self.v.fetchall()

		if len(self.data) == 1: 
			self.register_name.delete(0, END)
			self.register_name.insert(0, self.data[0][1])
			self.register_name.config(state=DISABLED)
			self.initialisation_button.config(text="Deinitialise Register")
			self.initialised = True
		else:
			self.initialisation_button.config(text="Initialise Register")
			self.register_name.focus()
			self.initialised = False
		self.vonn.commit()

	def registerinit(self):
		self.v.execute("SELECT * FROM host_connect_info")
		self.data= self.v.fetchall()
		if len(self.data) == 0:
			messagebox.showerror(title="Error :(", message="Please connect to host")
			return False
		else:

			try:
				self.conn = mysql.connector.connect(
					host=self.data[0][0],
					user=self.data[0][1],
					passwd=self.data[0][2],
					database=self.data[0][3]
				)
				self.c=self.conn.cursor()
			except Exception as e:
				messagebox.showerror(title="Error :(", message=e)
				return False

		if self.register_name.get() != "":
			if self.initialised:
				self.v.execute("DELETE FROM settings WHERE name = 'registerid'")
				self.register_name.config(state=NORMAL)
				self.register_name.delete(0, END)
			else:
				self.c.execute("SELECT * FROM general_ledger_place WHERE place_name = %s", [self.register_name.get()])
				if len(self.c.fetchall()) == 0:
					self.v.execute("INSERT INTO settings(name, value) VALUES('registerid', ?)", [self.register_name.get()])
					self.c.execute("SELECT * FROM general_ledger_place ORDER BY place_id DESC LIMIT 1")
					self.data=self.c.fetchall()
					if len(self.data) == 1:
						self.id = int(self.data[0][0])+1
					else:
						self.id = 0
					self.c.execute("INSERT INTO general_ledger_place(place_id, place_name, value, location) VALUES(%s, %s, %s, 'registers')", [self.id, self.register_name.get(), 0])
					self.conn.commit()
				else:
					self.register_name.delete(0, END)
					return False
		self.vonn.commit()
		self.check_initialisation()

		

	def check_entry(self):
		self.entry = str(self.register_name.get())
		try:
			self.entry[1]
			self.register_name.delete(1, END)
		except IndexError:
			pass

	def close(self):
		self.root.destroy()
		self.root.quit()
		return True
