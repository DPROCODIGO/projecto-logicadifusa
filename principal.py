import tkinter as tk
from tkinter import ttk, font, Label, PhotoImage
import matplotlib.pyplot as plt
from Values import Colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import numpy as np
import skfuzzy as fuzz
import sys

ventana = tk.Tk()
ventana.title("Primera Ventana")
ventana.geometry("920x600")
ventana.resizable(False,False)

def ingresar():
    BIniciar.place_forget()
    lblImage1.place_forget()
    lblFondo.place_forget()
    varEntradas()
    grafEdad()

    bEdad.place(x=363, y=50, width=87)
    bIngreso.place(x=450, y=50, width=80)
    bCapPago.place(x=530, y=50, width=150)
    bTiempo.place(x=680, y=50, width=60)
    bHijos.place(x=740, y=50, width=50)
    bDeudas.place(x=790, y=50, width=95)


#Rutas
RutaLogo="Imagenes\Logo2.png"
RutaBackground="Imagenes\Background.png"
RutaSearch="Imagenes\Search.png"

Logo = PhotoImage(file=RutaLogo)
BG =PhotoImage(file=RutaBackground)
Search =PhotoImage(file=RutaSearch)

#Labels y Buttons
lblFondo=Label(ventana,image=BG)
lblFondo.place(x=0,y=0)
lblImage1=Label(ventana,image=Logo,bg=Colors.ColorPrimary)
lblImage1.place(x=381.91,y=79)

FontTitle = font.Font(family="helvetica", size=10, weight="bold")
Ari18 = font.Font(family='Arial', size=18)
comp = font.Font(family='helvetica', size=10, weight="bold")

#ROBOTO, 24
BIniciar = tk.Button(ventana, bg=Colors.ColorSecundary, text="INICIAR", font=Ari18, command=ingresar)
BIniciar.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
BIniciar.place(x=394,  y=430, width=131, height=55)

##Menu
def varEntradas():
    lblFormCliente = tk.Label(ventana, text="DATOS DEL CLIENTE", font=FontTitle)
    lblFormCliente.place(x=40, y=50)

    lblID = tk.Label(ventana, text="DNI: ")
    lblID.place(x=40, y=90)
    cID = tk.Entry(ventana)
    cID.place(x=150, y=90)

    bComprobar = tk.Button(ventana,image=Search)
    bComprobar.configure(relief=tk.GROOVE, background='white', activebackground=Colors.ColorSecundaryDark)
    bComprobar.place(x=257, y=90, width=20, height=20)

    lblNombre = tk.Label(ventana, text="Nombres: ")
    lblNombre.place(x=40, y=120)
    lENombre = tk.Entry(ventana)
    lENombre.place(x=150, y=120)

    lblApellido = tk.Label(ventana, text="Apellidos: ")
    lblApellido.place(x=40, y=150)
    lEApellido = tk.Entry(ventana)
    lEApellido.place(x=150, y=150)

    lblEmail = tk.Label(ventana, text="Correo: ")
    lblEmail.place(x=40, y=180)
    lEEmail = tk.Entry(ventana)
    lEEmail.place(x=150, y=180)

    lblCelular = tk.Label(ventana, text="Celular: ")
    lblCelular.place(x=40, y=210)
    lECelular = tk.Entry(ventana)
    lECelular.place(x=150, y=210)

    Sep= ttk.Separator(ventana)
    Sep.place(x=40, y=250,relwidth=0.27)

    lblFormEval = tk.Label(ventana, text="EVALUAR PRESTAMO", font=FontTitle)
    lblFormEval.place(x=40, y=270)

    lblEdad = tk.Label(ventana, text="Edad: ")
    lblEdad.place(x=40, y=300)
    cEdad = ttk.Combobox(state="readonly")
    cEdad["values"] = ["Joven", "Adulto", "Anciano"]
    cEdad.place(x=150, y=300)

    lblIngreso = tk.Label(ventana, text="Ingreso: ")
    lblIngreso.place(x=40, y=330)
    cIngreso = ttk.Combobox(state="readonly")
    cIngreso["values"] = ["Bajo", "Media", "Alta"]
    cIngreso.place(x=150, y=330)

    lblCapPago = tk.Label(ventana, text="Capacidad\nde pago: ")
    lblCapPago.place(x=40, y=360)
    cCapPago = ttk.Combobox(state="readonly")
    cCapPago["values"] = ["Bajo", "Moderado", "Alto"]
    cCapPago.place(x=150, y=360)

    lblTiempo = tk.Label(ventana, text="Tiempo: ")
    lblTiempo.place(x=40, y=400)
    cTiempo = ttk.Combobox(state="readonly")
    cTiempo["values"] = ["Nuevo", "Promedio", "Antiguo"]
    cTiempo.place(x=150, y=400)

    lblHijos = tk.Label(ventana, text="Hijos: ")
    lblHijos.place(x=40, y=430)
    cHijos = ttk.Combobox(state="readonly")
    cHijos["values"] = ["Bajo", "Moderado", "Alto"]
    cHijos.place(x=150, y=430)

    lblDeudas = tk.Label(ventana, text="Endeudamientos: ")
    lblDeudas.place(x=40, y=460)
    cDeudas = ttk.Combobox(state="readonly")
    cDeudas["values"] = ["Bajo", "Moderado", "Alto"]
    cDeudas.place(x=150, y=460)

    bEvaluar = tk.Button(ventana, bg=Colors.ColorSecundary, text="EVALUAR", font=comp, command=ingresar)
    bEvaluar.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
    bEvaluar.place(x=120,y=500)


