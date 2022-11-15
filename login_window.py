from tkinter import *
import mysql.connector
import basic_operations
from tkinter import messagebox
import sqlite3

class login():
	def __init__(self):
		self.vonn = sqlite3.connect("LocalData")
		self.v = self.vonn.cursor()
		try:
			self.v.execute("SELECT * FROM host_connect_info")
			self.data = self.v.fetchall()
			self.success = True
		except sqlite3.OperationalError:
			self.success = False
			messagebox.showerror(message = "Please Connect to a Server via Admin Access")

		if self.success:
			if len(self.data) == 0:
				messagebox.showerror(message = "Please Connect to a Server via Admin Access")
				self.success = False

			elif len(self.data) == 1:
				try:
					self.conn = mysql.connector.connect(
						host=self.data[0][0],
						user=self.data[0][1],
						passwd=self.data[0][2],
						database=self.data[0][3]
					)
					self.c = self.conn.cursor()
					self.success = True
				except Exception as e:
					messagebox.showerror(message = f"Error:{e}\nPossible Solutions:\n-Check your internet connection\n-Retry connecting to server via Admin Access\n-Email nicholasjbond2020@gmail.com")
					self.success = False
			else:
				messagebox.showerror(message = "Please Connect to a Server via Admin Access")
				self.success = False
				
			if self.success:
				self.root = Tk()
				self.root.title("Login")
				self.root.geometry("500x500+0+0")

				self.username_label = Label(self.root, text = "ID")
				self.username_label.place(anchor=CENTER, relx=0.5, rely=0.3)

				self.username_box = Entry(self.root, width = 25)
				self.username_box.place(anchor=CENTER, relx=0.5, rely=0.35)
				self.username_box.focus()

				self.password_label = Label(self.root, text = "Password")
				self.password_label.place(anchor=CENTER, relx=0.5, rely=0.45)

				self.password_box = Entry(self.root, width = 25, show="•")
				self.password_box.place(anchor=CENTER, relx=0.5, rely=0.5)

				self.submit_button = Button(self.root, text="Login", command = self.keyreturn)
				self.submit_button.place(anchor=CENTER, relx=0.5, rely=0.8)


				self.root.bind("<Return>", lambda a: self.keyreturn())
				self.root.mainloop()
		
		
		
		
		
	
	def keyreturn(self):
		if self.username_box.get() == "":
			self.username_box.focus()
		elif self.password_box.get() == "":
			self.password_box.focus()
		else:
			self.login()

	def login(self):
		self.c.execute("SELECT * FROM user WHERE id = %s", [self.username_box.get()])
		self.data = self.c.fetchall()
		if self.data == []:
			messagebox.showerror(message="Error:\nInvalid ID")
			self.username_box.delete(0, END)
			self.username_box.focus()
		else:
			if len(self.data) > 1:
				messagebox.showerror(message = "Urgent Error:\nMore than one user with the same id exists.\nPlease contact an Admin User for assistance")
			else:
				if self.data[0][2] == self.password_box.get():
					if basic_operations.is_int(self.data[0][3]) == True:
						self.v.execute("DROP TABLE if exists login_info")
						self.v.execute("CREATE TABLE login_info(user_id TEXT, username TEXT, permissions TEXT)")
						self.v.execute("INSERT INTO login_info(user_id, username, permissions) VALUES(?, ?, ?)", [self.data[0][0], self.data[0][1], self.data[0][3]])
						self.vonn.commit()
						self.root.destroy()
						print("hi")
						self.root.quit()
					else:
						messagebox.showerror(message = "Urgent Error:\nUsername and Password Correct.\nPermissions were unreadable, please ask and admin user to reset them for you")
					
				else:
					messagebox.showerror(message = "Error:\nInvalid Password")
					self.password_box.delete(0, END)
					self.password_box.focus()
				

		

# def login(host, usr, pas):
# 	try:
# 		window = login_view(host, usr, pas)
# 		var = window.power, window.username

# 	except mysql.connector.errors.ProgrammingError:
# 		var = -1
# 	except AttributeError:
# 		var = 0
# 		pass 
# 	return var

