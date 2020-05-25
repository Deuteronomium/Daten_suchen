#!/usr/bin/env python3

import tkinter as tk 
from tkinter import *
import os
import tkinter.messagebox as tkm
from tkinter.filedialog import askopenfilename, askdirectory    
from datetime import datetime
import subprocess
from tkinter import ttk
import pandas as pd
from tkintertable import TableCanvas, TableModel
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') #DEUTSCHES FORMAT
from datetime import datetime,timezone

#from tkintertable.Tables import TableCanvas
#from tkintertable.TableModels import TableModel

### Variablen


## Hauptfenster

Hauptfenster=tk.Tk()


#Hauptfenster.title("Daten suchen") #Titel festlegen
#Hauptfenster.config(bg="cornsilk2")


#Hauptfenster.wm_geometry("1000x1000")
#Hauptfenster.resizable(0,0)


#backFrame = tk.Frame(master=Hauptfenster,width=600,height=400,bg='cornsilk3')
#backFrame.place(x=0, y=0, width=600, height=400)

#model = TableModel()

#table = TableCanvas(backFrame, model,
#			cellwidth=60, cellbackgr='#e3f698',
#			thefont=('Arial',12),rowheight=18, rowheaderwidth=30,
#			rowselectedcolor='yellow', editable=True)

#table.redraw()

data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
       'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}
       } 

#table = TableCanvas(backFrame, data=data)
#table.show()
#table.redraw()

frame = Frame(Hauptfenster)
frame.pack()

model = TableModel()
table = TableCanvas(frame, model,
			cellwidth=60, cellbackgr='#e3f698',
			thefont=('Arial',12),rowheight=18, rowheaderwidth=30,
			rowselectedcolor='yellow', editable=True,data=data)
#table.show()


#Hauptfenster.mainloop()


root = tk.Tk()

height = 5
width = 5
for i in range(height): #Rows
    for j in range(width): #Columns
        b = Entry(root, text="")
        b.grid(row=i, column=j)

root.mainloop()


print("ENDE")
