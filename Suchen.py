#!/usr/bin/env python3

import tkinter as tk 
#from tkinter import *
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
import pickle
import sys

### Variablen

global Suchergebnis_Liste
global Dateimanager
global standardpfad
global Einstellungsfenster



#Einstellungen laden

def Einstellungen_laden():
    global Dateimanager
    global standardpfad

    try:
        aktueller_pfad=os.path.dirname(os.path.abspath(sys.argv[0]))
        
        fb=open(aktueller_pfad+"/"+"Einstellungen.pkl","rb")
        Einstellungen=pickle.load(fb)
        fb.close()

        Pfadvorgabe=Einstellungen[0]
        Dateimanagervorgabe=Einstellungen[1]
        
        Dateimanager=Dateimanagervorgabe
        standardpfad=Pfadvorgabe

    except:
        tkm.showerror("FEHLER","Laden von Einstellungen nicht möglich")
        os.abort()

    return Einstellungen

Einstellungen_laden()

## Hauptfenster

Hauptfenster=tk.Tk()


Hauptfenster.title("Daten suchen") #Titel festlegen
Hauptfenster.config(bg="cornsilk2")


Hauptfenster.wm_geometry("600x600")
Hauptfenster.resizable(0,0)


backFrame = tk.Frame(master=Hauptfenster,width=400,height=400,bg='cornsilk3')
backFrame.place(x=0, y=0, width=600, height=400)




## Funktionen

def Pfad_auslesen(pfad1):
    global standardpfad
    global Hauptfenster

    Pfad=askdirectory(initialdir=pfad1,parent=Hauptfenster)

    if Pfad=="":
        Pfad=standardpfad
    else:
        Pfad=Pfad+"/"
    
    pfad.set(Pfad)
    standardpfad=Pfad
    


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

class Button_Ordner_öffnen:

    global frame

    def __init__(self,nummer):
        self.nummer=nummer
        Button_Öffnen=tk.Button(frame,text="Ordner öffnen",command=lambda: self.Ordner_öffnen(self.nummer))
        Button_Öffnen.grid(row=self.nummer+1,column=3)



    def Ordner_öffnen(self,Suchergebnisnummer):
        global Suchergebnis_Liste
        global Dateimanager
        ordnerpfad=Suchergebnis_Liste.loc[Suchergebnisnummer,"Ordnerpfad"]
        subprocess.call([Dateimanager,ordnerpfad])
        return 

def kompletten_Pfad_erstellen(punktpfad,suchpfad):
    punktpfad=punktpfad[2:]
    kompletter_Pfad=suchpfad+punktpfad
    return kompletter_Pfad

def Dateiname_extrahieren(kompletter_Pfad):
    if os.path.isfile(kompletter_Pfad):
        Ordnerpfad,Dateiname=os.path.split(kompletter_Pfad)
    else:
        Ordnerpfad=kompletter_Pfad
        Dateiname="keine Datei"
    return (Ordnerpfad,Dateiname)

