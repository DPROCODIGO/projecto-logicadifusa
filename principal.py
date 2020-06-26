import tkinter as tk
from tkinter import ttk, font, Label, PhotoImage, VERTICAL
import matplotlib.pyplot as plt
from Values import Colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import numpy as np
import skfuzzy as fuzz
import database
from tkinter import messagebox
import sqlite3

import sys

ventana = tk.Tk()
ventana.title("UDELLA - EVALUADOR DE PRÉSTAMO")
ventana.iconbitmap("Imagenes\icono.ico")
ventana.geometry("920x600")
ventana.resizable(False,False)
ventana.configure(bg=Colors.ColorWhite)

def login_screen():
    global lblImage1,lblFondo,lblPanel,cUsuario,cContraseña,lblUsuario,img_Usuario,lblContraseña
    global img_verPass,img_NoverPass,lblRecuperar,img_Contraseña
    lblFondo = Label(ventana, image=BG)
    lblFondo.place(x=0, y=0)
    lblImage1 = Label(ventana, image=Logo, bg=Colors.ColorPrimary)
    lblImage1.place(x=381.91, y=20)
    lblPanel = tk.Label(ventana, width=35, height=15, borderwidth=1, relief="sunken", bg=Colors.ColorPrimary)
    lblPanel.place(x=360, y=220)

    lblUsuario=tk.Label(ventana,text="Usuario:",bg=Colors.ColorPrimary,fg=Colors.ColorWhite,
                        font=font.Font(size=12,weight="bold"))
    lblUsuario.place(x=370,y=230)
    img_Usuario = tk.Label(ventana, image=Usuario, bg=Colors.ColorPrimary)
    img_Usuario.place(x=370, y=260)
    cUsuario = tk.Entry(ventana)
    cUsuario.place(x=410,y=260,width=160,height=25)

    lblContraseña = tk.Label(ventana, text="Contraseña:", bg=Colors.ColorPrimary, fg=Colors.ColorWhite,
                          font=font.Font(size=12, weight="bold"))
    lblContraseña.place(x=370, y=300)
    img_Contraseña = tk.Label(ventana, image=Contraseña, bg=Colors.ColorPrimary)
    img_Contraseña.place(x=370, y=330)
    cContraseña = tk.Entry(ventana,show="*")
    cContraseña.place(x=410, y=330, width=160, height=25)

    img_verPass = tk.Button(ventana, image=VerPass, bg=Colors.ColorPrimary,state=tk.NORMAL,command=switchpass,relief="flat")
    img_verPass.configure(activebackground=Colors.ColorPrimary)

    img_NoverPass = tk.Button(ventana, image=NoVerPass, bg=Colors.ColorPrimary,state=tk.NORMAL,command=switchNopass,relief="flat")
    img_NoverPass.configure(activebackground=Colors.ColorPrimary)
    img_NoverPass.place(x=575, y=330,height=25)

    lblRecuperar = tk.Button(ventana, text="¿Olvidaste la contraseña?", bg=Colors.ColorPrimary, fg=Colors.ColorWhite,
                             font=font.Font(size=8, weight="bold"),relief="flat")
    lblRecuperar.configure(activebackground=Colors.ColorPrimary,activeforeground=Colors.ColorWhite)
    lblRecuperar.place(x=427, y=360)

    global BIniciar
    BIniciar = tk.Button(ventana, bg=Colors.ColorSecundary, text="INGRESAR", font=Ari14, command=login)
    BIniciar.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
    BIniciar.place(x=420, y=400, width=120, height=30)

def login():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    User=cUsuario.get()
    Pass=cContraseña.get()
    miCursor.execute("SELECT * FROM EMPLEADOS WHERE Usuario=? AND Contraseña=?",(User,Pass))
    DatosEmpleado=miCursor.fetchall()

    for Empleado in DatosEmpleado:
        Rol=Empleado[3]

    if DatosEmpleado:
        if Rol=="ASESOR":
            messagebox.showinfo("LOGIN CORRECTO","ROL ASESOR")
            ingresar()
        elif Rol=="ADMINISTRADOR":
            messagebox.showinfo("LOGIN CORRECTO","ROL ADMIN")
            ingresar_admin()
    else:
        messagebox.showerror("LOGIN INCORRECTO","Usuario y/o Contraseña no valido")