def switchEdad():
    if (bEdad['state'] == tk.NORMAL):
        #Edad
        bEdad['state'] = tk.DISABLED
        bEdad['bg']= Colors.ColorsDisabled
        grafEdad()
        #Ingreso
        bIngreso['state'] = tk.NORMAL
        bIngreso['bg'] = Colors.ColorSecundary
        #CapPago
        bCapPago['state'] = tk.NORMAL
        bCapPago['bg'] = Colors.ColorSecundary
        #Tiempo
        bTiempo['state'] = tk.NORMAL
        bTiempo['bg'] = Colors.ColorSecundary
        #Hijos
        bHijos['state'] = tk.NORMAL
        bHijos['bg'] = Colors.ColorSecundary
        # Deudas
        bDeudas['state'] = tk.NORMAL
        bDeudas['bg'] = Colors.ColorSecundary

def switchIngreso():
    if (bIngreso['state'] == tk.NORMAL):
        #Edad
        bEdad['state'] = tk.NORMAL
        bEdad['bg'] = Colors.ColorSecundary
        # Ingreso
        bIngreso['state'] = tk.DISABLED
        bIngreso['bg'] = Colors.ColorsDisabled
        grafIngresos()
        # CapPago
        bCapPago['state'] = tk.NORMAL
        bCapPago['bg'] = Colors.ColorSecundary
        # Tiempo
        bTiempo['state'] = tk.NORMAL
        bTiempo['bg'] = Colors.ColorSecundary
        # Hijos
        bHijos['state'] = tk.NORMAL
        bHijos['bg'] = Colors.ColorSecundary
        # Deudas
        bDeudas['state'] = tk.NORMAL
        bDeudas['bg'] = Colors.ColorSecundary

def switchCapPago():
    if (bCapPago['state'] == tk.NORMAL):
        # Edad
        bEdad['state'] = tk.NORMAL
        bEdad['bg'] = Colors.ColorSecundary
        # Ingreso
        bIngreso['state'] = tk.NORMAL
        bIngreso['bg'] = Colors.ColorSecundary
        # CapPago
        bCapPago['state'] = tk.DISABLED
        bCapPago['bg'] = Colors.ColorsDisabled
        grafCapPago()
        # Tiempo
        bTiempo['state'] = tk.NORMAL
        bTiempo['bg'] = Colors.ColorSecundary
        # Hijos
        bHijos['state'] = tk.NORMAL
        bHijos['bg'] = Colors.ColorSecundary
        # Deudas
        bDeudas['state'] = tk.NORMAL
        bDeudas['bg'] = Colors.ColorSecundary

def switchTiempo():
    if (bTiempo['state'] == tk.NORMAL):
        #Edad
        bEdad['state'] = tk.NORMAL
        bEdad['bg'] = Colors.ColorSecundary
        # Ingreso
        bIngreso['state'] = tk.NORMAL
        bIngreso['bg'] = Colors.ColorSecundary
        # CapPago
        bCapPago['state'] = tk.NORMAL
        bCapPago['bg'] = Colors.ColorSecundary
        # Tiempo
        bTiempo['state'] = tk.DISABLED
        bTiempo['bg'] = Colors.ColorsDisabled
        grafTiempo()
        # Hijos
        bHijos['state'] = tk.NORMAL
        bHijos['bg'] = Colors.ColorSecundary
        # Deudas
        bDeudas['state'] = tk.NORMAL
        bDeudas['bg'] = Colors.ColorSecundary