def Suchen():
    #Ausgabefeld leeren+ Wartezeit starten
    Ausgabefeld.delete("1.0",tk.END)
    Wartefeld.start()
    Wartetext.place(x=210, y=290, width=300, height=16)

    #Zeiten abfragen

    datum_von=Datum_von.Datum_pruefen()
    datum_bis=Datum_bis.Datum_pruefen()
    uhrzeit_von=Uhrzeit_von.Uhrzeit_pruefen()
    uhrzeit_bis=Uhrzeit_bis.Uhrzeit_pruefen()

    try:
        if uhrzeit_von!="leer":
            datum_von=datum_von.replace(hour=uhrzeit_von.hour)
            datum_von=datum_von.replace(minute=uhrzeit_von.minute)
            zeit_von=datum_von
        else:
            zeit_von=datum_von
    except:
        zeit_von=datetime.now().replace(hour=uhrzeit_von.hour)
        zeit_von=zeit_von.replace(minute=uhrzeit_von.minute)
        tkm.showinfo("Zeit von","Zeit von auf aktuelles Datum gesetzt")


    try:
        if uhrzeit_bis!="leer":
            datum_bis=datum_bis.replace(hour=uhrzeit_bis.hour)
            datum_bis=datum_bis.replace(minute=uhrzeit_bis.minute)
            zeit_bis=datum_bis
        else:
            zeit_bis=datum_bis
    
    except:
        zeit_bis=datetime.now().replace(hour=uhrzeit_bis.hour)
        zeit_bis=zeit_bis.replace(minute=uhrzeit_bis.minute)
        tkm.showinfo("Zeit bis","Zeit bis auf aktuelles Datum gesetzt")
    
    

   
    
    #Suchbegriff prüfen

    Suchbegriff=Begriffeingabe.get()

    #Dateityp prüfen

    Dateityp=Dateitypeingabe.get()

    if Dateityp!="":
        Suchbegriff=Suchbegriff+"*"+"."+Dateityp




    if Suchbegriff=="":
        tkm.showwarning("Fehlender Suchbegriff","Bitte Suchbegriff eingeben")
        Begriffeingabe.config(bg="red")
        return
    
    if Sterneeingabe_Check.get()==True:
        Suchbegriff="*"+str(Suchbegriff)+"*"

    

    Begriffeingabe.config(bg="white")

    #Dateien und Ordner Check
    

    if Ordner_check.get()==True and Dateien_check.get()==False:
        Filetype=("-type","d")
    elif Dateien_check.get()==True and Ordner_check.get()==False:
        Filetype=("-type","f")
    
    elif Dateien_check.get()==False and Ordner_check.get()==False:
        Ordner_Checkbox.select()
        Ordner_Dateien.select()
        Filetype=()
        tkm.showinfo("Suchart","Es werden Dateien und Ordner gesucht")

    if Dateien_check.get()==True and Ordner_check.get()==True:
        Filetype=()


    #SUCHEN

    try:
        os.chdir(pfad.get()) #Zum Suchverzeichnis wechseln
        Pfadeingabe.config(bg="white")
    except:
        if pfad.get()=="":
            tkm.showwarning("Warnung","Bitte Suchordner angeben")
            Pfadeingabe.config(bg="red")
            return
        else:
            tkm.showerror("Fehler","Es konnte nichts ins angegebene Verzeichnis gewechselt werden")
            Pfadeingabe.config(bg="red")
            return

    
    
    if zeit_bis=="leer" and zeit_von=="leer":
        
        Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}"""],stdout=subprocess.PIPE)
        if Filetype!=():
            Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""",Filetype[0],Filetype[1]],stdout=subprocess.PIPE)


    else:
        aktuelles_Datum=datetime.now().date()
        if zeit_bis!="leer" and zeit_von!="leer":
            zeitparameter1="+"+str((aktuelles_Datum-zeit_bis.date()).days-1)
            zeitparameter2="-"+str((aktuelles_Datum-zeit_von.date()).days+1)
            Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""","-mtime",zeitparameter1,"-mtime",zeitparameter2],stdout=subprocess.PIPE)
            if Filetype!=():
                Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""","-mtime",zeitparameter1,"-mtime",zeitparameter2,Filetype[0],Filetype[1]],stdout=subprocess.PIPE)

        elif zeit_bis!="leer" and zeit_von=="leer":
            zeitparameter1="+"+str((aktuelles_Datum-zeit_bis.date()).days-1)
            Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""","-mtime",zeitparameter1],stdout=subprocess.PIPE)
            if Filetype!=():
                Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""","-mtime",zeitparameter1,Filetype[0],Filetype[1]],stdout=subprocess.PIPE)


        elif zeit_bis=="leer" and zeit_von!="leer":
            zeitparameter2="-"+str((aktuelles_Datum-zeit_von.date()).days+1)
            Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""","-mtime",zeitparameter2],stdout=subprocess.PIPE)
            if Filetype!=():
                Suchergebnis=subprocess.run(["find","-iname",f"""{Suchbegriff}""","-mtime",zeitparameter2,Filetype[0],Filetype[1]],stdout=subprocess.PIPE)
    
    Ausgabefeld.insert("1.0",str(Suchergebnis.stdout.decode()))

    #Suchergebnis zerlegen
    Suchergebnis=Suchergebnis.stdout.decode().split(sep="\n")
    del Suchergebnis[-1]
    global Suchergebnis_Liste
    Suchergebnis_Liste=pd.DataFrame()
    Suchergebnis_Liste["kompletter Pfad"]=Suchergebnis
    Suchergebnis_Liste["kompletter Pfad"]=Suchergebnis_Liste["kompletter Pfad"].apply(lambda x:kompletten_Pfad_erstellen(x,pfad.get()))#####################################################
    Suchergebnis_Liste["Dateiname"]=Suchergebnis_Liste["kompletter Pfad"].apply(lambda x:Dateiname_extrahieren(x)[1])
    Suchergebnis_Liste["Ordnerpfad"]=Suchergebnis_Liste["kompletter Pfad"].apply(lambda x:Dateiname_extrahieren(x)[0])
    Suchergebnis_Liste["Änderungsdatum"]=Suchergebnis_Liste["kompletter Pfad"].apply(lambda x:os.path.getmtime(x))
    Suchergebnis_Liste["Änderungsdatum"]=Suchergebnis_Liste["Änderungsdatum"].apply(lambda x:datetime.fromtimestamp(x))

    #Suchergebnis nach Uhrzeiten filtern
    if zeit_bis!="leer" and zeit_von!="leer":
        Suchergebnis_Liste=Suchergebnis_Liste.where((Suchergebnis_Liste["Änderungsdatum"]>zeit_von) & (Suchergebnis_Liste["Änderungsdatum"]<zeit_bis)).dropna()
    elif zeit_bis!="leer" and zeit_von=="leer":
        Suchergebnis_Liste=Suchergebnis_Liste.where(Suchergebnis_Liste["Änderungsdatum"]<zeit_bis).dropna()
    
    elif zeit_bis=="leer" and zeit_von!="leer":
        Suchergebnis_Liste=Suchergebnis_Liste.where(Suchergebnis_Liste["Änderungsdatum"]>zeit_von).dropna()

    #Liste für Ausgabe aufbereiten Ordnerpfad, Dateiname, Änderungsdatum
    Suchergebnis_Liste=Suchergebnis_Liste.loc[:,("Ordnerpfad","Dateiname","Änderungsdatum")]

    #Daten ausgeben

    print("Zeit bis: ",zeit_bis)
    print("Zeit von: ",zeit_von)
    print("Dateityp: "+ Dateityp)
    print("Suchbegriff: "+ Suchbegriff)
    print("Sterneeingabe: "+str(Sterneeingabe_Check.get()))
    
    print(".............")
    print(Suchergebnis_Liste)
    print("Anzahl Suchergebnisse: "+str(len(Suchergebnis_Liste)))
    
    print("---------------------------")

    

    if len(Suchergebnis_Liste)>1000:
        tkm.showinfo("Hinweis","Es gibt mehr als 1000 Suchergebnisse")
        Suchergebnis_Liste=Suchergebnis_Liste.iloc[0:1000,:]
        Anzahl_Ergebnisse.config(text="mehr als 1000")
    else:
        Anzahl_Ergebnisse.config(text=str(len(Suchergebnis_Liste)))
    

    Wartefeld.stop()
    Wartetext.place_forget()

    if Suchergebnis_Liste.empty==False:
        Suchergebnisse_anzeigen_Button.config(state=tk.NORMAL)
    else:
        tkm.showinfo("kein Suchergebnis","keine Ordner und Dateien gefunden")
    
    
def Pfad_zerlegen(pfad,max_Zeichen):
    pfadteile=pfad.split(sep="/")
    del pfadteile[0]
    pfadteile=list(reversed(pfadteile))
    Ausgabepfad_temp=""
    Ausgabepfad=""
    while pfadteile!=[]:
        
        if len(Ausgabepfad_temp+pfadteile[-1])<max_Zeichen:
            pfadteil=pfadteile.pop()
            Ausgabepfad_temp=Ausgabepfad_temp+"/"+pfadteil
        else:
            Ausgabepfad=Ausgabepfad+Ausgabepfad_temp+"\n"
            Ausgabepfad_temp=""

    Ausgabepfad=Ausgabepfad+Ausgabepfad_temp
    return Ausgabepfad




def Suchergebnisse_anzeigen():
    global Suchergebnis_Liste
    if Suchergebnis_Liste.empty==True:
        tkm.showinfo("Hinweis","Keine Suchergebnisse verfügbar")
        return

    ## Ergebnisfenster

    Ergebnisfenster=tk.Tk()
    Ergebnisfenster.title("Suchergebnisse") #Titel festlegen
    Ergebnisfenster.config(bg="cornsilk2")
    Ergebnisfenster.wm_geometry("1000x600")
    Ergebnisfenster.resizable(0,0)
    
    
    Suchergebnis_Tabelle_Inhalt=dict.fromkeys(list(Suchergebnis_Liste.index.values))
    Suchergebnis_Tabelle_Spalten=Suchergebnis_Liste.columns.values
    
    for key in Suchergebnis_Tabelle_Inhalt.keys():
        zeile=dict()
        for column in Suchergebnis_Tabelle_Spalten:
            zeile[column]=Suchergebnis_Liste.loc[key,column]
        Suchergebnis_Tabelle_Inhalt[key]=zeile

    class AutoScrollbar(tk.Scrollbar):
    # A scrollbar that hides itself if it's not needed.
    # Only works if you use the grid geometry manager!
        def set(self, lo, hi):
            if float(lo) <= 0.0 and float(hi) >= 1.0:
                # grid_remove is currently missing from Tkinter!
                self.tk.call("grid", "remove", self)
            else:
                self.grid()
            tk.Scrollbar.set(self, lo, hi)
        def pack(self, **kw):
            raise tk.TclError("cannot use pack with this widget")
        def place(self, **kw):
            raise tk.TclError("cannot use place with this widget")

    vscrollbar = AutoScrollbar(Ergebnisfenster)
    vscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
    hscrollbar = AutoScrollbar(Ergebnisfenster, orient=tk.HORIZONTAL)
    hscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)

    canvas = tk.Canvas(Ergebnisfenster, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
    canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

    vscrollbar.config(command=canvas.yview)
    hscrollbar.config(command=canvas.xview)

    # make the canvas expandable
    Ergebnisfenster.grid_rowconfigure(0, weight=1)
    Ergebnisfenster.grid_columnconfigure(0, weight=1)

    # create canvas contents
    global frame
    frame = tk.Frame(canvas)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)

    rows = len(Suchergebnis_Liste)
    
    tk.Label(frame,text="Ordnerpfad",font="Arial 11 bold").grid(row=0,column=0)
    tk.Label(frame,text="Dateiname",font="Arial 11 bold").grid(row=0,column=1)
    tk.Label(frame,text="Änderungsdatum",font="Arial 11 bold").grid(row=0,column=2)


    for i in range(rows):
        Button_Ordner_öffnen(i)
        


        
        Feld_ordnerpfad = tk.Text(frame,width=50,state=tk.NORMAL,height=3)
        Feld_ordnerpfad.insert("0.0",Pfad_zerlegen(str(Suchergebnis_Liste.iloc[i,0]),49))
              
        Feld_ordnerpfad.grid(row=i+1, column=0, sticky='news',ipady=0,pady=0)
        Feld_ordnerpfad.config(state=tk.DISABLED)#,disabledbackground='white',disabledforeground="black")

        Feld_Dateiname=tk.Entry(frame,width=35,state=tk.NORMAL)
        Feld_Dateiname.insert(0,str(Suchergebnis_Liste.iloc[i,1]))
        Feld_Dateiname.grid(row=i+1, column=1, sticky='news')
        Feld_Dateiname.config(state=tk.DISABLED,disabledbackground='white',disabledforeground="black")

        Feld_Änderungsdatum=tk.Entry(frame,width=20,state=tk.NORMAL)
        Feld_Änderungsdatum.grid(row=i+1, column=2, sticky='news')
        Feld_Änderungsdatum.insert(0,datetime.strftime(Suchergebnis_Liste.iloc[i,2],"%d.%m.%Y %H:%M:%S"))
        Feld_Änderungsdatum.config(state=tk.DISABLED,disabledbackground='white',disabledforeground="black")
    

    

    canvas.create_window(0, 0, anchor=tk.NW, window=frame)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    
    




    

    
    


### Objekte ###

#Überschrift
tk.Label(Hauptfenster, text="Dateien und Ordner suchen",fg="black",font="Arial 12",bg="cornsilk2",justify="center").place(x=150, y=5, width=350, height=20)

#Pfad
y_Pfadeingabe=30

tk.Label(Hauptfenster, text="1. Pfad \n auswählen",fg="black",font="Arial 11",bg="cornsilk2",justify="center").place(x=10, y=y_Pfadeingabe, width=120, height=30)

pfad=tk.StringVar()

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
Sterneeingabe_Check=tk.BooleanVar()

Sterneeingabe=tk.Checkbutton(Hauptfenster, width=30, height=30,var=Sterneeingabe_Check)
Sterneeingabe.place(x=300, y=y_Eingabebegriff-65, width=20, height=20)
tk.Label(Hauptfenster, text="Begriff an jeder Stelle des Dateinamens",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w").place(x=320, y=y_Eingabebegriff-65, width=250, height=20)

Sterneeingabe.select() #Checkbutton anwählen


#Checkbox Ordner
Ordner_check=tk.BooleanVar()
Ordner_Checkbox=tk.Checkbutton(Hauptfenster, width=30, height=30,var=Ordner_check)
Ordner_Checkbox.place(x=300, y=y_Eingabebegriff-45, width=20, height=20)
tk.Label(Hauptfenster, text="Ordner suchen",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w").place(x=320, y=y_Eingabebegriff-45, width=250, height=20)

Ordner_Checkbox.select() #Checkbutton anwählen

#Checkbox Dateien
Dateien_check=tk.BooleanVar()
Ordner_Dateien=tk.Checkbutton(Hauptfenster, width=30, height=30,var=Dateien_check)
Ordner_Dateien.place(x=300, y=y_Eingabebegriff-25, width=20, height=20)
tk.Label(Hauptfenster, text="Dateien suchen",fg="black",font="Arial 10",bg="cornsilk2",justify="left",anchor="w").place(x=320, y=y_Eingabebegriff-25, width=250, height=20)

Ordner_Dateien.select() #Checkbutton anwählen

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

#Progressbar
Wartefeld=ttk.Progressbar(Hauptfenster, orient="horizontal", length=200, mode="determinate")
Wartefeld.place(x=210,y=310,width=300,height=20)

Wartetext=tk.Label(Hauptfenster, text="Suchvorgang läuft - Bitte warten ...",fg="black",font="Arial 10",bg="yellow",justify="center")


#Ausgabefeld
Ausgabefeld=tk.Text(Hauptfenster)
Ausgabefeld.place(x=0, y=y_Zeit_bis+150, width=580, height=200)

Scrollbar_Ausgabe=tk.Scrollbar(Hauptfenster)
Scrollbar_Ausgabe.place(x=580, y=y_Zeit_bis+150, width=20, height=200)

Scrollbar_Ausgabe.config(command=Ausgabefeld.yview)
Ausgabefeld.config(yscrollcommand=Scrollbar_Ausgabe.set)

#Anzahl Suchergebnisse
tk.Label(Hauptfenster,fg="black",font="Arial 10",justify="center",text="Anzahl \n Versuchsergebnisse: ",bg="cornsilk2").place(x=210,y=y_Zeit_bis+100)
Anzahl_Ergebnisse=tk.Label(Hauptfenster,fg="black",font="Arial 13",bg="grey73",justify="center",text="0")
Anzahl_Ergebnisse.place(x=360, y=y_Zeit_bis+105)

#Ergebnisse anzeigen

Suchergebnisse_anzeigen_Button=tk.Button(Hauptfenster,state=tk.DISABLED, text='5. Ergebnisse \n anzeigen',font="Arial 10 bold", command=Suchergebnisse_anzeigen)#Suchergebnisse_anzeigen)
Suchergebnisse_anzeigen_Button.place(x=10, y=y_Zeit_bis+90, width=125, height=60)

#Einstellungsmenü

def Einstellungen_Speichern(Pfadvorgabe,Dateimanagervorgabe):
    
    aktueller_pfad=os.path.dirname(os.path.abspath(sys.argv[0]))
    
    Einstellungen=(Pfadvorgabe.get(),Dateimanagervorgabe.get())
    
    fb=open(aktueller_pfad+"/"+"Einstellungen.pkl","wb")
    pickle.dump(Einstellungen,fb)
    fb.close()


def Pfad_auslesen_Einstellungen(pfad1):
    global standardpfad
    global Pfadvorgabe
    global Dateimanagervorgabe
    global pfad
    global Einstellungsfenster

    

    Pfad=askdirectory(initialdir=pfad1,parent=Einstellungsfenster) # immer im  Vordergrund!!!
    
    if Pfad=="":
        Pfad=standardpfad
    else:
        Pfad=Pfad+"/"
    
    Pfadvorgabe.delete(0,tk.END)
    Pfadvorgabe.insert(0,Pfad)
    standardpfad=Pfad
    pfad.set(standardpfad)
    
    Einstellungen_Speichern(Pfadvorgabe,Dateimanagervorgabe)

    #Einstellungsfenster.wm_attributes('-topmost', 1)

   #Einstellungsfenster.lift() #Fenster in den Vordergrund
    
    



def Einstellungen_öffnen():
    
    global Pfadvorgabe
    global Dateimanagervorgabe
    global Einstellungsfenster

    Einstellungsfenster=tk.Tk()
    
    Einstellungsfenster.title("Einstellungen und Vorgaben")
    tk.Label(Einstellungsfenster,text="Einstellungen",font="Arial 11 bold underline").grid(row=0,column=1)
    
    tk.Label(Einstellungsfenster,text="Standard-Suchpfad",font="Arial 10").grid(row=1,column=0,sticky=tk.W)
    Pfadvorgabe=tk.Entry(Einstellungsfenster,width=40)
    Pfadvorgabe.grid(row=1,column=1)

    tk.Label(Einstellungsfenster,text="Dateimanager - Befehl",font="Arial 10").grid(row=2,column=0)
    Dateimanagervorgabe=tk.Entry(Einstellungsfenster,width=40)
    Dateimanagervorgabe.grid(row=2,column=1)

    tk.Button(Einstellungsfenster,text="Speichern",command=lambda:Einstellungen_Speichern(Pfadvorgabe,Dateimanagervorgabe)).grid(row=3,column=1)

    

    Einstellungen=Einstellungen_laden()

    Pfadvorgabe.insert(0,Einstellungen[0])
    Dateimanagervorgabe.insert(0,Einstellungen[1])

    Button_Pfad_öffnen=tk.Button(Einstellungsfenster,text="Öffnen",command=lambda:Pfad_auslesen_Einstellungen(standardpfad))
    Button_Pfad_öffnen.grid(row=1,column=3)

    
    

    Einstellungsfenster.mainloop()

    

   
    





menu = tk.Menu(Hauptfenster)
Hauptfenster.config(menu=menu)

filemenu = tk.Menu(menu)
menu.add_cascade(label="Einstellungen", menu=filemenu)
filemenu.add_command(label="Vorgaben", command=Einstellungen_öffnen)

############################################

#if 'normal' != Einstellungsfenster.state():
 #       print ('running')
  #      #Hauptfenster.deiconify()
   #     print(Einstellungsfenster.state())



Hauptfenster.mainloop() #Starten des gebauten Formulars









