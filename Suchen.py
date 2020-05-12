#!/usr/bin/env python3

import tkinter as tk 
import os
import tkinter.messagebox as tkm
from tkinter.filedialog import askopenfilename, askdirectory    
from datetime import datetime


Hauptfenster=tk.Tk()


Hauptfenster.title("Daten suchen") #Titel festlegen
Hauptfenster.config(bg="cornsilk2")


Hauptfenster.wm_geometry("600x600")
Hauptfenster.resizable(0,0)


backFrame = tk.Frame(master=Hauptfenster,width=400,height=400,bg='cornsilk3')
backFrame.place(x=0, y=0, width=600, height=350)


## Funktionen

def Pfad_auslesen(pfad1):
    #global standardpfad
    Pfad=askdirectory(initialdir=pfad1)
    pfad.set(Pfad)


class Zeitfeld:
    def __init__(self,von_oder_bis,Zeiteinheit):
        self.von_oder_bis=von_oder_bis
        self.Zeiteinheit=Zeiteinheit
        
            

    def Farbe_weiß(self):
        Zeiteinheit=self.Zeiteinheit
        von_oder_bis=self.von_oder_bis
        if Zeiteinheit=="Datum":
            if von_oder_bis=="von":
                Tag_von.config(bg="white")
                Monat_von.config(bg="white")
                Jahr_von.config(bg="white")
                
            elif von_oder_bis=="bis":
                Tag_bis.config(bg="white")
                Monat_bis.config(bg="white")
                Jahr_bis.config(bg="white")
        
        if Zeiteinheit=="Uhrzeit":
            if von_oder_bis=="von":
                Stunde_von.config(bg="white")
                Minute_von.config(bg="white")
                
                
            elif von_oder_bis=="bis":
                Stunde_bis.config(bg="white")
                Minute_bis.config(bg="white")

    def Farbe_rot(self):
        Zeiteinheit=self.Zeiteinheit
        von_oder_bis=self.von_oder_bis
        if Zeiteinheit=="Datum":
            if von_oder_bis=="von":
                Tag_von.config(bg="red")
                Monat_von.config(bg="red")
                Jahr_von.config(bg="red")
                
            elif von_oder_bis=="bis":
                Tag_bis.config(bg="red")
                Monat_bis.config(bg="red")
                Jahr_bis.config(bg="red")
        
        if Zeiteinheit=="Uhrzeit":
            if von_oder_bis=="von":
                Stunde_von.config(bg="red")
                Minute_von.config(bg="red")
                
                
            elif von_oder_bis=="bis":
                Stunde_bis.config(bg="red")
                Minute_bis.config(bg="red")
    
    def Uhrzeit_pruefen(self):
        Zeiteinheit=self.Zeiteinheit
        von_oder_bis=self.von_oder_bis

        if Zeiteinheit=="Uhrzeit" and von_oder_bis=="von":
            self.stunde=Stunde_von.get()
            self.minute=Minute_von.get()
        elif Zeiteinheit=="Uhrzeit" and von_oder_bis=="bis":
            self.stunde=Stunde_bis.get()
            self.minute=Minute_bis.get()

        try:
            if self.stunde!="" or self.minute!="" :
                uhrzeit=datetime.strptime(self.stunde+" "+self.minute,"%H %M")
                self.Farbe_weiß()
            elif self.stunde=="" or self.minute=="":
                uhrzeit="leer"
                self.Farbe_weiß()
            else:
                tkm.showinfo("Uhrzeiteingabe","Bitte vollständige Uhrzeit bei "+"'"+von_oder_bis +"'" "eintragen")
                uhrzeit="leer"
        except:
            tkm.showwarning("Eingabefehler","Uhrzeiteingabe fehlerhaft: \n Format: HH MM  \n Prüfen ob Uhrzeit existiert")
            self.Farbe_rot()
            uhrzeit="leer"
    
        return uhrzeit
    
    def Datum_pruefen(self):
        
        Zeiteinheit=self.Zeiteinheit
        von_oder_bis=self.von_oder_bis
        
        if Zeiteinheit=="Datum" and von_oder_bis=="von":
            self.tag=Tag_von.get()
            self.monat=Monat_von.get()
            self.jahr=Jahr_von.get()
        elif Zeiteinheit=="Datum" and von_oder_bis=="bis":
            self.tag=Tag_bis.get()
            self.monat=Monat_bis.get()
            self.jahr=Jahr_bis.get()
        
        try:
            if self.tag!="" or self.monat!="" or self.jahr!="":
                datum=datetime.strptime(self.tag+" "+self.monat+" "+self.jahr,"%d %m %Y")
                self.Farbe_weiß()
            elif self.tag=="" or self.monat=="" or self.jahr=="":
                datum="leer"
                self.Farbe_weiß()
            else:
                tkm.showinfo("Datumseingabe","Bitte vollständiges Datum bei "+"'"+von_oder_bis +"'" "eintragen")
                datum="leer"
        except:
            tkm.showwarning("Eingabefehler","Datumseingabe fehlerhaft: \n Format: TT MM JJJJ \n Prüfen ob Datum existiert")
            self.Farbe_rot()
            datum="leer"
    
        return datum



