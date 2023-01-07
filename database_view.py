
import admin_access
from tkinter import *
import login_window
from tkinter import messagebox
import sqlite3
import database_editor
import basic_operations
import setting

fg = "blue"

class DatabaseView():
	def __init__(self):
		self.vonn = sqlite3.connect("LocalData")
		self.v = self.vonn.cursor()
		
		self.root = Tk()
		self.root.title("Database Manager")
		self.root.geometry("500x500+0+0")
		self.power = 0
		#Label title
		self.label=Label(self.root, text="Databse Manager", font=("Arial", 20))
		self.label.place(anchor=CENTER, relx=0.5, rely =0.04)
		#Buttons
		self.admin_access_button = Button(self.root, text="Admin Access", command= self.admin_access, fg='blue')
		self.admin_access_button.place(anchor=CENTER, relx=0.5, rely=0.1)

		self.login_button = Button(self.root, text="Login", command = self.login, fg='blue')
		self.login_button.place(anchor=CENTER, relx=0.5, rely=0.175)

		self.delete_tempdata_button = Button(self.root, text="Delete Local Data", command=self.delete_tempdata, fg='red')
		self.delete_tempdata_button.place(anchor=CENTER, relx=0.5, rely=0.25)

		#Row 2
		self.local_settings_button = Button(self.root, text="Local Settings", command = self.local_settings, fg='red')
		self.local_settings_button.place(anchor=CENTER, relx=0.5, rely=0.325)

		self.global_settings_button = Button(self.root, text="Global Settings", command = self.global_settings, fg='red')
		self.global_settings_button.place(anchor=CENTER, relx=0.5, rely=0.4)

		self.contact_developer_button = Button(self.root, text="Contact Developer", command = self.contact_developer, fg='blue')
		self.contact_developer_button.place(anchor=CENTER, relx=0.5, rely=0.475)

		self.view_tables_button = Button(self.root, text="Table Viewer",fg='red', command=self.view_tables)
		self.view_tables_button.place(anchor=CENTER, relx = 0.5, rely= 0.625)

		self.statistics_button = Button(self.root, text="Statistics Viewer",fg='red', command=self.view_statistics)
		self.statistics_button.place(anchor=CENTER, relx = 0.5, rely= 0.7)

		Button(self.root, text = "Logout", command=self.logout,fg='blue').place(anchor=CENTER, relx=0.5, rely=0.8)
		




		Label(self.root, text="Logged In As:", font=("Arial", 20)).place(anchor=CENTER, relx=0.2, rely =0.9)
		self.userEntry = Entry(self.root, font=("Arial", 20))
		self.userEntry.place(anchor=CENTER, relx = 0.6, rely=0.9)
		self.userEntry.config(state = DISABLED)

		self.root.mainloop()




	def view_tables(self):
		if self.view_tables_button.cget('fg') == "blue":
			database_editor.view_database()
		return True
	


	def contact_developer(self):
		messagebox.showerror(message="Contact Developer:\nEmail: nicholasjbond2020@gmail.com")

	def local_settings(self):
		setting.LocalSettings()
		if self.local_settings_button.cget('fg') == "blue":
			pass
		

	def global_settings(self):
		if self.global_settings_button.cget('fg') == "blue":
			("Comming Soon")

	def view_statistics(self):
		if self.view_tables_button.cget('fg') == "blue":
			print("Coming Soon")


	def delete_tempdata(self):
		if self.delete_tempdata_button.cget('fg') == "blue":
			self.v.execute("DROP table host_connect_info")
			self.power = "000000000000000000000000000000"
			self.update_buttons()

	def logout(self):
		self.v.execute("DROP TABLE login_info")
		self.vonn.commit()
		self.power ="000000000000000000000000000000"
		self.update_buttons()
		self.userEntry.config(state = NORMAL)
		self.userEntry.delete(0, END)
		self.userEntry.config(state = DISABLED)
	def login(self):
		login_window.login()

		try:
			self.v.execute("SELECT * FROM login_info")
			self.data = self.v.fetchall()
			self.power =self.data[0][2]
			self.update_buttons()
			self.userEntry.config(state = NORMAL)
			self.userEntry.delete(0, END)
			self.userEntry.insert(0, self.data[0][1])
			self.userEntry.config(state = DISABLED)
		except sqlite3.OperationalError:
			pass
		

	def update_buttons(self):
		
		self.button_active(self.delete_tempdata_button, 0)
		self.button_active(self.local_settings_button, 5)
		self.button_active(self.global_settings_button, 6)
		self.button_active(self.statistics_button, 7)
		if self.power[1] == "1" or self.power[2] == "1" or self.power[3] == "1" or self.power[4] == "1":
			self.view_tables_button.config(fg = "blue")
		else:
			self.view_tables_button.config(fg = "red")
		#other power goes up to 29 starting at 0,  (30 total)


		

	def button_active(self, button, power):
		
		if self.power[power] == "1":

			button.config(fg = "blue")
			
		else:
			button.config(fg = "red")

	def admin_access(self):
		admin_access.Connect()
		


def run():
	DatabaseView()