def switchpass():
    if(img_verPass['state'] == tk.NORMAL):
        img_verPass.place_forget()
        img_NoverPass['state'] = tk.NORMAL
        img_NoverPass.place(x=575, y=330,height=25)
def switchNopass():
    if(img_NoverPass['state'] == tk.NORMAL):
        img_NoverPass.place_forget()
        img_verPass['state'] = tk.NORMAL
        img_verPass.place(x=575, y=330,height=25)

def crearCliente():
    try:
        miConexion=sqlite3.connect("BDPrestamoPersonal")

        miCursor=miConexion.cursor()

        miCursor.execute("INSERT INTO CLIENTES VALUES(NULL, '" + cDNI.get() +
            "','" + lENombre.get() +
            "','" + lEApellido.get() +
            "','" + lEEMail.get() +
            "','" + lECelular.get() +
            "','" + lEFech_Nac.get() +
            "',NULL,NULL)")

        miConexion.commit()

        messagebox.showinfo("BBDD","Registro insertado con éxito")
    except:
        messagebox.showwarning("¡Advertencia!","El usuario ya existe")

def buscarCliente():
    miConexion=sqlite3.connect("BDPrestamoPersonal")

    miCursor=miConexion.cursor()

    miCursor.execute("SELECT * FROM CLIENTES WHERE DNI="+cDNI.get())
    DatosCliente=miCursor.fetchall()

    for cliente in DatosCliente:
        micID.set(cliente[0])
        milENombre.set(cliente[2])
        milEApellido.set(cliente[3])
        milEEMail.set(cliente[4])
        milECelular.set(cliente[5])
        milEFech_Nac.set(cliente[6])
    miConexion.commit()

    calcular_edad()

def limpiarEntrys():
    micID.set("")
    micDNI.set("")
    milENombre.set("")
    milEApellido.set("")
    milEEMail.set("")
    milECelular.set("")
    milEFech_Nac.set("")

def calcular_edad():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("SELECT (strftime('%Y', 'now') - strftime('%Y', Fech_Nac )) - (strftime('%m-%d', 'now') < strftime('%m-%d', Fech_Nac )) from CLIENTES WHERE DNI="+cDNI.get())
    res = miCursor.fetchall()
    micEdad.set(res)

def close_loginScreen():
    lblFondo.place_forget()
    lblImage1.place_forget()
    BIniciar.place_forget()
    lblPanel.place_forget()
    cUsuario.place_forget()
    lblUsuario.place_forget()
    img_Usuario.place_forget()
    img_Contraseña.place_forget()
    cContraseña.place_forget()
    lblContraseña.place_forget()
    img_verPass.place_forget()
    img_NoverPass.place_forget()
    lblRecuperar.place_forget()

