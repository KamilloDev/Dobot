import tkinter as tk
from tkinter import ttk
from cam import Cam
from PIL import ImageTk, Image

import time
import pydobot
import threading


class Dobot_dummy():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0
	
	def pose(self):
		return self.x,self.y,self.z,0,0,0,0,0

	def move_to(self, x,y,z,r, wait=False):
		if wait:
			time.sleep(0.5)
		self.x = x
		self.y = y
		self.z = z
		return None

class Main(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)

		# Hvis I ikke har noget USB-kamera tilkoblet,
		# skal I formentlig bruge Cam(0) for at få fat i
		# kameraet på jeres skærm.
		# Hvis I sætter et USB-kamera til, skal I
		# formentlig bruge Cam(1)
		self.cam = Cam(0)
		cam = threading.Thread(target=self.update_view)
		cam.start()
		self.dobot = pydobot.Dobot(port="COM8")

		self.create_interface()
		self.update_view()
  
		self.cube_colors = [60, 0, 240, 120]
		self.cube_names = ["Yellow","Red","Blue","Green"]
		self.plade = [[0 for _ in range(4)] for _ in range(4)]
		self.red = 0
		self.blue = 0
		self.yellow = 0
		self.green = 0
		self.x = 0
		self.y = 0
  
		
	def _from_rgb(self,rgb):
			r, g, b = rgb
			return f'#{r:02x}{g:02x}{b:02x}'  

	def move(self, x, y):
		r = 90
		self.dobot.move_to(274+(x*20), 66+(y*20), 20, r, True)
		self.dobot.move_to(274+(x*20), 66+(y*20), -40, r, True)
		self.dobot.suck(True)
		self.dobot.move_to(274+(x*20), 66+(y*20), 20, r, True)
		self.dobot.move_to(270+(x*20), -37+(y*20)-100, 20, r, True)
		self.dobot.move_to(270+(x*20), -37+(y*20)-100, -38, r, True)
		self.dobot.suck(False)
		self.dobot.move_to(270+(x*20), -37+(y*20)-100, 20, r, True)

	def move_specific(self, old_x, old_y, new_x, new_y):
		r = 90
		self.dobot.move_to(274+(old_x*20), 66+(old_y*20), 20, r, True)
		self.dobot.move_to(274+(old_x*20), 66+(old_y*20), -38, r, True)
		self.dobot.suck(True)
		self.dobot.move_to(274+(old_x*20), 66+(old_y*20), 20, r, True)
		self.dobot.move_to(270+(new_x*20), -37+(new_y*20)-100, 20, r, True)
		self.dobot.move_to(270+(new_x*20), -37+(new_y*20)-100, -38, r, True)
		self.dobot.suck(False)
		self.dobot.move_to(270+(new_x*20), -37+(new_y*20)-100, 20, r, True)

	def get_closest_color(self, col):
		if col >= 170 and col <= 179 or col >= 0 and col <= 10:
			return 1
		elif col >=22 and col <= 42:
			return 0
		elif col >= 43 and col <= 82:
			return 3
		elif col >= 95 and col <= 127:
			return 2
			

	def increment_coords(self):
		if self.x == 3:
			self.y += 1
			self.x = 0
		else:
			self.x += 1

	def get_color_plade(self):
		selcted_color = self.combo_color.get()
		r = 90
		self.dobot.move_to(200, 50, 0, r, True)
		for y in range(4):
			for x in range(4):
				if self.plade[y][x] == 0 and "Yellow" == selcted_color:
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
				elif self.plade[y][x] == 1 and "Red" == selcted_color:
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
				elif self.plade[y][x] == 2 and "Blue" == selcted_color:
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
				elif self.plade[y][x] == 3 and "Green" == selcted_color:
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()


	def get_color(self):
		selcted_color = self.combo_color.get()
		r = 90
		self.dobot.move_to(200, 50, 0, r, True)
		for x in range(4):
			for y in range(4):
				self.dobot.move_to(274-46+(x*20), 66-16+(y*20),-30,r,True)
				col = self.cam.read_color_hsv(320,240).tolist()
				index = self.get_closest_color(col[0])

				if index == 0 and "Yellow" == selcted_color:
					print(f"{col} - Yellow!")
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
				elif index == 1 and "Red" == selcted_color:
					print(f"{col} - Red!")
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
				elif index == 2 and "Blue" == selcted_color:
					print(f"{col} - Blue!")
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
				elif index == 3 and "Green" == selcted_color:
					print(f"{col} - Green!")
					self.move_specific(x, y, self.x, self.y)
					self.increment_coords()
					
	
	def calibrate(self):
		r = 90
		self.red = 0
		self.blue = 0
		self.yellow = 0
		self.green = 0
		self.dobot.move_to(200, 50, 0, r, True)
		for x in range(4):
			for y in range(4):
				self.dobot.move_to(274-46+(x*20), 66-16+(y*20),-30,r,True)
				col = self.cam.read_color_hsv(320,240).tolist()
				index = self.get_closest_color(col[0])
		
				if index == 0 :
					print(f"{col} - Yellow!")
					self.plade[y][x] = 0
					self.yellow += 1
				elif index == 1:
					print(f"{col} - Red!")
					self.plade[y][x] = 1
					self.red += 1
				elif index == 2:
					print(f"{col} - Blue!")
					self.plade[y][x] = 2
					self.blue += 1
				elif index == 3:
					print(f"{col} - Green!")
					self.plade[y][x] = 3
					self.green += 1
		
		self.label_yellow.configure(text=f"Ammount of yellow is: {self.yellow}")
		self.label_red.configure(text=f"Ammount of red is: {self.red}")
		self.label_blue.configure(text=f"Ammount of blue is: {self.blue}")
		self.label_green.configure(text=f"Ammount of green is: {self.green}")
	

	def update_view(self):
		self.cam.make_frame()
		frame = self.cam.frame
		img = Image.fromarray(frame)
		imgtk = ImageTk.PhotoImage(image=img)
		self.lbl_show_frame.imgtk = imgtk
		self.lbl_show_frame.configure(image=imgtk)

		self.after(5, self.update_view)


	def create_interface(self):
		self.main_frame = tk.Frame(self)

		self.titel = tk.Label(self.main_frame, text="Brick terminal")
		self.combo_color = ttk.Combobox(self.main_frame)
		self.combo_color['values'] = ['Yellow', 'Red', 'Blue', 'Green']
		self.get = tk.Button(self.main_frame, text="Get", command=self.get_color_plade)
		self.scan_and_go = tk.Button(self.main_frame, text="Scan and get", command=self.get_color)
		self.calibrate_bt = tk.Button(self.main_frame, text="Calibrate", command=self.calibrate)
		self.label_yellow = tk.Label(self.main_frame, text="Scan before getting yellow ammount!")
		self.label_red = tk.Label(self.main_frame, text="Scan before getting red ammount!")
		self.label_blue = tk.Label(self.main_frame, text="Scan before getting blue ammount!")
		self.label_green = tk.Label(self.main_frame, text="Scan before getting green ammount!")
		self.lbl_show_frame = tk.Label(self.main_frame)
		
		self.titel.grid(row=0, column=0)
		self.combo_color.grid(row=0, column=1)
		self.get.grid(row=0, column=3)
		self.scan_and_go.grid(row=0, column=4)
		self.calibrate_bt.grid(row=0, column=5)
		self.label_yellow.grid(row=1, column=1)
		self.label_red.grid(row=2, column=1)
		self.label_blue.grid(row=3, column=1)
		self.label_green.grid(row=4, column=1)
		self.lbl_show_frame.grid(row=5,column=0, rowspan=2)
		self.main_frame.pack(padx = 20, pady=10)
		
		self.pack()


root = tk.Tk()
root.title("Dobot")

interface = Main()
interface.mainloop()