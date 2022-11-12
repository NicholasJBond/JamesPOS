from tkinter import *
import mysql.connector
import basic_operations
from tkinter import messagebox
class login_view():
	def __init__(self,host, usr, pas):
		self.power = 0 
		self.host = host
		self.usr = usr
		self.pas = pas
		try:
			self.conn = mysql.connector.connect(
				host=self.host,
				user=self.usr,
				passwd=self.pas,
				database=basic_operations.get_name()
				
			)
			self.c = self.conn.cursor()
		except mysql.connector.errors.InterfaceError:
			messagebox.showerror(message = "Please Connect to a server")
			return None
	
	
		
		
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
		if self.username_box.get() != "":
			if self.password_box.get() != "":
				self.login()
			else:
				self.password_box.focus()
		else:
			self.username_box.focus()

	def login(self):
		self.id = self.username_box.get()
		self.c.execute("SELECT * FROM user WHERE id = %s", [self.id])
		self.data = self.c.fetchall()
		if self.data == []:
			messagebox.showerror(message="Error:\nInvalid ID")
			self.username_box.delete(0, END)
			self.username_box.focus()
		else:
			if len(self.data) > 1:
				messagebox.showerror(message = "Urgent Error:\nMore than one user with the same id exists.\n!!!Fix Immediately!!!")
			else:
				self.username = self.data[0][1]
				
				
				if self.data[0][2] == self.password_box.get():
					if basic_operations.is_int(self.data[0][3]) == True:
						self.power = self.data[0][3]
					else:
						self.power = 0
						
					self.root.destroy()
					self.root.quit()
				else:
					messagebox.showerror(message = "Error:\nInvalid Password")
					self.password_box.delete(0, END)
					self.password_box.focus()
				

		

def login(host, usr, pas):
	try:
		window = login_view(host, usr, pas)
		var = window.power, window.username

	except mysql.connector.errors.ProgrammingError:
		var = -1
	except AttributeError:
		var = 0
		pass 
	return var