def ingresar_admin():
    close_loginScreen()
    MenuBar()
    global cVID,cVNombre,cVTipo,cValor1, cValor2, cValor3, cValor4,cBValor1,cBValor2,cBValor3,\
        cVal1Par1,cVal1Par2,cVal1Par3,cVal1Par4,cVal2Par1,cVal2Par2,cVal2Par3,cVal3Par1,cVal3Par2,cVal3Par3,cVal3Par4


    global micVID,micVNombre,micVTipo,micValor1, micValor2, micValor3, micValor4,micBValor1,micBValor2,micBValor3,\
        micVal1Par1,micVal1Par2,micVal1Par3,micVal1Par4,micVal2Par1,micVal2Par2,micVal2Par3,micVal3Par1,micVal3Par2,\
        micVal3Par3,micVal3Par4

    micVID = tk.StringVar()
    micVNombre = tk.StringVar()
    micVTipo = tk.StringVar()
    micValor1 = tk.StringVar()
    micValor2 = tk.StringVar()
    micValor3 = tk.StringVar()
    micValor4 = tk.StringVar()
    micBValor1 = tk.StringVar()
    micBValor2 = tk.StringVar()
    micBValor3 = tk.StringVar()
    micVal1Par1 = tk.StringVar()
    micVal1Par2 = tk.StringVar()
    micVal1Par3 = tk.StringVar()
    micVal1Par4 = tk.StringVar()
    micVal2Par1 = tk.StringVar()
    micVal2Par2 = tk.StringVar()
    micVal2Par3 = tk.StringVar()
    micVal3Par1 = tk.StringVar()
    micVal3Par2 = tk.StringVar()
    micVal3Par3 = tk.StringVar()
    micVal3Par4 = tk.StringVar()

    lblVariable = tk.Label(ventana, text="VARIABLES", font=font.Font(size=15, weight="bold"), bg="#FFFFFF")
    lblVariable.place(x=20, y=15)

    lblID = tk.Label(ventana,text="ID:",bg=Colors.ColorWhite)
    lblID.place(x=25,y=70)
    cVID=tk.Entry(ventana,textvariable=micVID)
    cVID.place(x=100,y=70)
    lblNombre = tk.Label(ventana, text="Nombre:",bg=Colors.ColorWhite)
    lblNombre.place(x=25, y=100)
    cVNombre = tk.Entry(ventana,textvariable=micVNombre)
    cVNombre.place(x=100, y=100)
    lblTipo = tk.Label(ventana, text="Tipo:",bg=Colors.ColorWhite)
    lblTipo.place(x=25, y=130)
    cVTipo = tk.Entry(ventana,textvariable=micVTipo)
    cVTipo.place(x=100, y=130)

    lblValorL=tk.Label(ventana,text="Valor \nLinguistico",font=font.Font(size=10,weight="bold"), bg="#FFFFFF")
    lblValorL.place(x=277,y=28)

    lblValorL = tk.Label(ventana, text="Función de \nPertenencia", font=font.Font(size=10, weight="bold"), bg="#FFFFFF")
    lblValorL.place(x=377, y=28)

    lblValorL = tk.Label(ventana, text="Parámetros", font=font.Font(size=10, weight="bold"), bg="#FFFFFF")
    lblValorL.place(x=500, y=34)

    cValor1 = tk.Entry(ventana,textvariable=micValor1)
    cValor1.place(x=275, y=70,width=75)
    cValor2 = tk.Entry(ventana,textvariable=micValor2)
    cValor2.place(x=275, y=100,width=75)
    cValor3 = tk.Entry(ventana,textvariable=micValor3)
    cValor3.place(x=275, y=130,width=75)

    cBValor1=ttk.Combobox(state="readonly",textvariable=micBValor1)
    cBValor1["values"]=["Triangular","Trapezoidal"]
    cBValor1.place(x=375,y=70,width=100)

    cBValor2 = ttk.Combobox(state="readonly",textvariable=micBValor2)
    cBValor2["values"] = ["Triangular", "Trapezoidal"]
    cBValor2.place(x=375, y=100,width=100)

    cBValor3 = ttk.Combobox(state="readonly",textvariable=micBValor3)
    cBValor3["values"] = ["Triangular", "Trapezoidal"]
    cBValor3.place(x=375, y=130,width=100)

    cVal1Par1 = tk.Entry(ventana,textvariable=micVal1Par1)
    cVal1Par1.place(x=500, y=70, width=30)
    cVal1Par2 = tk.Entry(ventana,textvariable=micVal1Par2)
    cVal1Par2.place(x=540, y=70, width=30)
    cVal1Par3 = tk.Entry(ventana,textvariable=micVal1Par3)
    cVal1Par3.place(x=580, y=70, width=30)
    cVal1Par4 = tk.Entry(ventana,textvariable=micVal1Par4)
    cVal1Par4.place(x=620, y=70, width=30)

    cVal2Par1 = tk.Entry(ventana,textvariable=micVal2Par1)
    cVal2Par1.place(x=500, y=100, width=30)
    cVal2Par2 = tk.Entry(ventana,textvariable=micVal2Par2)
    cVal2Par2.place(x=540, y=100, width=30)
    cVal2Par3 = tk.Entry(ventana,textvariable=micVal2Par3)
    cVal2Par3.place(x=580, y=100, width=30)

    cVal3Par1 = tk.Entry(ventana,textvariable=micVal3Par1)
    cVal3Par1.place(x=500, y=130, width=30)
    cVal3Par2 = tk.Entry(ventana,textvariable=micVal3Par2)
    cVal3Par2.place(x=540, y=130, width=30)
    cVal3Par3 = tk.Entry(ventana,textvariable=micVal3Par3)
    cVal3Par3.place(x=580, y=130, width=30)
    cVal3Par4 = tk.Entry(ventana,textvariable=micVal3Par4)
    cVal3Par4.place(x=620, y=130, width=30)


    bBuscar = tk.Button(ventana, text="BUSCCAR",image=Buscar23, compound="left",bg=Colors.ColorSecundary,
                         font=font.Font(size=10,weight="bold"),activebackground=Colors.ColorSecundary)
    bBuscar.place(x=725, y=70,width=110,height=25)

    bModificar=tk.Button(ventana,text="MODIFICAR",image=Modificar23, compound="left",bg=Colors.ColorSecundary,
                         font=font.Font(size=10,weight="bold"),activebackground=Colors.ColorSecundary)
    bModificar.place(x=725,y=100,width=110,height=25)

    bLimpiar=tk.Button(ventana,text="BORRAR",image=Borrar23, compound="left",bg=Colors.ColorSecundary,
                         font=font.Font(size=10,weight="bold"),activebackground=Colors.ColorSecundary,command=limpiarVar)
    bLimpiar.place(x=725,y=130,width=110,height=25)


    lblPanelA = tk.Label(ventana, width=127, height=22, borderwidth=1, relief="sunken", bg="#FFFFFF")
    lblPanelA.place(x=10, y=250)