def Suchen():
    datum_von=Datum_von.Datum_pruefen()
    datum_bis=Datum_bis.Datum_pruefen()
    
    uhrzeit_von=Uhrzeit_von.Uhrzeit_pruefen()
    uhrzeit_bis=Uhrzeit_bis.Uhrzeit_pruefen()

    print(datum_von)
    print(datum_bis)
    print(uhrzeit_von)
    print(uhrzeit_bis)

### Objekte ###

#Überschrift
tk.Label(Hauptfenster, text="Dateien und Ordner suchen",fg="black",font="Arial 12",bg="cornsilk2",justify="center").place(x=150, y=5, width=350, height=20)

#Pfad
y_Pfadeingabe=30

tk.Label(Hauptfenster, text="1. Pfad \n auswählen",fg="black",font="Arial 11",bg="cornsilk2",justify="center").place(x=10, y=y_Pfadeingabe, width=120, height=30)

pfad=tk.StringVar()
#global standardpfad
standardpfad="/home/"
pfad.set(standardpfad) # Standardpfad
Pfadeingabe=tk.Entry(Hauptfenster,textvariable=pfad)
Pfadeingabe.place(x=210, y=y_Pfadeingabe, width=350, height=30)
tk.Label(Hauptfenster, text="Suchpfad",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w").place(x=210, y=y_Pfadeingabe+25, width=350, height=16)

Pfadöffnen=tk.Button(Hauptfenster, text='Öffnen',font="Arial 10", width=25, command=lambda: Pfad_auslesen(standardpfad))
Pfadöffnen.place(x=140, y=y_Pfadeingabe, width=50, height=30)





#Begriff Eingabe

y_Eingabebegriff=140

tk.Label(Hauptfenster, text="2. Begriff \n eingeben und \n Optionen wählen",fg="black",font="Arial 11",bg="cornsilk2",justify="center").place(x=10, y=y_Eingabebegriff-50, width=120, height=60)

#Begrifffeld
Begriffeingabe=tk.Entry(Hauptfenster)
Begriffeingabe.place(x=210, y=y_Eingabebegriff, width=350, height=30)
Begriffeingabe_Label=tk.Label(Hauptfenster, text="Suchbegriff",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w")
Begriffeingabe_Label.place(x=210, y=y_Eingabebegriff+25, width=350, height=16)

#Dateityp
Dateitypeingabe=tk.Entry(Hauptfenster)
Dateitypeingabe.place(x=210, y=y_Eingabebegriff-50, width=55, height=30)
tk.Label(Hauptfenster, text="Dateityp",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w").place(x=210, y=y_Eingabebegriff-50+25, width=55, height=16)

#Checkbox Sterne
Sterneeingabe=tk.Checkbutton(Hauptfenster, width=30, height=30)
Sterneeingabe.place(x=300, y=y_Eingabebegriff-50, width=20, height=20)
tk.Label(Hauptfenster, text="Begriff an jeder Stelle des Dateinamens",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w").place(x=320, y=y_Eingabebegriff-50, width=250, height=20)

Sterneeingabe.select() #Checkbutton anwählen

#Zeiten

y_Zeit_von=y_Eingabebegriff+60

tk.Label(Hauptfenster, text="3. Zeitfenster \n optional eingeben",fg="black",font="Arial 11",bg="cornsilk2",justify="center").place(x=10, y=y_Zeit_von, width=120, height=60)

#Zeit von

tk.Label(Hauptfenster, text="von",fg="black",font="Arial 12",bg="cornsilk2",justify="center").place(x=150, y=y_Zeit_von+10, width=50, height=16)

Tag_von=tk.Entry(Hauptfenster)
Monat_von=tk.Entry(Hauptfenster)
Jahr_von=tk.Entry(Hauptfenster)
Stunde_von=tk.Entry(Hauptfenster)
Minute_von=tk.Entry(Hauptfenster)

Tag_von.place(x=210, y=y_Zeit_von, width=50, height=30)
tk.Label(Hauptfenster, text="Tag",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=210, y=y_Zeit_von+30, width=50, height=16)
Monat_von.place(x=260, y=y_Zeit_von, width=50, height=30)
tk.Label(Hauptfenster, text="Monat",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=260, y=y_Zeit_von+30, width=50, height=16)
Jahr_von.place(x=310, y=y_Zeit_von, width=50, height=30)
tk.Label(Hauptfenster, text="Jahr",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=310, y=y_Zeit_von+30, width=50, height=16)
Stunde_von.place(x=390, y=y_Zeit_von, width=50, height=30)
tk.Label(Hauptfenster, text="Stunde",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=390, y=y_Zeit_von+30, width=50, height=16)
Minute_von.place(x=440, y=y_Zeit_von, width=50, height=30)
tk.Label(Hauptfenster, text="Minute",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=440, y=y_Zeit_von+30, width=50, height=16)

#Zeit bis

y_Zeit_bis=y_Zeit_von+45

tk.Label(Hauptfenster, text="bis",fg="black",font="Arial 12",bg="cornsilk2",justify="center").place(x=150, y=y_Zeit_bis+10, width=50, height=16)

Tag_bis=tk.Entry(Hauptfenster)
Monat_bis=tk.Entry(Hauptfenster)
Jahr_bis=tk.Entry(Hauptfenster)
Stunde_bis=tk.Entry(Hauptfenster)
Minute_bis=tk.Entry(Hauptfenster)

Tag_bis.place(x=210, y=y_Zeit_bis, width=50, height=30)
tk.Label(Hauptfenster, text="Tag",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=210, y=y_Zeit_von+30, width=50, height=16)
Monat_bis.place(x=260, y=y_Zeit_bis, width=50, height=30)
tk.Label(Hauptfenster, text="Monat",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=260, y=y_Zeit_von+30, width=50, height=16)
Jahr_bis.place(x=310, y=y_Zeit_bis, width=50, height=30)
tk.Label(Hauptfenster, text="Jahr",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=310, y=y_Zeit_von+30, width=50, height=16)
Stunde_bis.place(x=390, y=y_Zeit_bis, width=50, height=30)
tk.Label(Hauptfenster, text="Stunde",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=390, y=y_Zeit_von+30, width=50, height=16)
Minute_bis.place(x=440, y=y_Zeit_bis, width=50, height=30)
tk.Label(Hauptfenster, text="Minute",fg="black",font="Arial 10",bg="cornsilk2",justify="center").place(x=440, y=y_Zeit_von+30, width=50, height=16)

#Zeitfeldklassen:

Datum_von=Zeitfeld("von","Datum")
Datum_bis=Zeitfeld("bis","Datum")
Uhrzeit_von=Zeitfeld("von","Uhrzeit")
Uhrzeit_bis=Zeitfeld("bis","Uhrzeit")


#Auswertebutton

Suchbutton=tk.Button(Hauptfenster, text='4. SUCHEN',font="Arial 10 bold", command=Suchen)
Suchbutton.place(x=10, y=y_Zeit_bis+30, width=125, height=60)


#Ausgabefeld
Ausgabefeld=tk.Text(Hauptfenster)
Ausgabefeld.place(x=0, y=y_Zeit_bis+100, width=580, height=250)

Scrollbar_Ausgabe=tk.Scrollbar(Hauptfenster)
Scrollbar_Ausgabe.place(x=580, y=y_Zeit_bis+100, width=20, height=250)

Scrollbar_Ausgabe.config(command=Ausgabefeld.yview)
Ausgabefeld.config(yscrollcommand=Scrollbar_Ausgabe.set)

############################################

Hauptfenster.mainloop() #Starten des gebauten Formulars









