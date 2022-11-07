import mysql.connector
from tkinter import *
from tkinter import messagebox
import basic_operations



class create_item():
	def __init__(self, host):
		self.host = host
		self.root = Tk()
		self.root.title("Create Item")
		self.root.geometry("500x400+0+0")
	
		self.title_label = Label(self.root, text = "Create Item", font = ("Arial", 35))
		self.title_label.place(anchor=CENTER, relx=0.5, rely=0.15)

		self.plu_label = Label(self.root, text = "PLU*:")
		self.plu_label.place(anchor=E, relx=0.38, rely = 0.3)

		self.description_label = Label(self.root, text = "Description*:")
		self.description_label.place(anchor=E, relx=0.38, rely = 0.37)

		self.price_label = Label(self.root, text = "Price: $")
		self.price_label.place(anchor=E, relx=0.38, rely = 0.44)

		self.type_label = Label(self.root, text = "Type:")
		self.type_label.place(anchor=E, relx=0.38, rely = 0.51)

		self.category_label = Label(self.root, text = "Category:") 
		self.category_label.place(anchor=E, relx=0.38, rely = 0.58)

		self.points_label = Label(self.root, text = "Bonus Points:")
		self.points_label.place(anchor=E, relx=0.38, rely = 0.65)


		#entrys

		self.plu_entry = Entry(self.root)
		self.plu_entry.place(anchor=W, relx=0.4, rely = 0.3)
		self.plu_entry.focus()

		self.description_entry = Entry(self.root)
		self.description_entry.place(anchor=W, relx=0.4, rely = 0.37)

		self.price_entry = Entry(self.root)
		self.price_entry.place(anchor=W, relx=0.4, rely = 0.44)

		self.typea = IntVar()
		self.typea.set(0)
		
		Radiobutton(self.root, text = "$ per item",indicatoron = 0, variable = self.typea, value = 0).place(anchor=W, relx = 0.4, rely=0.51)
		Radiobutton(self.root, text = "$ per weight", indicatoron = 0, variable = self.typea, value = 1).place(anchor=W, relx = 0.575, rely=0.51)
		
		

		
		self.category_entry = Entry(self.root)
		self.category_entry.place(anchor=W, relx=0.4, rely = 0.58)

		self.points_entry = Entry(self.root)
		self.points_entry.place(anchor=W, relx=0.4, rely = 0.65)

		self.submit_button = Button(self.root, text="Create", command=self.create)
		self.submit_button.place(anchor=CENTER, relx=0.5, rely=0.8)

		self.close_button = Button(self.root, text="❌", command=self.close)
		self.close_button.place(anchor=CENTER, relx=0.5, rely=0.9)

		self.root.bind("<Return>", lambda a:self.create())
		self.root.mainloop()
		return None

	def close(self):
		self.root.destroy()
		self.root.quit()

	def create(self):
		if self.plu_entry.get() == "":
			self.plu_entry.focus()
		else:
			if self.description_entry.get() == "":
				self.description_entry.focus()
			else:
				if self.price_entry.get() == "":
					self.price_entry.focus()
				else:
					if self.category_entry.get() == "":
						self.category_entry.focus()
					else:
						if self.points_entry.get() == "":
							self.points_entry.focus()
						else:
							self.plu = self.plu_entry.get()
							self.description = self.description_entry.get()
							self.price = self.price_entry.get()
							self.category = self.category_entry.get()
							self.points = self.points_entry.get()
							if basic_operations.is_float(self.price) == True and basic_operations.is_int(self.points) == True:

								
								self.conn = mysql.connector.connect(
									host=self.host[0],
									user=self.host[1],
									passwd=self.host[2],
									database=basic_operations.table_name
									
								)
								self.c = self.conn.cursor()
								self.c.execute("INSERT INTO items(plu, description, price, type, category, points, quantity) VALUES(%s,%s,%s,%s,%s,%s, 0)", [self.plu, self.description, self.price, self.typea.get(), self.category, self.points])
								self.conn.commit()
								self.root.destroy()
								self.root.quit()
							elif basic_operations.is_float(self.price) == True:
								self.points_entry.focus()
							else:
								self.price_entry.focus()

		return True