def switchHijos():
    if (bHijos['state'] == tk.NORMAL):
        #Edad
        bEdad['state'] = tk.NORMAL
        bEdad['bg'] = Colors.ColorSecundary
        # Ingreso
        bIngreso['state'] = tk.NORMAL
        bIngreso['bg'] = Colors.ColorSecundary
        # CapPago
        bCapPago['state'] = tk.NORMAL
        bCapPago['bg'] = Colors.ColorSecundary
        # Tiempo
        bTiempo['state'] = tk.NORMAL
        bTiempo['bg'] = Colors.ColorSecundary
        # Hijos
        bHijos['state'] = tk.DISABLED
        bHijos['bg'] = Colors.ColorsDisabled
        grafHijos()
        # Deudas
        bDeudas['state'] = tk.NORMAL
        bDeudas['bg'] = Colors.ColorSecundary

def switchDeudas():
    if (bDeudas['state'] == tk.NORMAL):
        #Edad
        bEdad['state'] = tk.NORMAL
        bEdad['bg'] = Colors.ColorSecundary
        # Ingreso
        bIngreso['state'] = tk.NORMAL
        bIngreso['bg'] = Colors.ColorSecundary
        # CapPago
        bCapPago['state'] = tk.NORMAL
        bCapPago['bg'] = Colors.ColorSecundary
        # Tiempo
        bTiempo['state'] = tk.NORMAL
        bTiempo['bg'] = Colors.ColorSecundary
        # Hijos
        bHijos['state'] = tk.NORMAL
        bHijos['bg'] = Colors.ColorSecundary
        # Deudas
        bDeudas['state'] = tk.DISABLED
        bDeudas['bg'] = Colors.ColorsDisabled
        grafDeudas()


SVar=font.Font(size = 10,weight="bold")
bEdad = tk.Button(ventana, bg=Colors.ColorSecundary, text="EDAD", state=tk.DISABLED, command=switchEdad, font=SVar)
bEdad.configure(relief=tk.GROOVE, background="#e2e2e0", activebackground=Colors.ColorSecundaryDark)

bIngreso = tk.Button(ventana,bg=Colors.ColorSecundary, text="INGRESOS",state=tk.NORMAL,command=switchIngreso,font= SVar)
bIngreso.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)

bCapPago = tk.Button(ventana, bg=Colors.ColorSecundary, text="CAPACIDAD DE PAGO",state=tk.NORMAL,command=switchCapPago,font= SVar)
bCapPago.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)

bTiempo = tk.Button(ventana, bg=Colors.ColorSecundary, text="TIEMPO",state=tk.NORMAL,command=switchTiempo,font= SVar)
bTiempo.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)

bHijos = tk.Button(ventana, bg=Colors.ColorSecundary, text="HIJOS",state=tk.NORMAL,command=switchHijos,font= SVar)
bHijos.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)

bDeudas = tk.Button(ventana, bg=Colors.ColorSecundary, text="DEUDAS",state=tk.NORMAL,command=switchDeudas,font= SVar)
bDeudas.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)

#SKFUZZY

#Reglas
# Rango de la calidad de la edad (años)
x_edad = np.arange(18, 85, 1)

# Rango de la calidad del ingresos (soles)
x_ingreso = np.arange(930, 5000, 1)

# Rango del porcentaje de capapago (soles)
x_capapago = np.arange(500, 1000, 1)

# Rango del porcentaje de tiempo (meses)
x_tiempo = np.arange(0, 12, 1)

# Rango del porcentaje de hijos (cantidad)
x_hijos = np.arange(0, 8, 1)

# Rango del porcentaje de deudas (meses)
x_deudas = np.arange(1, 4, 1)


#Edad Joven
ed_jo = fuzz.trapmf(x_edad,[18,18,23,25])
#Edad Adulta
ed_ad = fuzz.trapmf(x_edad,[20,25,60,65])
#Edad Anciano
ed_vi = fuzz.trapmf(x_edad,[60,65,70,75])


#Ingreso Bajo
in_ba = fuzz.trimf(x_ingreso,[930,930,1600])
#Ingreso Medio
in_me = fuzz.trimf(x_ingreso,[1400,1600,5000])
#Ingreso Alto
in_al = fuzz.trimf(x_ingreso,[4000,5000,5000])


#CapPaog Bajo
cp_ba = fuzz.trimf(x_capapago,[500,500,700])
#CapPaog Medio
cp_me = fuzz.trimf(x_capapago,[600,700,1100])
#CapPaog Alto
cp_al = fuzz.trimf(x_capapago,[700,1100,1100])

#Tiempo nuevo
ti_nu = fuzz.trimf(x_tiempo,[0,0,3])
#Tiempo promedio
ti_pr = fuzz.trimf(x_tiempo,[0,3,6])
#Tiempo antiguo
ti_an = fuzz.trimf(x_tiempo,[3,6,12])

