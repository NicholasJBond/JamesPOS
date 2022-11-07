import mysql.connector
import database_setup
from tkinter import *
import login_window
from tkinter import messagebox
import sqlite3
import database_editor
import basic_operations

conn = sqlite3.connect("tempData")
v = conn.cursor()
v.execute("CREATE TABLE IF NOT EXISTS host_connect_info(host TEXT, usr TEXT, pas TEXT)")
conn.commit()
fg = "blue"

class DatabaseView():
	def __init__(self):
		self.host_connect_info = 0
		v.execute("SELECT * FROM host_connect_info")
		self.data = v.fetchall()
		
		if self.data != []:
			self.host_connect_info = [self.data[0][0],self.data[0][1],self.data[0][2]]
		self.root = Tk()
		self.root.title("Database Manager")
		self.root.geometry("500x500+0+0")
		self.power = 0
		#Label title
		self.label=Label(self.root, text="Databse Manager", font=("Arial", 20))
		self.label.place(anchor=CENTER, relx=0.5, rely =0.04)
		#Buttons
		self.admin_access = Button(self.root, text="Admin Access", command= self.host_login, fg=fg)
		self.admin_access.place(anchor=CENTER, relx=0.2, rely=0.1)

		self.login_button = Button(self.root, text="Login", command = self.login, fg=fg)
		self.login_button.place(anchor=CENTER, relx=0.5, rely=0.1)

		self.delete_tempdata_button = Button(self.root, text="Delete tempData", state = DISABLED, command=self.delete_tempdata, fg=fg)
		self.delete_tempdata_button.place(anchor=CENTER, relx=0.8, rely=0.1)

			#Row 2
		self.export_items_button = Button(self.root, text="Export Items", state = DISABLED, command = self.coming_soon)
		self.export_items_button.place(anchor=CENTER, relx=0.2, rely=0.16)

		self.export_user_button = Button(self.root, text="Export User", state = DISABLED, command = self.coming_soon)
		self.export_user_button.place(anchor=CENTER, relx=0.50, rely=0.16)

		self.export_transactions_button = Button(self.root, text="Export Transactions", state = DISABLED, command = self.coming_soon)
		self.export_transactions_button.place(anchor=CENTER, relx=0.8, rely=0.16)

			#Row 3
		self.export_accounts_button = Button(self.root, text="Export Accounts", state = DISABLED, command = self.coming_soon)
		self.export_accounts_button.place(anchor=CENTER, relx=0.2, rely=0.22)

		self.export_rewards_button = Button(self.root, text="Export Rewards", state = DISABLED, command = self.coming_soon)
		self.export_rewards_button.place(anchor=CENTER, relx=0.50, rely=0.22)

		self.export_statistics_button = Button(self.root, text="Export Statistics", state = DISABLED, command = self.coming_soon)
		self.export_statistics_button.place(anchor=CENTER, relx=0.8, rely=0.22)

			#Row 4
		self.create_user_button = Button(self.root, text="Create User", state = DISABLED, command = self.create_user, fg=fg)
		self.create_user_button.place(anchor=CENTER, relx=0.2, rely=0.28)

		self.edit_user_button = Button(self.root, text="Edit User", state = DISABLED, command = self.coming_soon)
		self.edit_user_button.place(anchor=CENTER, relx=0.50, rely=0.28)

		self.delete_user_button = Button(self.root, text="Delete User", state = DISABLED, command = self.coming_soon)
		self.delete_user_button.place(anchor=CENTER, relx=0.8, rely=0.28)

			#Row 5
		self.create_item_button = Button(self.root, text="Create Item", state = DISABLED, command=self.create_items, fg=fg)
		self.create_item_button.place(anchor=CENTER, relx=0.2, rely=0.34)

		self.edit_item_button = Button(self.root, text="Edit Item", state = DISABLED, command = self.edit_items, fg=fg)
		self.edit_item_button.place(anchor=CENTER, relx=0.50, rely=0.34)

		self.delete_item_button = Button(self.root, text="Delete Item", state = DISABLED, command = self.delete_items, fg=fg)
		self.delete_item_button.place(anchor=CENTER, relx=0.8, rely=0.34)

			#Row 6
		self.create_account_button = Button(self.root, text="Create Account", state = DISABLED, command = self.coming_soon)
		self.create_account_button.place(anchor=CENTER, relx=0.2, rely=0.4)

		self.edit_account_button = Button(self.root, text="Edit Account", state = DISABLED, command = self.coming_soon)
		self.edit_account_button.place(anchor=CENTER, relx=0.50, rely=0.4)

		self.delete_account_button = Button(self.root, text="Delete Account", state = DISABLED, command = self.coming_soon)
		self.delete_account_button.place(anchor=CENTER, relx=0.8, rely=0.4)

		#Row 7
		self.create_rewards_button = Button(self.root, text="Create Rewards", state = DISABLED, command = self.coming_soon)
		self.create_rewards_button.place(anchor=CENTER, relx=0.2, rely=0.46)

		self.edit_rewards_button = Button(self.root, text="Edit Rewards", state = DISABLED, command = self.coming_soon)
		self.edit_rewards_button.place(anchor=CENTER, relx=0.50, rely=0.46)

		self.delete_rewards_button = Button(self.root, text="Delete Rewards", state = DISABLED, command = self.coming_soon)
		self.delete_rewards_button.place(anchor=CENTER, relx=0.8, rely=0.46)

		#Row 8
		self.view_transactions_button = Button(self.root, text="View Transactions", state = DISABLED, command = self.coming_soon)
		self.view_transactions_button.place(anchor=CENTER, relx=0.2, rely=0.52)

		self.view_rewards_button = Button(self.root, text ="View Rewards", state = DISABLED, command = self.coming_soon)
		self.view_rewards_button.place(anchor=CENTER, relx=0.50, rely=0.52)

		self.view_stats_button = Button(self.root, text="View Statistics", state = DISABLED, command = self.coming_soon)
		self.view_stats_button.place(anchor=CENTER, relx=0.8, rely=0.52)

		#Row 9
		self.edit_settings_button = Button(self.root, text="Edit Settings", state = DISABLED, command = self.coming_soon)
		self.edit_settings_button.place(anchor=CENTER, relx=0.2, rely=0.58)

		self.clear_transactions_button = Button(self.root, text ="Clear Transactions", state = DISABLED, command = self.coming_soon)
		self.clear_transactions_button.place(anchor=CENTER, relx=0.50, rely=0.58)

		self.contact_developer_button = Button(self.root, text="Contact Developer", command = self.contact_developer, fg=fg)
		self.contact_developer_button.place(anchor=CENTER, relx=0.8, rely=0.58)


		Label(self.root, text="Logged In As:", font=("Arial", 20)).place(anchor=CENTER, relx=0.2, rely =0.9)
		self.userEntry = Entry(self.root)
		self.userEntry.place(anchor=CENTER, relx = 0.6, rely=0.9)
		self.userEntry.config(state = DISABLED)

		self.root.mainloop()

		
	def coming_soon(self):
		messagebox.showinfo(message="Comming Soon!")
	def export_items(self):
		return True

	def export_user(self):
		return True

	def export_transactions(self):
		return True
	
	def export_accounts(self):
		return True

	def export_rewards(self):
		return True

	def export_statistics(self):
		return True
	
	def create_items(self):
		database_editor.create_item(self.host_connect_info)
		return True

	def edit_items(self):
		database_editor.edit_item(self.host_connect_info)
		return True

	def delete_items(self):
		database_editor.delete_item(self.host_connect_info)
		return True
	
	def create_user(self):
		database_editor.create_user(self.host_connect_info)
		return True

	def edit_user(self):
		return True

	def delete_user(self):
		return True
	
	def create_account(self):
		return True

	def edit_account(self):
		return True

	def delete_account(self):
		return True
	
	def create_rewards(self):
		return True

	def edit_rewards(self):
		return True

	def delete_rewards(self):
		return True
	
	def view_transactions(self):
		return True

	def view_rewards(self):
		return True

	def view_stats(self):
		return True
	
	def edit_settings(self):
		return True

	def clear_transactions(self):
		return True

	def export_items(self):
		return True

	def contact_developer(self):
		messagebox.showerror(message="Contact Developer:\nEmail: nicholasjbond2020@gmail.com")




	def delete_tempdata(self):
		v.execute("DROP table host_connect_info")
		self.power = "000000000000000000000000000000"
		self.update_buttons()


	def login(self):
		self.a = 1
		
		try:
			v.execute("SELECT * FROM host_connect_info")
			self.a = 0
			
		except:
			
			messagebox.showerror(message="Error:\nNo Database Selected\nSelect Database through 'Admin Access'")
		if self.a == 0:
			
			if self.host_connect_info == 0:
				
				messagebox.showerror(message="Error:\nPlease connect to database via\nAdmin Access")

			else:
				
				try:
					self.conn = mysql.connector.connect(
						host=self.host_connect_info[0],
						user=self.host_connect_info[1],
						passwd=self.host_connect_info[2],
						database=basic_operations.table_name
						
					)
					self.c = self.conn.cursor()
				except mysql.connector.errors.InterfaceError:
					messagebox.showerror(message = "Please Connect to a server")
					return None

				except mysql.connector.errors.ProgrammingError:
					messagebox.showerror(message = "Please Connect Via Admin Access")
					return None


				

				self.power = login_window.login(self.host_connect_info[0],self.host_connect_info[1],self.host_connect_info[2])
				self.npower = self.power
				if self.npower == "-1":
					
					messagebox.showerror(message="Error:\nPlease create a database via\nAdmin Access")
					self.power = "000000000000000000000000000000"
				else:
					

					
					self.userEntry.config(state = NORMAL)
					self.userEntry.delete(0, END)
					self.userEntry.insert(0, self.power[1])
					self.userEntry.config(state = DISABLED)
					
					self.power = str(self.power[0])
					self.update_buttons()
					

	def update_buttons(self):
		print(F"Power: {self.power}")
		self.button_active(self.delete_tempdata_button, 0)
		self.button_active(self.export_items_button, 1)
		self.button_active(self.export_user_button, 2)
		self.button_active(self.export_transactions_button, 3)
		self.button_active(self.export_accounts_button, 4)
		self.button_active(self.export_rewards_button, 5)
		self.button_active(self.export_statistics_button, 6)
		self.button_active(self.create_user_button, 7)
		self.button_active(self.edit_user_button, 8)
		self.button_active(self.delete_user_button, 9)
		self.button_active(self.create_item_button, 10)
		self.button_active(self.edit_item_button, 11)
		self.button_active(self.delete_item_button, 12)
		self.button_active(self.create_account_button, 13)
		self.button_active(self.edit_account_button, 14)
		self.button_active(self.delete_account_button, 15)
		self.button_active(self.create_rewards_button, 16)
		self.button_active(self.edit_rewards_button, 17)
		self.button_active(self.delete_rewards_button, 18)
		self.button_active(self.view_transactions_button, 19)
		self.button_active(self.view_rewards_button, 20)
		self.button_active(self.view_stats_button, 21)
		self.button_active(self.edit_settings_button, 22)
		self.button_active(self.clear_transactions_button, 23)
		#other power goes up to 29 starting at 0,  (30 total)


		

	def button_active(self, button, power):
		
		if self.power[power] == "1":

			button.config(state=ACTIVE)
			button.focus()
		else:
			button.config(state=DISABLED)
	def host_login(self):
		v.execute("CREATE TABLE IF NOT EXISTS host_connect_info(host TEXT, usr TEXT, pas TEXT)")
		self.host_connect_info = database_setup.connect()
		v.execute("INSERT INTO host_connect_info(host, usr, pas) VALUES(?, ?, ?)", [self.host_connect_info[0],self.host_connect_info[1],self.host_connect_info[2]])
		conn.commit()
		database_setup.create(self.host_connect_info[0],self.host_connect_info[1],self.host_connect_info[2])
		