class edit_item():
	def __init__(self,host):
		self.host = host
		self.conn = mysql.connector.connect(
									host=self.host[0],
									user=self.host[1],
									passwd=self.host[2],
									database=basic_operations.table_name
									
								)
		self.c = self.conn.cursor()
		self.root = Tk()
		self.root.title("Edit Item")
		self.root.geometry("500x400+0+0")
	
		self.title_label = Label(self.root, text = "Edit Item", font = ("Arial", 35))
		self.title_label.place(anchor=CENTER, relx=0.5, rely=0.15)

		self.plu_label = Label(self.root, text = "PLU*:")
		self.plu_label.place(anchor=E, relx=0.38, rely = 0.3)

		self.description_label = Label(self.root, text = "Description*:")
		self.description_label.place(anchor=E, relx=0.38, rely = 0.37)

		self.price_label = Label(self.root, text = "Price: $")
		self.price_label.place(anchor=E, relx=0.38, rely = 0.44)

		self.type_label = Label(self.root, text = "Type:")
		self.type_label.place(anchor=E, relx=0.38, rely = 0.51)

		self.category_label = Label(self.root, text = "Category:") 
		self.category_label.place(anchor=E, relx=0.38, rely = 0.58)

		self.points_label = Label(self.root, text = "Bonus Points:")
		self.points_label.place(anchor=E, relx=0.38, rely = 0.65)

		self.quantity_label = Label(self.root, text = "Quantity In Stock:")
		self.quantity_label.place(anchor=E, relx=0.38, rely = 0.72)


		#entrys
		#
		self.search_button = Button(self.root, text = "🔍")
		self.search_button.place(anchor=CENTER, relx=0.85, rely = 0.293)

		self.plu_entry = Entry(self.root)
		self.plu_entry.place(anchor=W, relx=0.4, rely = 0.3)
		self.plu_entry.focus()

		self.description_entry = Entry(self.root)
		self.description_entry.place(anchor=W, relx=0.4, rely = 0.37)

		self.price_entry = Entry(self.root)
		self.price_entry.place(anchor=W, relx=0.4, rely = 0.44)



		self.typea = IntVar()
		self.typea.set(0)
		
		Radiobutton(self.root, text = "$ per item",indicatoron = 0, variable = self.typea, value = 0).place(anchor=W, relx = 0.4, rely=0.51)
		Radiobutton(self.root, text = "$ per weight", indicatoron = 0, variable = self.typea, value = 1).place(anchor=W, relx = 0.575, rely=0.51)
		

		
		self.category_entry = Entry(self.root)
		self.category_entry.place(anchor=W, relx=0.4, rely = 0.58)

		self.points_entry = Entry(self.root)
		self.points_entry.place(anchor=W, relx=0.4, rely = 0.65)

		self.quantity_entry = Entry(self.root)
		self.quantity_entry.place(anchor=W, relx=0.4, rely = 0.72)

		self.save_button = Button(self.root, text="Save", command=self.save)
		self.save_button.place(anchor=CENTER, relx=0.5, rely=0.8)

		self.close_button = Button(self.root, text="❌", command=self.close)
		self.close_button.place(anchor=CENTER, relx=0.5, rely=0.9)

		self.root.bind("<Return>", lambda a:self.enter())
		self.root.mainloop()
		return None
	def close(self):
		self.root.destroy()
		self.root.quit()

	def enter(self):
		if self.plu_entry.get() != "" and self.description_entry.get() == "":
			self.search()
		else:
			if self.plu_entry.get() == "":
				self.plu_entry.focus()
			else:
				if self.description_entry.get() == "":
					self.description_entry.focus()
				else:
					if self.price_entry.get() == "":
						self.price_entry.focus()
					else:
						if self.category_entry.get() == "":
							self.category_entry.focus()
						else:
							if self.points_entry.get() == "":
								self.points_entry.focus()
							else:
								self.save()

	def search(self):
		self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_entry.get()])
		self.data = self.c.fetchall()
		if self.data == []:
			self.plu_entry.delete(0, END)
			
		else:
			print(self.data)
			self.plu = self.plu_entry.get()
			self.refil_entry(self.description_entry, self.data[0][1])
			self.refil_entry(self.price_entry, self.data[0][5])
			self.refil_entry(self.category_entry, self.data[0][3])
			self.refil_entry(self.points_entry, self.data[0][4])
			self.typea.set(self.data[0][2])
			self.refil_entry(self.quantity_entry, self.data[0][6])
		return True
	def save(self):
		if self.plu_entry.get() != "":
			self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_entry.get()])
			self.data = self.c.fetchall()
			
				
			if basic_operations.is_int(self.points_entry.get()) == True:
				if basic_operations.is_float(self.price_entry.get()) == True:
					if basic_operations.is_float(self.quantity_entry.get())==True:

						self.c.execute("UPDATE items SET plu = %s, description = %s, price = %s, type = %s, category = %s, points = %s, quantity = %s WHERE plu = %s",
								[
								self.plu_entry.get(),
								self.description_entry.get(), 
								self.price_entry.get(), 
								self.typea.get(), 
								self.category_entry.get(), 
								self.points_entry.get(), 
								self.quantity_entry.get(), 
								self.plu
								]
								)
						self.conn.commit()
						self.root.destroy()
						self.root.quit()
					else:
						self.quantity_entry.delete(0, END)
						self.quantity_entry.focus()
				else:
					self.price_entry.delete(0, END)
					self.price_entry.focus()
			else:
				self.points_entry.delete(0, END)
				self.points_entry.focus()
		return True
	def refil_entry(self, entry, inputa):
		entry.delete(0, END)
		entry.insert(0, inputa)
