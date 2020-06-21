import tkinter as tk
from tkinter import ttk, font, Label, PhotoImage
import matplotlib.pyplot as plt
from Values import Colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import numpy as np
import skfuzzy as fuzz
import sys

ventana = tk.Tk()
ventana.title("UDELLA - EVALUADOR DE PRÉSTAMO")
ventana.geometry("920x600")
ventana.resizable(False,False)
ventana.configure(bg=Colors.ColorWhite)

def ingresar():
    BIniciar.place_forget()
    lblImage1.place_forget()
    lblFondo.place_forget()
    varEntradas()
    grafEdad()

    bEdad.place(x=413, y=50, width=47)
    bIngreso.place(x=460, y=50, width=80)
    bCapPago.place(x=540, y=50, width=150)
    bTiempo.place(x=690, y=50, width=60)
    bHijos.place(x=750, y=50, width=50)
    bDeudas.place(x=800, y=50, width=85)
    bPrestamo.place(x=333, y=50, width=80)


#Rutas
RutaLogo="Imagenes\Logo.png"
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
    lblFormCliente = tk.Label(ventana, text="DATOS DEL CLIENTE", font=FontTitle,bg=Colors.ColorWhite)
    lblFormCliente.place(x=40, y=50)

    lblID = tk.Label(ventana, text="DNI: ",bg=Colors.ColorWhite)
    lblID.place(x=40, y=90)
    cID = tk.Entry(ventana)
    cID.place(x=150, y=90)

    bComprobar = tk.Button(ventana,image=Search)
    bComprobar.configure(relief=tk.GROOVE, background=Colors.ColorWhite, activebackground=Colors.ColorSecundaryDark)
    bComprobar.place(x=257, y=90, width=20, height=20)

    lblNombre = tk.Label(ventana,bg=Colors.ColorWhite, text="Nombres: ")
    lblNombre.place(x=40, y=120)
    lENombre = tk.Entry(ventana)
    lENombre.place(x=150, y=120)

    lblApellido = tk.Label(ventana,bg=Colors.ColorWhite, text="Apellidos: ")
    lblApellido.place(x=40, y=150)
    lEApellido = tk.Entry(ventana)
    lEApellido.place(x=150, y=150)

    lblEmail = tk.Label(ventana, bg=Colors.ColorWhite,text="Correo: ")
    lblEmail.place(x=40, y=180)
    lEEmail = tk.Entry(ventana)
    lEEmail.place(x=150, y=180)

    lblCelular = tk.Label(ventana,bg=Colors.ColorWhite, text="Celular: ")
    lblCelular.place(x=40, y=210)
    lECelular = tk.Entry(ventana)
    lECelular.place(x=150, y=210)

    Sep= ttk.Separator(ventana)
    Sep.place(x=40, y=250,relwidth=0.27)

    lblFormEval = tk.Label(ventana, text="EVALUAR PRÉSTAMO",bg=Colors.ColorWhite, font=FontTitle)
    lblFormEval.place(x=40, y=270)

    lblEdad = tk.Label(ventana, bg=Colors.ColorWhite,text="Edad: ")
    lblEdad.place(x=40, y=300)
    cEdad = tk.Entry(ventana)
    cEdad.place(x=150, y=300)

    lblIngreso = tk.Label(ventana, bg=Colors.ColorWhite,text="Ingreso: ")
    lblIngreso.place(x=40, y=330)
    cIngreso = tk.Entry(ventana)
    cIngreso.place(x=150, y=330)

    lblCapPago = tk.Label(ventana, bg=Colors.ColorWhite,text="Capacidad\nde pago: ")
    lblCapPago.place(x=40, y=360)
    cCapPago = tk.Entry(ventana)
    cCapPago.place(x=150, y=360)

    lblTiempo = tk.Label(ventana,bg=Colors.ColorWhite, text="Tiempo: ")
    lblTiempo.place(x=40, y=400)
    cTiempo = tk.Entry(ventana)
    cTiempo.place(x=150, y=400)

    lblHijos = tk.Label(ventana, bg=Colors.ColorWhite,text="Hijos: ")
    lblHijos.place(x=40, y=430)
    cHijos = tk.Entry(ventana)
    cHijos.place(x=150, y=430)

    lblDeudas = tk.Label(ventana, bg=Colors.ColorWhite,text="Endeudamientos: ")
    lblDeudas.place(x=40, y=460)
    cDeudas = tk.Entry(ventana)
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
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida

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
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida

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
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida

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
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida

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
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida

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
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida

def switchPrestamo():
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
        bDeudas['state'] = tk.NORMAL
        bDeudas['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.DISABLED
        bPrestamo['bg'] = Colors.ColorsDisabled
        grafPrestamo()

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

bPrestamo = tk.Button(ventana, bg=Colors.ColorSecundary, text="PRÉSTAMO",state=tk.NORMAL,command=switchPrestamo,font= SVar)
bPrestamo.configure(relief=tk.GROOVE, background=Colors.ColorSalida, activebackground=Colors.ColorSalidaDark)

#SKFUZZY

#Reglas
# Rango de la calidad de la edad (años)
x_edad = np.arange(20, 65, 1)

# Rango de la calidad del ingresos (soles)
x_ingreso = np.arange(930, 15000, 1)

# Rango del porcentaje de capapago (soles)
x_capapago = np.arange(500, 5000, 1)

# Rango del porcentaje de tiempo (meses)
x_tiempo = np.arange(3, 24, 1)

# Rango del porcentaje de hijos (cantidad)
x_hijos = np.arange(0, 5, 1)

# Rango del porcentaje de deudas (semanas)
x_deudas = np.arange(0, 17, 1)

# Rango del porcentaje de préstamo (soles)
x_prestamo = np.arange(500, 50000, 1)

#Edad Joven
ed_jo = fuzz.trapmf(x_edad,[20,20,25,30])
#Edad Adulta
ed_ad = fuzz.trimf(x_edad,[25,40,55])
#Edad Anciano
ed_vi = fuzz.trapmf(x_edad,[50,55,65,65])


#Ingreso Bajo
in_ba = fuzz.trapmf(x_ingreso,[930,930,1200,1500])
#Ingreso Medio
in_me = fuzz.trimf(x_ingreso,[1350,3350,5000])
#Ingreso Alto
in_al = fuzz.trapmf(x_ingreso,[4000,5000,15000,15000])


#CapPago Bajo
cp_ba = fuzz.trapmf(x_capapago,[500,500,750,1100])
#CapPago Medio
cp_me = fuzz.trimf(x_capapago,[900,1500,2000])
#CapPago Alto
cp_al = fuzz.trapmf(x_capapago,[1700,3500,5000,5000])

#Tiempo nuevo
ti_nu = fuzz.trapmf(x_tiempo,[3,3,6,12])
#Tiempo promedio
ti_pr = fuzz.trimf(x_tiempo,[6,12,18])
#Tiempo antiguo
ti_an = fuzz.trapmf(x_tiempo,[12,18,24,24])

#Hijos bajo
hi_ba = fuzz.trapmf(x_hijos,[0,0,0,1])
#Hijos moderado
hi_mo = fuzz.trimf(x_hijos,[0,1,3])
#Hijos alto
hi_al = fuzz.trapmf(x_hijos,[1,3,5,5])

#Deudas bajas
de_ba = fuzz.trimf(x_deudas,[0,0,4])
#Deudas medio
de_me = fuzz.trimf(x_deudas,[2,8,12])
#Deudas alto
de_al = fuzz.trimf(x_deudas,[10,16,16])

#Préstamo bajas
pr_ba = fuzz.trimf(x_prestamo,[500,500,7500])
#Préstamo medio
pr_me = fuzz.trimf(x_prestamo,[5000,15000,30000])
#Préstamo alto
pr_al = fuzz.trimf(x_prestamo,[25000,50000,50000])

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
    ax5.set_title("Historial de Deudas")
    ax5.legend()

    canvas = FigureCanvasTkAgg(figDe,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

def grafPrestamo():
    figPr, ax6 = plt.subplots(figsize=(5.5, 3))

    ax6.plot(x_prestamo,pr_ba,'r',linewidth=2,label="Bajo")
    ax6.plot(x_prestamo,pr_me,'g',linewidth=2,label="Moderado")
    ax6.plot(x_prestamo,pr_al,'b',linewidth=2,label="Alto")
    ax6.set_title("Préstamo")
    ax6.legend()

    canvas = FigureCanvasTkAgg(figPr,master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333,y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

#Valores de entrada EJEMPLO
edad = 26
ingreso = 2500
hijos = 2
cap_pago = 750
tiempo = 3
deudas = 5


edad_lvl_jo = fuzz.interp_membership(x_edad, ed_jo, edad)
edad_lvl_ad = fuzz.interp_membership(x_edad, ed_ad, edad)
edad_lvl_vi = fuzz.interp_membership(x_edad, ed_vi, edad)

ingreso_lvl_ba = fuzz.interp_membership(x_ingreso, in_ba, ingreso)
ingreso_lvl_me = fuzz.interp_membership(x_ingreso, in_me, ingreso)
ingreso_lvl_al = fuzz.interp_membership(x_ingreso, in_al, ingreso)

hijos_lvl_ba = fuzz.interp_membership(x_hijos, hi_ba, hijos)
hijos_lvl_mo = fuzz.interp_membership(x_hijos, hi_mo, hijos)
hijos_lvl_al = fuzz.interp_membership(x_hijos, hi_al, hijos)

cappago_lvl_ba = fuzz.interp_membership(x_capapago, cp_ba, cap_pago)
cappago_lvl_me = fuzz.interp_membership(x_capapago, cp_me, cap_pago)
cappago_lvl_al = fuzz.interp_membership(x_capapago, cp_al, cap_pago)

tiempo_lvl_nu = fuzz.interp_membership(x_tiempo, ti_nu, tiempo)
tiempo_lvl_pr = fuzz.interp_membership(x_tiempo, ti_pr, tiempo)
tiempo_lvl_an = fuzz.interp_membership(x_tiempo, ti_an, tiempo)

deudas_lvl_ba = fuzz.interp_membership(x_deudas, de_ba, deudas)
deudas_lvl_me = fuzz.interp_membership(x_deudas, de_me, deudas)
deudas_lvl_al = fuzz.interp_membership(x_deudas, de_al, deudas)

#reglas INGRESOS - CAPACIDAD - EDAD - TIEMPO - HIJOS - DEUDAS
activar_regla_1 = np.fmax(ingreso_lvl_ba, cappago_lvl_ba)
activar_regla_2 = np.fmax(ingreso_lvl_me, cappago_lvl_me)
activar_regla_3 = np.fmax(ingreso_lvl_al, cappago_lvl_al)

prestamo_ba = np.fmin(activar_regla_1, pr_ba)
prestamo_md = np.fmin(activar_regla_2, pr_me)
prestamo_al = np.fmin(activar_regla_3, pr_al)

agregar = np.fmax(prestamo_ba,np.fmax(prestamo_md,prestamo_md))
prestamo = fuzz.defuzz(x_prestamo,agregar,'centroid')
print("RESULTADO PARA PROBAR, NO ES LA VERSION FINAL")
print("EL MONTO A PRESTAR ES DE: S/.",prestamo)

ventana.mainloop()