def limpiarVar():
    micVID.set("")
    micVNombre.set("")
    micVTipo.set("")
    micValor1.set("")
    micValor2.set("")
    micValor3.set("")
    micValor4.set("")
    micBValor1.set("")
    micBValor2.set("")
    micBValor3.set("")
    micVal1Par1.set("")
    micVal1Par2.set("")
    micVal1Par3.set("")
    micVal1Par4.set("")
    micVal2Par1.set("")
    micVal2Par2.set("")
    micVal2Par3.set("")
    micVal3Par1.set("")
    micVal3Par2.set("")
    micVal3Par3.set("")
    micVal3Par4.set("")


def MenuBar():
    BarraMenu=tk.Menu(ventana)
    ventana.config(menu=BarraMenu)

    sesionmenu = tk.Menu(BarraMenu, tearoff=0)
    sesionmenu.add_command(label="Cerrar Sesión")
    sesionmenu.add_separator()
    sesionmenu.add_command(label="Salir", command=ventana.quit)

    helpmenu = tk.Menu(BarraMenu, tearoff=0)
    helpmenu.add_command(label="Ayuda")
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...")

    variablemenu = tk.Menu(BarraMenu, tearoff=0)
    variablemenu.add_command(label="Variable de entrada")
    variablemenu.add_command(label="Variable de salida")

    reglamenu = tk.Menu(BarraMenu, tearoff=0)
    reglamenu.add_command(label="Visualizar")

    BarraMenu.add_cascade(label="Cuenta", menu=sesionmenu)
    BarraMenu.add_cascade(label="Variable", menu=variablemenu)
    BarraMenu.add_cascade(label="Reglas", menu=reglamenu)
    BarraMenu.add_cascade(label="Ayuda", menu=helpmenu)

def ingresar():
    close_loginScreen()
    varEntradas()
    grafEdad()
    bEdad.place(x=413, y=50, width=47)
    bIngreso.place(x=460, y=50, width=80)
    bCapPago.place(x=540, y=50, width=150)
    bTiempo.place(x=690, y=50, width=60)
    bHijos.place(x=750, y=50, width=50)
    bDeudas.place(x=800, y=50, width=85)
    bPrestamo.place(x=333, y=50, width=80)
    database.conexionBBDD()

#Rutas
RutaLogo="Imagenes\Logo.png"
RutaBackground="Imagenes\Background.png"
RutaSearch="Imagenes\Search.png"
RutaAgregar="Imagenes\Agregar.png"
RutaBorrar="Imagenes\img_borrar.png"
RutaBorrar23="Imagenes\img_borrar23.png"
RutaModificar23="Imagenes\img_modificar23.png"
RutaBuscar23="Imagenes\img_buscar23.png"
RutaUsuario="Imagenes\img_usuario.png"
RutaContraseña="Imagenes\img_contraseña.png"
RutaVerPass="Imagenes\img_ver_pass.png"
RutaNoVerPass="Imagenes\img_nover_pass.png"