class delete_item():
	def __init__(self,host):
		self.host = host
		self.conn = mysql.connector.connect(
									host=self.host[0],
									user=self.host[1],
									passwd=self.host[2],
									database=basic_operations.table_name
									
								)
		self.c = self.conn.cursor()
		self.root = Tk()
		self.root.title("Delete Item")
		self.root.geometry("500x400+0+0")
	
		self.title_label = Label(self.root, text = "Delete Item", font = ("Arial", 35))
		self.title_label.place(anchor=CENTER, relx=0.5, rely=0.15)

		self.plu_label = Label(self.root, text = "Search PLU", font = ("Arial", 15))
		self.plu_label.place(anchor=CENTER, relx=0.5, rely=0.3)

		self.search_button = Button(self.root, text = "🔍", command = self.search)
		self.search_button.place(anchor=CENTER, relx=0.75, rely = 0.1+0.293)
		self.delete_button = Button(self.root, text = "🗑️", command = self.delete)
		self.delete_button.place(anchor=CENTER, relx=0.5, rely = 0.8)

		self.info_label = Label(self.root, text= "PLU: \nDescription: \nPrice: \nCategory: \nQuantity: \nBonus Points: ", justify=RIGHT)
		self.info_label.place(anchor = E, relx=0.5, rely=0.6)

		self.result_label = Label(self.root, text= "", justify=LEFT)
		self.result_label.place(anchor = W, relx=0.5, rely=0.6)

		self.close_button = Button(self.root, text="❌", command=self.close)
		self.close_button.place(anchor=CENTER, relx=0.5, rely=0.9)

		self.plu_entry = Entry(self.root)
		self.plu_entry.place(anchor=CENTER, relx=0.5, rely = 0.4)
		self.plu_entry.focus()

		self.root.bind("<Return>", lambda a: self.search())
		self.root.mainloop()

	def close(self):
		self.root.destroy()
		self.root.quit()

	def search(self):
		self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_entry.get()])
		self.data = self.c.fetchall()
		if self.data == []:
			self.plu_entry.delete(0, END)
			self.result_label.configure(text="")
			return False

		else:
			self.result_label.configure(text = f"{self.data[0][0]}\n{self.data[0][1]}\n{self.data[0][5]}\n{self.data[0][3]}\n{self.data[0][6]}\n{self.data[0][4]}")
			return True
	def delete(self):
		if self.search() == True:
			if messagebox.askquestion ("Delete Item", "Are you sure you want to delete this item?", icon = 'warning') == "yes":
				self.c.execute("DELETE FROM items WHERE plu = %s", [self.plu_entry.get()])
				self.conn.commit()
				self.close()
			else:
				self.plu_entry.delete(0, END)
				self.result_label.configure(text="")
		return True

