import tkinter as tk
from cam import Cam
from PIL import ImageTk, Image

import time
from serial.tools import list_ports
import pydobot
import numpy as np


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

        self.cube_colors = [[213,190,30],[255,5,35],[125,198,111], [5,153,244]]
        self.cube_names = ["Gul","Rød","Grøn","Blå"]


        self.create_interface()


        ports = list_ports.comports()

        # Sæt simulate = True hvis I ikke har en robot
        # Sæt simulate = False hvis I har en robot
        simulate = True
        if simulate:
            self.dobot = Dobot_dummy()
        else:
            for i, port in enumerate(ports):
                print(f"{i}: {port.device} ({port.description})")
            #p = int(input("Port: "))
            p = 0
            port = None
            if len(ports) > 0 and len(ports) > p:
                port = ports[p].device

            #device = pydobot.Dobot(port=port, verbose=True)
            self.dobot = pydobot.Dobot(port=port)
            r = 90
            #Her skal robotten hente en klods, og føre den over kameraet, for at undersøge om den er gul
            self.dobot.move_to(274-46, 66-15,-30,r,False)

        self.update_view()


    def get_yellow(self):
        r = 90
        #Her skal robotten hente en klods, og føre den over kameraet, for at undersøge om den er gul
        self.dobot.move_to(274-46, 66-15,-30,r,True)


    # Denne funktion kører automatisk, og sørger for at vise billedet fra kameraet
    # og farven på en udvalgt pixel.
    def update_view(self):
        self.cam.make_frame()

        frame = self.cam.frame
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lbl_show_frame.imgtk = imgtk
        self.lbl_show_frame.configure(image=imgtk)

        col = self.cam.read_color(320,240)
        self.lbl_indicator.configure(bg=self._from_rgb(col))
        index = self.get_closest_color(col)
        self.lbl_color.configure(text=f"Farve: {col} ({self.cube_names[index]})")

        self.after(30, self.update_view)	


    def get_closest_color(self, col):
        min_afstand = 3*(255)+1
        min_index = -1
        for index,tjek_color in enumerate(self.cube_colors):
            afstand = 0
            for c in range(3):
                afstand = afstand + (col[c] - tjek_color[c])
            if afstand < min_afstand:
                min_afstand = afstand
                min_index = index
        return min_index

    # Her oprettes vores brugerinterface.
    # I kan selv tilføje de widgets, I har behov for
    def create_interface(self):
        self.main_frame = tk.Frame(self)

        # Tilføj her
        self.lbl_color = tk.Label(self.main_frame, text="Farve:")
        self.lbl_color.grid(row=2,column=0)


        self.but_yellow = tk.Button(self.main_frame, text="Gul", command=self.get_yellow)
        self.but_yellow.grid(row=0,column=0)
        self.lbl_indicator = tk.Label(self.main_frame, width=20, height = 5, text = "")
        self.lbl_indicator.grid(row=1, column=0)
        self.lbl_show_frame = tk.Label(self.main_frame)
        self.lbl_show_frame.grid(row=0,column=1, rowspan=2)
        self.main_frame.pack(padx = 20, pady=10)

        self.pack()

    # Denne lille funktion laver farvekoden fra 
    # kameraet om til et format, som tkinter kan bruge
    def _from_rgb(self,rgb):
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'





root = tk.Tk()
root.title("Dobot")

interface = Main()
interface.mainloop()