#Hijos bajo
hi_ba = fuzz.trimf(x_hijos,[0,0,1])
#Hijos moderado
hi_mo = fuzz.trimf(x_hijos,[0,1,3])
#Hijos alto
hi_al = fuzz.trimf(x_hijos,[1,3,5])

#Deudas bajas
de_ba = fuzz.trimf(x_deudas,[0,0,1])
#Deudas medio
de_me = fuzz.trimf(x_deudas,[0,1,2])
#Deudas alto
de_al = fuzz.trimf(x_deudas,[1,2,3])

def grafEdad():
    figEdad, ax0 = plt.subplots(figsize=(5.5, 3))

    ax0.plot(x_edad,ed_jo,'r',linewidth=2,label="Joven")
    ax0.plot(x_edad,ed_ad,'g',linewidth=2,label="Adulto")
    ax0.plot(x_edad,ed_vi,'b',linewidth=2,label="Anciano")
    ax0.set_title("Edad")
    ax0.legend()

    canvas = FigureCanvasTkAgg(figEdad,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

def grafIngresos():
    figIng, ax1 = plt.subplots(figsize=(5.5, 3))

    ax1.plot(x_ingreso,in_ba,'r',linewidth=2,label="Bajo")
    ax1.plot(x_ingreso,in_me,'g',linewidth=2,label="Medio")
    ax1.plot(x_ingreso,in_al,'b',linewidth=2,label="Alto")
    ax1.set_title("Ingresos")
    ax1.legend()

    canvas = FigureCanvasTkAgg(figIng,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

def grafCapPago():
    figCP, ax2 = plt.subplots(figsize=(5.5, 3))

    ax2.plot(x_capapago,cp_ba,'r',linewidth=2,label="Bajo")
    ax2.plot(x_capapago,cp_me,'g',linewidth=2,label="Medio")
    ax2.plot(x_capapago,cp_al,'b',linewidth=2,label="Alto")
    ax2.set_title("Capacidad de Pago")
    ax2.legend()

    canvas = FigureCanvasTkAgg(figCP,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

def grafTiempo():
    figT, ax3 = plt.subplots(figsize=(5.5, 3))

    ax3.plot(x_tiempo,ti_nu,'r',linewidth=2,label="Nuevo")
    ax3.plot(x_tiempo,ti_pr,'g',linewidth=2,label="Promedio")
    ax3.plot(x_tiempo,ti_an,'b',linewidth=2,label="Antiguo")
    ax3.set_title("Tiempo Trabajando")
    ax3.legend()

    canvas = FigureCanvasTkAgg(figT,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

def grafHijos():
    figHi, ax4 = plt.subplots(figsize=(5.5, 3))

    ax4.plot(x_hijos,hi_ba,'r',linewidth=2,label="Bajo")
    ax4.plot(x_hijos,hi_mo,'g',linewidth=2,label="Moderado")
    ax4.plot(x_hijos,hi_al,'b',linewidth=2,label="Alto")
    ax4.set_title("Hijos")
    ax4.legend()

    canvas = FigureCanvasTkAgg(figHi,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

def grafDeudas():
    figDe, ax5 = plt.subplots(figsize=(5.5, 3))

    ax5.plot(x_deudas,de_ba,'r',linewidth=2,label="Bajo")
    ax5.plot(x_deudas,de_me,'g',linewidth=2,label="Moderado")
    ax5.plot(x_deudas,de_al,'b',linewidth=2,label="Alto")
    ax5.set_title("Hijos")
    ax5.legend()

    canvas = FigureCanvasTkAgg(figDe,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

edad=34
ingreso = 2500

edad_lvl_jo = fuzz.interp_membership(x_edad, ed_jo, edad)
edad_lvl_ad = fuzz.interp_membership(x_edad, ed_ad, edad)
edad_lvl_vi = fuzz.interp_membership(x_edad, ed_vi, edad)

ingreso_lvl_ba = fuzz.interp_membership(x_ingreso, in_ba, ingreso)
ingreso_lvl_me = fuzz.interp_membership(x_ingreso, in_me, ingreso)
ingreso_lvl_al = fuzz.interp_membership(x_ingreso, in_al, ingreso)

activar_regla_1 = np.fmax(edad_lvl_jo, ingreso_lvl_ba)
prestamo = np.fmin(activar_regla_1, cp_ba) # removed entirely to 0
prestamo_md = np.fmin(ingreso_lvl_me, cp_me)





ventana.mainloop()