Logo = PhotoImage(file=RutaLogo)
BG =PhotoImage(file=RutaBackground)
Search =PhotoImage(file=RutaSearch)
Agregar =PhotoImage(file=RutaAgregar)
Borrar =PhotoImage(file=RutaBorrar)
Borrar23 =PhotoImage(file=RutaBorrar23)
Modificar23 =PhotoImage(file=RutaModificar23)
Buscar23 =PhotoImage(file=RutaBuscar23)
Usuario =PhotoImage(file=RutaUsuario)
Contraseña =PhotoImage(file=RutaContraseña)
VerPass =PhotoImage(file=RutaVerPass)
NoVerPass =PhotoImage(file=RutaNoVerPass)

#Labels y Buttons
FontTitle = font.Font(family="helvetica", size=10, weight="bold")
Ari18 = font.Font(family='Arial', size=18)
Ari14 = font.Font(family='Arial', size=14)
comp = font.Font(family='helvetica', size=10, weight="bold")


login_screen()
##Menu
def varEntradas():
    lblFormCliente = tk.Label(ventana, text="DATOS DEL CLIENTE", font=FontTitle,bg=Colors.ColorWhite)
    lblFormCliente.place(x=40, y=50)

    lblID = tk.Label(ventana, text="ID: ", bg=Colors.ColorWhite)
    lblID.place(x=40, y=90)
    global micID,micDNI, milENombre, milEApellido,milEEMail,milECelular,milEFech_Nac,micEdad
    micID = tk.StringVar()
    micDNI = tk.StringVar()
    milENombre = tk.StringVar()
    milEApellido = tk.StringVar()
    milEEMail = tk.StringVar()
    milECelular = tk.StringVar()
    milEFech_Nac = tk.StringVar()
    micEdad = tk.StringVar()

    global cID, cDNI, lENombre, lEApellido,lEEMail,lECelular,lEFech_Nac
    cID = tk.Entry(ventana,textvariable=micID,state=tk.DISABLED)
    cID.place(x=150, y=90)

    lblDNI = tk.Label(ventana, text="DNI: ",bg=Colors.ColorWhite)
    lblDNI.place(x=40, y=120)
    cDNI= tk.Entry(ventana,textvariable=micDNI)
    cDNI.place(x=150, y=120)

    bComprobar = tk.Button(ventana,image=Search)
    bComprobar.configure(relief=tk.GROOVE, background=Colors.ColorWhite, activebackground=Colors.ColorSecundaryDark,command=buscarCliente)
    bComprobar.place(x=257, y=120, width=20, height=20)

    lblNombre = tk.Label(ventana,bg=Colors.ColorWhite, text="Nombres: ")
    lblNombre.place(x=40, y=150)
    lENombre = tk.Entry(ventana,textvariable=milENombre)
    lENombre.place(x=150, y=150)

    lblApellido = tk.Label(ventana,bg=Colors.ColorWhite, text="Apellidos: ")
    lblApellido.place(x=40, y=180)
    lEApellido = tk.Entry(ventana,textvariable=milEApellido)
    lEApellido.place(x=150, y=180)

    lblEmail = tk.Label(ventana, bg=Colors.ColorWhite,text="Correo: ")
    lblEmail.place(x=40, y=210)
    lEEMail = tk.Entry(ventana,textvariable=milEEMail)
    lEEMail.place(x=150, y=210)

    lblCelular = tk.Label(ventana,bg=Colors.ColorWhite, text="Celular: ")
    lblCelular.place(x=40, y=240)
    lECelular = tk.Entry(ventana,textvariable=milECelular)
    lECelular.place(x=150, y=240)

    lblFech_Nac = tk.Label(ventana, bg=Colors.ColorWhite, text="Fecha Nacimiento: ")
    lblFech_Nac.place(x=40, y=270)
    lEFech_Nac = tk.Entry(ventana,textvariable=milEFech_Nac)
    lEFech_Nac.place(x=150, y=270)

    bAgregar = tk.Button(ventana, text="AGREGAR", image=Agregar, compound="left", bg=Colors.ColorSecundary,
                         font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,command=crearCliente)
    bAgregar.place(x=40, y=305, height=30)

    bBorrar = tk.Button(ventana, text="BORRAR",image=Borrar, compound="left",bg=Colors.ColorSecundary,
                         font=font.Font(size=10,weight="bold"),activebackground=Colors.ColorSecundary,command=limpiarEntrys)
    bBorrar.place(x=180, y=305,height=30)

    Sep= ttk.Separator(ventana)
    Sep.place(x=40, y=340,relwidth=0.27)

    lblFormEval = tk.Label(ventana, text="EVALUAR PRÉSTAMO",bg=Colors.ColorWhite, font=FontTitle)
    lblFormEval.place(x=40, y=350)

    global cEdad, cIngreso, cCapPago, cTiempo, cHijos, cDeudas
    global lblEdad, lblIngreso, lblCapPago, lblTiempo, lblHijos, lblDeudas
    lblEdad = tk.Label(ventana, bg=Colors.ColorWhite,text="Edad: ")
    lblEdad.place(x=40, y=380)
    cEdad = tk.Entry(ventana,textvariable=micEdad)
    cEdad.place(x=150, y=380)

    lblIngreso = tk.Label(ventana, bg=Colors.ColorWhite,text="Ingreso: ")
    lblIngreso.place(x=40, y=410)
    cIngreso = tk.Entry(ventana)
    cIngreso.place(x=150, y=410)

    lblCapPago = tk.Label(ventana, bg=Colors.ColorWhite,text="Capacidad\nde pago: ")
    lblCapPago.place(x=40, y=440)
    cCapPago = tk.Entry(ventana)
    cCapPago.place(x=150, y=440)

    lblTiempo = tk.Label(ventana,bg=Colors.ColorWhite, text="Tiempo: ")
    lblTiempo.place(x=40, y=470)
    cTiempo = tk.Entry(ventana)
    cTiempo.place(x=150, y=470)

    lblHijos = tk.Label(ventana, bg=Colors.ColorWhite,text="Hijos: ")
    lblHijos.place(x=40, y=500)
    cHijos = tk.Entry(ventana)
    cHijos.place(x=150, y=500)

    lblDeudas = tk.Label(ventana, bg=Colors.ColorWhite,text="Endeudamientos: ")
    lblDeudas.place(x=40, y=530)
    cDeudas = tk.Entry(ventana)
    cDeudas.place(x=150, y=530)

    bEvaluar = tk.Button(ventana, bg=Colors.ColorSecundary, text="EVALUAR", font=comp, command=evaluar_prest)
    bEvaluar.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
    bEvaluar.place(x=120,y=550)
    panel_evaluacion()

