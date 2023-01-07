from tkinter import *
import mysql.connector
import database_view
import sqlite3
from tkinter import messagebox
import basic_operations
import datetime


class window:
	def __init__(self):
		self.vonn = sqlite3.connect("LocalData")
		self.v = self.vonn.cursor()



		self.state = "Login"
		self.fullscreen = False
		self.root = Tk()
		self.root.geometry("800x480")
		self.root.title("POS")
		self.root.attributes("-fullscreen", self.fullscreen)

		self.background_colour = "light blue"
		
		self.forground_colour = "white"

		self.createframes()
	
		self.start_login_frame()


		self.root.bind("<KP_Enter>",  lambda a: self.returnkey())
		self.root.bind("<Return>",  lambda a: self.returnkey())
		self.root.mainloop()


		
	def returnkey(self):
		if self.state == "Login":
			self.process_login()


	
	def createframes(self):
		self.login_frame = Frame(self.root, bg=self.background_colour, height = 480, width=800)
		self.login_frame.pack()

	
	def start_login_frame(self):
		self.login_frame_label = Label(self.login_frame, text="Enter Login Number", font=("Arial", 30), bg=self.background_colour, fg=self.forground_colour)
		self.login_frame_label.place(anchor=CENTER, relx= 0.5, rely = 0.3)

		self.login_frame_entry = Entry(self.login_frame, width = 25, font = ("Arial", 25))
		self.login_frame_entry.place(anchor=CENTER, relx=0.5, rely=0.4)
		self.login_frame_entry.focus()
		
		self.login_frame_button = Button(self.login_frame, text="Login", width = 10, height= 2, font = ("Arial", 25), command = self.process_login)
		self.login_frame_button.place(anchor=CENTER, relx=0.5, rely=0.6)

		self.login_frame_button_open_settings = Button(self.login_frame, text="Open Databse", bg=self.background_colour, width=15, height=2, command=self.open_databse_viewer)
		self.login_frame_button_open_settings.place(anchor=SE, relx=0.95, rely=0.95)

		self.fullscreen_button = Button(self.login_frame, text="Toggle Screen", width = 10, height= 2, font = ("Arial", 15), command = self.toggle_screen)
		self.fullscreen_button.place(anchor=CENTER, relx=0.1, rely=0.05)
		
	
	def toggle_screen(self):
		if self.fullscreen == False:
			self.root.attributes("-fullscreen", True)
			self.fullscreen = True
			self.root.geometry("800x480")
		else:
			self.root.geometry("800x480")
			self.root.attributes("-fullscreen", False)
			self.fullscreen = False
			

	def process_login(self):
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
			except Exception as e:
				messagebox.showerror(title="Error :(", message=e)
				return False

		self.c = self.conn.cursor()
		self.v.execute("SELECT * FROM settings WHERE name = 'registerid'")
		self.data = self.v.fetchall()
		self.c.execute("SELECT * FROM general_ledger_place WHERE place_name = %s", [self.data[0][1]])
		self.data = self.c.fetchall()
		if len(self.data) != 1:
			messagebox.showerror(title="Error :(", message="Please declare/redeclare this register")
		else:
			self.c = self.conn.cursor()
			self.c.execute("SELECT * FROM user WHERE id = %s", [self.login_frame_entry.get()])
			self.data = self.c.fetchall()
			if len(self.data) == 1:

				self.v.execute("SELECT * FROM settings WHERE name = 'registerid'")
				if len(self.v.fetchall()) == 1:
					self.v.execute("DROP TABLE if exists login_info")
					self.v.execute("CREATE TABLE login_info(user_id TEXT, username TEXT, permissions TEXT)")
					self.v.execute("INSERT INTO login_info(user_id, username, permissions) VALUES(?, ?, ?)", [self.data[0][0], self.data[0][1], self.data[0][3]])
					self.state = "Invoice"
					self.vonn.commit()
					self.root.destroy()
					self.root.quit()
					

					

				else:
					messagebox.showerror(title="Error :(", message="Please initialise this register")
			return True

	def open_databse_viewer(self):
		database_view.run()

		
		return	True