class create_user():
	def __init__(self, host):
		self.database = basic_operations.table_name
		self.host = host
		self.root = Tk()
		self.root.title("Create Item")
		self.root.geometry("500x400+0+0")
	
		self.title_label = Label(self.root, text = "Create User", font = ("Arial", 35))
		self.title_label.place(anchor=CENTER, relx=0.5, rely=0.15)

		Label(self.root, text = "ID:").place(anchor=E, relx=0.38, rely = 0.3)

		Label(self.root, text = "Password:").place(anchor=E, relx=0.38, rely = 0.37)

		Label(self.root, text = "Name:").place(anchor=E, relx=0.38, rely = 0.44)

		Label(self.root, text = "Permissions:").place(anchor=E, relx=0.38, rely = 0.51)

		Label(self.root, text = "Presets:").place(anchor=E, relx=0.38, rely = 0.65)




		#entrys

		self.id_entry = Entry(self.root)
		self.id_entry.place(anchor=W, relx=0.4, rely = 0.3)
		self.id_entry.focus()

		self.password_entry = Entry(self.root)
		self.password_entry.place(anchor=W, relx=0.4, rely = 0.37)

		self.name_entry = Entry(self.root)
		self.name_entry.place(anchor=W, relx=0.4, rely = 0.44)
		self.perms = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.perm = StringVar()
		self.perm.set("Select Permissions to edit")

		self.options = [
		    "Delete Temporary Data",
		    "Export list of Items",
		    "Export list of Users",
		    "Export list of Transactions",
		    "Export list of Accounts",
		    "Export list of Customer Rewards",
		    "Export statistics",
		    "Create User",
		    "Edit Users",
		    "Delete Users",
		    "Create Item",
		    "Edit Items",
		    "Delete Items",
		    "Create Account",
		    "Edit Account",
		    "Delete Account",
		    "Create Rewards",
		    "Edit Rewards",
		    "Delete Rewards",
		    "View Transactions",
		    "View Rewards",
		    "View Statistics",
		    "Edit Settings",
		    "Clear Transactions"
		]		
		self.permission_menu = OptionMenu( self.root , self.perm , *self.options, command = self.permission_select)
		self.permission_menu.place(anchor=W, relx = 0.4, rely = 0.51)

		self.status_value = IntVar()
		self.status = Checkbutton(self.root, text = "Select Permission", variable = self.status_value, onvalue = 1, offvalue = 0, command = self.adjustperms, state=DISABLED)
		self.status.place(anchor = W, relx = 0.4, rely = 0.58)

		self.preset_admin_button = Button(self.root, text = "Admin", command = self.presetadmin)
		self.preset_admin_button.place(anchor =W, relx = 0.4, rely = 0.65)

		self.preset_manager_button = Button(self.root, text = "Manager", command = self.presetmanager)
		self.preset_manager_button.place(anchor =W, relx = 0.55, rely = 0.65)

		self.preset_manager_button = Button(self.root, text = "Operator", command = self.presetoperator)
		self.preset_manager_button.place(anchor =W, relx = 0.725, rely = 0.65)

		self.submit_button = Button(self.root, text="Create", command=self.create)
		self.submit_button.place(anchor=CENTER, relx=0.5, rely=0.8)

		self.close_button = Button(self.root, text="❌", command=self.close)
		self.close_button.place(anchor=CENTER, relx=0.5, rely=0.9)

		self.root.bind("<Return>", lambda a:self.create())
		self.root.mainloop()
		return None
	def presetadmin(self):
		self.perms = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
		self.perm.set(self.options[0])
		self.permission_select(1)

	def presetmanager(self):
		self.perms = [0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1]
		self.perm.set(self.options[0])
		self.permission_select(1)

	def presetoperator(self):
		self.perms = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1]
		self.perm.set(self.options[0])
		self.permission_select(1)

	def adjustperms(self):
		for i in range(len(self.options)):
			
			if self.perm.get() == self.options[i]:
				self.num = i
				break

			else:
				i += 1

		self.perms[self.num] = self.status_value.get() 
		if self.status_value.get() == 0:
			self.status.config(text="Permission Denied")
		else:
			
			self.status.config(text="Permission Granted")			


	def permission_select(self, a):
		self.permission_menu.config(state = ACTIVE)
		self.status.config(state = ACTIVE)


		for i in range(len(self.options)):
			
			if self.perm.get() == self.options[i]:
				self.num = i
				break
			else:
				pass
			
		self.status_value.set(self.perms[self.num])
		print(self.status_value.get())

		if self.status_value.get() == 0:
			self.status.config(text="Permission Denied")
		else:
			
			self.status.config(text="Permission Granted")
		

	def close(self):
		self.root.destroy()
		self.root.quit()

	def create(self):
		if self.id_entry.get() == "":
			self.id_entry.focus()
		elif self.password_entry.get() == "":
			self.password_entry.focus()
		elif self.name_entry.get() == "":
			self.name_entry.focus()
		else:
			self.newperms = ""
			for i in range(len(self.perms)):
				self.newperms = self.newperms + str(self.perms[i])
			
								
			self.conn = mysql.connector.connect(
				host=self.host[0],
				user=self.host[1],
				passwd=self.host[2],
				database=self.database
				
			)
			self.c = self.conn.cursor()


			
			self.c.execute("SELECT * FROM user WHERE id = %s", [self.id_entry.get()])
			if len(self.c.fetchall()) > 1:
				self.id_entry.delete(0, END)
				self.id_entry.focus()
				Label(self.root, text = "User with ID already exists.", font = ("Arial", 20), fg = "Red").place(anchor= CENTER, relx =0.5, rely = 0.7)
			else:
				self.c.execute("INSERT INTO user(id, name, password, permissions) VALUES(%s, %s, %s, %s)", [self.id_entry.get(), self.name_entry.get(), self.password_entry.get(), self.newperms])
				self.conn.commit()
				self.close()
							
		return True
		


		
