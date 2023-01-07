from tkinter import *
import mysql.connector
import sqlite3
from tkinter import messagebox
import basic_operations
import datetime
import application



class window():
	def __init__(self):

		self.vonn = sqlite3.connect("LocalData")
		self.v = self.vonn.cursor()
		
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

		self.loyaltynum = None

		
		self.fullscreen = True
		self.root = Tk()
		self.root.geometry("800x480")
		self.root.title("POS")
		self.root.attributes("-fullscreen", self.fullscreen)

		self.background_colour = "light blue"
		
		self.forground_colour = "white"

		self.invoice_frame = Frame(self.root, bg=self.background_colour, height = 480, width=800)
		self.invoice_frame.pack()
		self.create_widgets()
		self.state = "Login"
		self.root.bind("<KP_Subtract>",  lambda a: self.subtract())
		self.root.bind("<KP_Add>",  lambda a: self.add())
		self.root.bind("<KP_Divide>",  lambda a: self.divide())
		self.root.bind("<KP_Multiply>",  lambda a: self.multiply())
		self.root.bind("<minus>",  lambda a: self.subtract())
		self.root.bind("<+>",  lambda a: self.add())
		self.root.bind("</>",  lambda a: self.divide())
		self.root.bind("<*>",  lambda a: self.multiply())
		self.root.bind("<KP_Enter>",  lambda a: self.returnkey())
		self.root.bind("<Return>",  lambda a: self.returnkey())

		


		self.root.mainloop()

	def create_widgets(self):
		self.invoice_frame.pack()
		self.line1_text = ""
		self.line1 = Label(self.invoice_frame, text=self.line1_text, font = ("Arial", 30), fg=self.forground_colour, bg = self.background_colour)
		self.line1.place(anchor=CENTER, relx=0.5, rely=0.1)

		self.line2_text = ""
		self.line2 = Label(self.invoice_frame, text=self.line2_text, font = ("Arial", 28), fg=self.forground_colour, bg = self.background_colour)
		self.line2.place(anchor=CENTER, relx=0.5, rely=0.2)

		self.line3_text = ""
		self.line3 = Label(self.invoice_frame, text=self.line3_text, font = ("Arial", 26), fg=self.forground_colour, bg = self.background_colour)
		self.line3.place(anchor=CENTER, relx=0.5, rely=0.3)

		self.line4_text = ""
		self.line4 = Label(self.invoice_frame, text=self.line4_text, font = ("Arial", 24), fg=self.forground_colour, bg = self.background_colour)
		self.line4.place(anchor=CENTER, relx=0.5, rely=0.4)

		self.line5_text = ""
		self.line5 = Label(self.invoice_frame, text=self.line5_text, font = ("Arial", 22), fg=self.forground_colour, bg = self.background_colour)
		self.line5.place(anchor=CENTER, relx=0.5, rely=0.5)

		self.line6_text = ""
		self.line6 = Label(self.invoice_frame, text=self.line6_text, font = ("Arial", 20), fg=self.forground_colour, bg = self.background_colour)
		self.line6.place(anchor=CENTER, relx=0.5, rely=0.6)

		
		self.tranid = Button(self.invoice_frame, text = "A000000001",font=("Arial", 25))
		self.tranid.place(anchor=W, relx=0.745, rely = 0.68)
		Button(self.invoice_frame, text = "Cash on hand", font=("Arial", 25)).place(anchor=W,relx =0.03, rely=0.68)
		self.cid = Button(self.invoice_frame, text="$   0.00", font=("Arial", 25))
		self.cid.place(anchor=W, relx=0.268, rely=0.68)

		Button(self.invoice_frame, text = "Total", font=("Arial", 25)).place(anchor=W,relx =0.45, rely=0.68)
		self.total = Button(self.invoice_frame, text="$   0.00", font=("Arial", 25))
		self.total.place(anchor=W, relx=0.563, rely=0.68)

		self.helptext = "/ markdown 	* change qty 	+ pay"
		self.help = Label(self.invoice_frame, text=self.helptext, font =("Arial", 30), fg=self.background_colour, bg="white")
		self.help.place(anchor=CENTER, relx=0.5, rely = 0.775)

		self.entry = Entry(self.invoice_frame, width =37, font = ("Arial",35), fg=self.background_colour)
		self.entry.place(anchor=CENTER, relx = 0.5, rely=0.9)
		self.entry.focus()
		
		self.reset_invoice()
		
		return None
	def reset_invoice(self):
		self.entry.delete(0,END)
		self.entry.focus()
		self.invoice_frame.pack()
		self.update_stats()
		self.line1.config(text="")
		self.line2.config(text="")
		self.line3.config(text="")
		self.line4.config(text="")
		self.line5.config(text="")
		self.line6.config(text="")
		self.state = "Invoice"
		self.update_helptext("/ markdown 	* change qty 	+ pay")
		self.plu_list = []
		self.quantity_list = []
		self.price_list = []
		self.points_list = []
		self.top = None
		self.total.config(text="$   0.00")

	def login(self):
		# self.invoice_frame.pack_forget()
		# application.window()
		# print(self.root.winfo_manager())
		
		
		self.root.withdraw()
		application.window()
		self.root.deiconify()
		self.reset_invoice()
		

	def subtract(self):
		if self.state == "Eftpos":
			self.state = "Pay"
			self.update_helptext("/ markdown 	* change qty 	+ pay")
		return True

	def divide(self):
		if self.state == "Invoice":
			self.markdown()
		elif self.state == "Pay":
			self.cash()
	def add(self):
		if self.state == "Invoice":
			self.pay()
		elif self.state == "Pay":
			self.account()
		
	def multiply(self):
		if self.state == "Invoice":
			self.change_qty()
		elif self.state == "Pay":
			self.update_helptext("Enter to process sale 	- To go back")
			self.state = "Eftpos"
			self.entry.delete(0,END)

		return True
		
	def returnkey(self):
		print(f"State: {self.state}")
		if self.state == "Login":
			self.login()
		elif self.state == "Invoice":
			self.invoice_search()
		elif self.state == "Pay":
			self.state = "Invoice"
			self.update_helptext("/ markdown 	* change qty 	+ pay")
		elif self.state == "Eftpos":
			if self.entry.get() == "":
				self.process_sale("Eftpos", self.calctotal())
				self.reset_invoice()
				
			elif basic_operations.is_float(self.entry.get()):
				self.process_sale("Eftpos", self.entry.get())
					
			else:
				print("Error: Amount entered is not a number")
	

	def itemtype(self, typee):
		if typee == 0:
			return "each"
		else:
			return "per kg"
	def update_helptext(self, text):
		self.help.config(text = text)
	def invoice_search(self):
		if self.entry.get() == "0001":
			self.reset_invoice()
			self.help.config(text="")
			self.login()
			
			

			return None
		elif self.entry.get() == "0002":
			self.reset_invoice()
			return None

		self.c.execute("SELECT * FROM items WHERE plu = %s", [self.entry.get()])
		
		self.data = self.c.fetchall()
		if len(self.data) == 1:
			self.multiple = False
			for i in range(len(self.plu_list)):

				if self.data[0][0] == self.plu_list[i]:
					self.multiple = True
					break
			

			if self.multiple:
				self.i = i
				self.remove_line(self.i)
				self.quantity_list[self.i] += 1
				
			else:
				self.i = len(self.plu_list)
				self.plu_list.append(self.data[0][0])
				self.quantity_list.append(1)
				self.price_list.append(self.data[0][5])
				self.points_list.append(self.data[0][4])
			self.calctotal()
			self.display_line(f"{self.quantity_list[self.i]} x {self.data[0][1]} @ ${self.price_list[self.i]:.2f} {self.itemtype(self.data[0][2])}", float(self.price_list[self.i])*self.quantity_list[self.i], self.plu_list[self.i])
		else:
			self.c.execute("SELECT * FROM accounts WHERE id = %s", [self.entry.get()])
			self.data = self.c.fetchall()
			if len(self.data) == 1:
				self.loyaltynum = self.entry.get()

		self.entry.delete(0, END)

	def process_sale(self, paymentmethod, amount):

		#Updating Ledger
		if paymentmethod == "Eftpos":
			if amount == self.calctotal():
				self.c.execute("SELECT * FROM general_ledger_place WHERE place_name = 'Eftpos Bank'")
				self.data = self.c.fetchall()
				if self.data == []:
					self.c.execute("SELECT * FROM general_ledger_place ORDER BY place_id DESC LIMIT 1")
					self.data=self.c.fetchall()
					if len(self.data) == 1:
						self.id = int(self.data[0][0])+1
					else:
						self.id = 0
					self.c.execute("INSERT INTO general_ledger_place(place_id, place_name, value, location) VALUES(%s, %s, %s, 'Bank')", [self.id, 'Eftpos Bank', 0])
					self.conn.commit()
					self.c.execute("SELECT * FROM general_ledger_place WHERE place_name = 'Eftpos Bank'")
					self.data = self.c.fetchall()

				self.c.execute("SELECT * FROM general_ledger ORDER BY id DESC LIMIT 1")
				self.data=self.c.fetchall()
				if len(self.data) == 1:
					self.id = int(self.data[0][0])+1
				else:
					self.id = 0

				self.v.execute("SELECT * FROM login_info")
				self.user= self.v.fetchall()[0][0]
				self.datetime = datetime.datetime.now()

				self.c.execute("INSERT INTO general_ledger(id, amount, from_id, to_id, time_s, date_s, user_id) VALUES(%s, %s, %s, %s, %s, %s, %s)", [self.id, round(self.calctotal(),3), "Customer", "Eftpos Bank", self.datetime.strftime("%X"), self.datetime.strftime("%x"), self.user])
				self.conn.commit()

				
				self.c.execute("SELECT * FROM general_ledger_place WHERE place_name = 'Eftpos Bank'")
				self.data = self.c.fetchall()[0][2] + self.calctotal()
				self.c.execute("UPDATE general_ledger_place SET value = %s WHERE place_name = 'Eftpos Bank'", [round(self.data,3)])
				self.conn.commit()
				

				#---------------------Transaction updating
				self.c.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 1")
				self.data=self.c.fetchall()
			
				if len(self.data) == 1:
					
					self.id = int(self.data[0][0])+1
				else:
					self.id = 0


				
				self.discounts = 0
				for i in range(len(self.plu_list)):
					self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_list[i]])
					self.data = self.c.fetchall()[0]
					self.c.execute("INSERT INTO transaction_items(id, plu, description, quantity, total, gst, shelf_price, points) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", [self.id, self.plu_list[i],self.data[1], self.quantity_list[i], round(self.price_list[i]*self.quantity_list[i]/1.1,3),round(self.price_list[i]*self.quantity_list[i]/1.1*0.1,3), self.data[5], self.points_list[i]])
					self.discounts = self.discounts + ((self.data[5]*self.quantity_list[i])-(self.price_list[i]*self.quantity_list[i]))
				


				self.v.execute("SELECT * FROM settings WHERE name = 'registerid'")
				self.data = self.v.fetchall()
				self.c.execute("INSERT INTO transactions(id, date_s, time_s, total, gst, payment_method, loyalty_id, discounts, amount_recieved, location, user_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[self.id, self.datetime.strftime("%x"), self.datetime.strftime("%X"), round(self.calctotal()/1.1,3), round(self.calctotal()/1.1*0.1,3), "Eftpos", self.loyaltynum, round(self.discounts,2), round(self.calctotal(),3), self.data[0][1],self.user])
				if self.loyaltynum != None:
					self.c.execute("SELECT * FROM accounts WHERE id = %s", [self.loyaltynum])
					self.points = self.c.fetchall()[0][4]
					for i in range(len(self.points_list)):
						self.points = self.points + self.points_list[i]
					
					self.c.execute("UPDATE accounts SET points = %s WHERE id = %s", [self.points, self.loyaltynum])

				for i in range(len(self.plu_list)):
					self.c.execute("SELECT quantity FROM items WHERE plu =%s", [self.plu_list[i]])
					self.data = self.c.fetchall()[0][0]
					self.c.execute("UPDATE items SET quantity = %s WHERE PLU = %s", [self.data - self.quantity_list[i], self.plu_list[i]])
					print(i)

		self.conn.commit()
		return True
	def cash(self):
		self.state = "Cash"
		return True
	def account(self):
		self.state="Account"
		return True
	def markdown(self):
		self.entry.delete(len(self.entry.get())-1, END)
		if len(self.plu_list) > 0:
			pass
		else:
			return None
		if basic_operations.is_float(self.entry.get()):
			for i in range(len(self.plu_list)):
			
				if self.plu_list[i] == self.top:
					a = True
					break
				else:
					a = False
			if a:
				
				self.remove_line(i)
				self.price_list[i] = float(self.entry.get())
				self.entry.delete(0, END)
				self.calctotal()
				self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_list[i]])
				self.data = self.c.fetchall()
				self.display_line(f"{self.quantity_list[i]} x {self.data[0][1]} @ ${self.price_list[self.i]:.2f} {self.itemtype(self.data[0][2])}", float(self.price_list[i])*self.quantity_list[i], self.plu_list[i])
				
		else:
			self.entry.delete(0, END)
			self.entry.insert(0, "Enter a number you fool")

	def change_qty(self):
		self.entry.delete(len(self.entry.get())-1, END)
		if len(self.plu_list) <= 0: return None
		if basic_operations.is_float(self.entry.get()):
			for i in range(len(self.plu_list)):
				if self.plu_list[i] == self.top:
					a = True
					break
				else:
					a = False
			if a:
				
				self.remove_line(i)
				self.quantity_list[i] = round(float(self.entry.get()),3)
				self.entry.delete(0, END)
				self.calctotal()
				self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_list[i]])
				self.data = self.c.fetchall()
				self.display_line(f"{self.quantity_list[i]} x {self.data[0][1]} @ ${self.price_list[self.i]:.2f} {self.itemtype(self.data[0][2])}", float(self.price_list[i])*self.quantity_list[i], self.plu_list[i])
				for i in range(len(self.plu_list)):
					if self.plu_list[i] == self.top:
						self.c.execute("SELECT * FROM items WHERE plu = %s",[self.plu_list[i]])
						self.data=self.c.fetchall()[0][4]
						self.points_list[i] = self.data * self.quantity_list[i]
				
		else:
			self.entry.delete(0, END)
			self.entry.insert(0, "Enter a number you fool")
	def pay(self):
		if len(self.plu_list) > 0:
			pass
		else:
			return None
		self.entry.delete(0, END)
		self.state = "Pay"
		self.update_helptext("/ Cash 	* Manual Eftpos 	+ Account")

		return True
	def calctotal(self):
		self.price = 0
		for i in range(len(self.price_list)):
			self.price += self.price_list[i]*self.quantity_list[i]
		self.total.config(text = f'${self.price:.2f}')
		return self.price

	def display_line(self, text, price, plu):
		dashes = ""
		for i in range(45-len(text)):
			dashes = dashes + "-"
		line = text+dashes+f'${price:.2f}'
		
		if line[0] == "-":
			self.line1.config(fg="red")
		else:
			self.line1.config(fg="white")
		
		self.red_line(self.line1, self.line2)
		self.red_line(self.line2, self.line3)
		self.red_line(self.line3, self.line4)
		self.red_line(self.line4, self.line5)
		self.red_line(self.line5, self.line6)

		self.line6.config(text = self.line5.cget("text"))
		self.line5.config(text = self.line4.cget("text"))
		self.line4.config(text = self.line3.cget("text"))
		self.line3.config(text = self.line2.cget("text"))
		self.line2.config(text = self.line1.cget("text"))
		self.line1.config(text = line)
		self.top = plu
		return None

	def red_line(self, var, var2):
		if var.cget("text") != "":
			if var.cget("text")[0] == "-":
				var2.config(fg="red")
			else:
				var2.config(fg="white")

	def remove_line(self, i):
			
		self.c.execute("SELECT * FROM items WHERE plu = %s", [self.plu_list[i]])
		self.data = self.c.fetchall()
		thing =f"{round(self.quantity_list[i],3)} x {self.data[0][1]} @ ${self.price_list[i]:.2f} {self.itemtype(self.data[0][2])}", float(self.price_list[i])*self.quantity_list[i]
		dashes = ""
		for i in range(45-len(thing[0])):
			dashes = dashes + "-"
		line = thing[0]+dashes+f'${thing[1]:.2f}'
		
		
		if self.line1.cget("text")==line:
			self.line1.config(text=self.line2.cget("text"))
			self.line2.config(text=self.line3.cget("text"))
			self.line3.config(text=self.line4.cget("text"))
			self.line4.config(text=self.line5.cget("text"))
			self.line5.config(text=self.line6.cget("text"))
			self.line6.config(text="")

			
		if self.line2.cget("text")==line:
			self.line2.config(text=self.line3.cget("text"))
			self.line3.config(text=self.line4.cget("text"))
			self.line4.config(text=self.line5.cget("text"))
			self.line5.config(text=self.line6.cget("text"))
			self.line6.config(text="")
	
		if self.line3.cget("text")==line:
			
			self.line3.config(text=self.line4.cget("text"))
			self.line4.config(text=self.line5.cget("text"))
			self.line5.config(text=self.line6.cget("text"))
			self.line6.config(text="")
	
		if self.line4.cget("text")==line:
			
			self.line4.config(text=self.line5.cget("text"))
			self.line5.config(text=self.line6.cget("text"))
			self.line6.config(text="")
	
		if self.line5.cget("text")==line:
			
			self.line5.config(text=self.line6.cget("text"))
			self.line6.config(text="")
			
		if self.line6.cget("text")==line:
			self.line6.config(text="")
		
	

		return None

	def update_stats(self):
		self.v.execute("SELECT * FROM settings WHERE name = 'registerid'")
		self.data = self.v.fetchall()
		self.tranid_text = self.data[0][1]
		self.c.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 1")
		self.data = self.c.fetchall()
		if len(self.data) == 1:
			self.id = int(self.data[0][0]) + 1
		else:
			self.id = 1
		self.data = ""
		for i in range(9-len(str(self.id))):
			self.data = self.data + "0"
		self.tranid_text = str(self.tranid_text) + str(self.data)+str(self.id)
		self.tranid.config(text=self.tranid_text)

		self.v.execute("SELECT * FROM settings WHERE name = 'registerid'")
		self.data = self.v.fetchall()
		self.c.execute("SELECT * FROM general_ledger_place WHERE place_name = %s", [self.data[0][1]])
		self.data = self.c.fetchall()
		if self.data[0][2] == 0:
			self.amount = "$  0.00"
		else:
			self.amount = f'${self.data[0][2]:.2f}'
			
		self.cid.config(text=self.amount)
	