def panel_evaluacion():

    panel = tk.Label(ventana, width=80, height=10, borderwidth=1, relief="sunken",bg="white")
    panel.place(x=333, y=415)

    lblTitle = tk.Label(ventana, text = "RESULTADOS DE EVALUACIÓN", bg="white",font = font.Font(family='helvetica', size=15, weight="bold"))
    lblTitle.place(x=335, y=420)

    lblPrestamo = tk.Label(ventana, text = "EL MONTO A PRESTAR ES DE: S/. ",bg="white")
    lblPrestamo.place(x=335,y=460)

    lblTipPr = tk.Label(ventana, text="TIPO DE PRESTAMO: ", bg="white")
    lblTipPr.place(x=335, y=490)

    global lblResp, lblcat
    lblResp= tk.Label(ventana, text="", bg="white")
    lblResp.place(x=515,y=460)

    lblcat = tk.Label(ventana, text="", bg="white")
    lblcat.place(x=450, y=490)

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
    if (bPrestamo['state'] == tk.NORMAL):
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

def evaluar_prest():
    global edad, ingreso, cap_pago, tiempo, hijos, deudas
    edad = cEdad.get()
    ingreso = cIngreso.get()
    cap_pago = cCapPago.get()
    tiempo = cTiempo.get()
    hijos = cHijos.get()
    deudas = cDeudas.get()
    fuzzi()

def fuzzi():
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

    if prestamo <= 7500:
        lblcat.configure(text="BAJO")
    elif prestamo >7500 and prestamo <= 30000:
        lblcat.configure(text="MEDIO")
    elif prestamo > 30000:
        lblcat.configure(text="ALTO")
    #Reduce el resultado a 2 decimales
    lblResp.configure(text=str(round(prestamo,2)))

ventana.mainloop()