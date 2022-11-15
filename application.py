from tkinter import *
import mysql.connector
import database_view
class window():
	def __init__(self):
		self.fullscreen = False
		self.root = Tk()
		self.root.geometry("800x480")
		self.root.title("POS")

		self.background_colour = "green"
		self.forground_colour = "blue"

		self.createframes()
		self.start_login_frame()

		self.root.mainloop()

	def createframes(self):
		self.login_frame = Frame(self.root, bg=self.background_colour, height = 480, width=800)
		self.login_frame.pack()

		self.invoice_frame = Frame(self.root)
		self.invoice_frame.pack()
		self.invoice_frame.pack_forget()

	def start_login_frame(self):
		self.login_frame_label = Label(self.login_frame, text="Enter Login Number", font=("Arial", 30), bg=self.background_colour, fg=self.forground_colour)
		self.login_frame_label.place(anchor=CENTER, relx= 0.5, rely = 0.3)

		self.login_frame_entry = Entry(self.login_frame, width = 25, font = ("Arial", 25))
		self.login_frame_entry.place(anchor=CENTER, relx=0.5, rely=0.4)
		self.login_frame_entry.focus()
		
		self.login_frame_button = Button(self.login_frame, text="Login", width = 10, height= 2, font = ("Arial", 25))
		self.login_frame_button.place(anchor=CENTER, relx=0.5, rely=0.6)

		self.login_frame_button_open_settings = Button(self.login_frame, text="Open Databse", bg=self.background_colour, width=15, height=2, command=self.open_databse_viewer)
		self.login_frame_button_open_settings.place(anchor=SE, relx=0.95, rely=0.95)

		self.fullscreen_button = Button(self.login_frame, text="Toggle Screen", width = 10, height= 2, font = ("Arial", 15), command = self.toggle_screen)
		self.fullscreen_button.place(anchor=CENTER, relx=0.1, rely=0.05)

	def toggle_screen(self):
		if self.fullscreen == False:
			self.root.attributes("-fullscreen", True)
			self.fullscreen = True
		else:
			self.root.attributes("-fullscreen", False)
			self.fullscreen = False

	def start_invoice_frame(Self):
		return True

	def process_login(self):
		return True

	def open_databse_viewer(self):
		database_view.run()

		
		return	True


