import tkinter as tk
from tkinter import ttk, font, Label, PhotoImage, VERTICAL
import matplotlib.pyplot as plt
from skfuzzy.control.visualization import ControlSystemVisualizer

from Values import Colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import skfuzzy as fuzz
import database
from tkinter import messagebox
from skfuzzy import control as ctrl
import sqlite3
import sys

ventana = tk.Tk()
ventana.title("UDELLA - EVALUADOR DE PRÉSTAMO")
ventana.iconbitmap("Imagenes\icono2.ico")
ventana.geometry("920x600")
ventana.resizable(False, False)
ventana.configure(bg=Colors.ColorWhite)


def login_screen():
    global lblImage1, lblFondo, lblPanel, cUsuario, cContraseña, lblUsuario, img_Usuario, lblContraseña
    global img_verPass, img_NoverPass, lblRecuperar, img_Contraseña
    lblFondo = Label(ventana, image=BG)
    lblFondo.place(x=0, y=0)
    lblImage1 = Label(ventana, image=Logo, bg=Colors.ColorPrimary)
    lblImage1.place(x=381.91, y=20)
    lblPanel = tk.Label(ventana, width=35, height=15, borderwidth=1, relief="sunken", bg=Colors.ColorPrimary)
    lblPanel.place(x=360, y=220)

    lblUsuario = tk.Label(ventana, text="Usuario:", bg=Colors.ColorPrimary, fg=Colors.ColorWhite,
                          font=font.Font(size=12, weight="bold"))
    lblUsuario.place(x=370, y=230)
    img_Usuario = tk.Label(ventana, image=Usuario, bg=Colors.ColorPrimary)
    img_Usuario.place(x=370, y=260)
    cUsuario = tk.Entry(ventana)
    cUsuario.place(x=410, y=260, width=160, height=25)

    lblContraseña = tk.Label(ventana, text="Contraseña:", bg=Colors.ColorPrimary, fg=Colors.ColorWhite,
                             font=font.Font(size=12, weight="bold"))
    lblContraseña.place(x=370, y=300)
    img_Contraseña = tk.Label(ventana, image=Contraseña, bg=Colors.ColorPrimary)
    img_Contraseña.place(x=370, y=330)
    cContraseña = tk.Entry(ventana, show="*")
    cContraseña.place(x=410, y=330, width=160, height=25)

    img_verPass = tk.Button(ventana, image=VerPass, bg=Colors.ColorPrimary, state=tk.NORMAL, command=switchpass,
                            relief="flat")
    img_verPass.configure(activebackground=Colors.ColorPrimary)

    img_NoverPass = tk.Button(ventana, image=NoVerPass, bg=Colors.ColorPrimary, state=tk.NORMAL, command=switchNopass,
                              relief="flat")
    img_NoverPass.configure(activebackground=Colors.ColorPrimary)
    img_NoverPass.place(x=575, y=330, height=25)

    lblRecuperar = tk.Button(ventana, text="¿Olvidaste la contraseña?", bg=Colors.ColorPrimary, fg=Colors.ColorWhite,
                             font=font.Font(size=8, weight="bold"), relief="flat")
    lblRecuperar.configure(activebackground=Colors.ColorPrimary, activeforeground=Colors.ColorWhite)
    lblRecuperar.place(x=427, y=360)

    global BIniciar
    BIniciar = tk.Button(ventana, bg=Colors.ColorSecundary, text="INGRESAR", font=Ari14, command=login)
    BIniciar.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
    BIniciar.place(x=420, y=400, width=120, height=30)


def login():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    User = cUsuario.get()
    Pass = cContraseña.get()
    miCursor.execute("SELECT * FROM EMPLEADOS WHERE Usuario=? AND Contraseña=?", (User, Pass))
    DatosEmpleado = miCursor.fetchall()

    for Empleado in DatosEmpleado:
        Rol = Empleado[3]

    if DatosEmpleado:
        if Rol == "ASESOR":
            messagebox.showinfo("LOGIN CORRECTO", "ROL ASESOR")
            ingresar()
        elif Rol == "ADMINISTRADOR":
            messagebox.showinfo("LOGIN CORRECTO", "ROL ADMIN")
            ingresar_admin()
    else:
        messagebox.showerror("LOGIN INCORRECTO", "Usuario y/o Contraseña no valido")


def switchpass():
    if (img_verPass['state'] == tk.NORMAL):
        img_verPass.place_forget()
        img_NoverPass.place(x=575, y=330, height=25)
        cContraseña['show'] = "*"

def switchNopass():
    if (img_NoverPass['state'] == tk.NORMAL):
        cContraseña['show'] = ""
        img_NoverPass.place_forget()
        img_verPass.place(x=575, y=330, height=25)

def crearCliente():
    try:
        miConexion = sqlite3.connect("BDPrestamoPersonal")

        miCursor = miConexion.cursor()

        miCursor.execute("INSERT INTO CLIENTES VALUES(NULL, '" + cDNI.get() +
                         "','" + lENombre.get() +
                         "','" + lEApellido.get() +
                         "','" + lEEMail.get() +
                         "','" + lECelular.get() +
                         "','" + lEFech_Nac.get() +
                         "',NULL,NULL)")

        miConexion.commit()

        messagebox.showinfo("BBDD", "Registro insertado con éxito")
    except:
        messagebox.showwarning("¡Advertencia!", "El usuario ya existe")


def buscarCliente():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("SELECT * FROM CLIENTES WHERE DNI=" + cDNI.get())
    DatosCliente = miCursor.fetchall()

    for cliente in DatosCliente:
        micID.set(cliente[0])
        milENombre.set(cliente[2])
        milEApellido.set(cliente[3])
        milEEMail.set(cliente[4])
        milECelular.set(cliente[5])
        milEFech_Nac.set(cliente[6])
    miConexion.commit()

    calcular_edad()


def buscarVar():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("""SELECT VARIABLES.ID_Variable,VARIABLES.Nombre,VARIABLES.Tipo,VALORES_LINGUISTICOS.Nombre,
        VALORES_LINGUISTICOS.Func_Pertenencia, VALORES_LINGUISTICOS.Parametro1, VALORES_LINGUISTICOS.Parametro2,
        VALORES_LINGUISTICOS.Parametro3, VALORES_LINGUISTICOS.Parametro4 FROM VALORES_LINGUISTICOS
        JOIN VARIABLES ON VARIABLES.ID_Variable = VALORES_LINGUISTICOS.ID_Variable
        WHERE VARIABLES.ID_Variable= """ + cVID.get())

    DatosVar = miCursor.fetchall()

    tup1, tup2, tup3 = DatosVar

    micVNombre.set(tup1[1])
    micVTipo.set(tup1[2])
    micValor1.set(tup1[3])
    micBValor1.set(tup1[4])
    micVal1Par1.set(tup1[5])
    micVal1Par2.set(tup1[6])
    micVal1Par3.set(tup1[7])
    micVal1Par4.set(tup1[8])

    micValor2.set(tup2[3])
    micBValor2.set(tup2[4])
    micVal2Par1.set(tup2[5])
    micVal2Par2.set(tup2[6])
    micVal2Par3.set(tup2[7])
    micVal2Par4.set(tup2[8])

    micValor3.set(tup3[3])
    micBValor3.set(tup3[4])
    micVal3Par1.set(tup3[5])
    micVal3Par2.set(tup3[6])
    micVal3Par3.set(tup3[7])
    micVal3Par4.set(tup3[8])

    miConexion.commit()

def mostrar_variables():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("""SELECT VALORES_LINGUISTICOS.Nombre,VARIABLES.Nombre,VALORES_LINGUISTICOS.Parametro1, VALORES_LINGUISTICOS.Parametro2,
            VALORES_LINGUISTICOS.Parametro3, VALORES_LINGUISTICOS.Parametro4 FROM VALORES_LINGUISTICOS
            JOIN VARIABLES ON VARIABLES.ID_Variable = VALORES_LINGUISTICOS.ID_Variable""")

    datos=miCursor.fetchall()
    var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17,var18 =datos
    global NVariable1,NVariable2,NVariable3,NVariable4,NVariable5,NVariable6
    NVariable1=var1[1]
    NVariable2=var4[1]
    NVariable3=var7[1]
    NVariable4=var10[1]
    NVariable5=var13[1]
    NVariable6=var16[1]

    global var1val1,var1val2,var1val3
    var1val1 = var1[0]
    var1val2 = var2[0]
    var1val3 = var3[0]

    global var2val1, var2val2, var2val3
    var2val1 = var4[0]
    var2val2 = var5[0]
    var2val3 = var6[0]
    global var3val1, var3val2, var3val3
    var3val1 = var7[0]
    var3val2 = var8[0]
    var3val3 = var9[0]
    global var4val1, var4val2, var4val3
    var4val1 = var10[0]
    var4val2 = var11[0]
    var4val3 = var12[0]
    global var5val1, var5val2, var5val3
    var5val1 = var13[0]
    var5val2 = var14[0]
    var5val3 = var15[0]
    global var6val1, var6val2, var6val3
    var6val1 = var16[0]
    var6val2 = var17[0]
    var6val3 = var18[0]


    #OBTENCION DE PARAMETROS
    # Variable 1 - Valor Linguistico 1
    global v1val1Par1,v1val1Par2,v1val1Par3,v1val1Par4
    v1val1Par1=var1[2]
    v1val1Par2=var1[3]
    v1val1Par3=var1[4]
    v1val1Par4=var1[5]
    # Variable 1 - Valor Linguistico 2
    global v1val2Par1,v1val2Par2,v1val2Par3,v1val2Par4
    v1val2Par1 = var2[2]
    v1val2Par2 = var2[3]
    v1val2Par3 = var2[4]
    v1val2Par4 = var2[5]
    # Variable 1 - Valor Linguistico 3
    global v1val3Par1,v1val3Par2,v1val3Par3,v1val3Par4
    v1val3Par1 = var3[2]
    v1val3Par2 = var3[3]
    v1val3Par3 = var3[4]
    v1val3Par4 = var3[5]
    # Variable 2 - Valor Linguistico 1
    global v2val1Par1, v2val1Par2, v2val1Par3, v2val1Par4
    v2val1Par1 = var4[2]
    v2val1Par2 = var4[3]
    v2val1Par3 = var4[4]
    v2val1Par4 = var4[5]
    # Variable 2 - Valor Linguistico 2
    global v2val2Par1, v2val2Par2, v2val2Par3, v2val2Par4
    v2val2Par1 = var5[2]
    v2val2Par2 = var5[3]
    v2val2Par3 = var5[4]
    v2val2Par4 = var5[5]
    # Variable 2 - Valor Linguistico 3
    global v2val3Par1, v2val3Par2, v2val3Par3, v2val3Par4
    v2val3Par1 = var6[2]
    v2val3Par2 = var6[3]
    v2val3Par3 = var6[4]
    v2val3Par4 = var6[5]
    # Variable 3 - Valor Linguistico 1
    global v3val1Par1, v3val1Par2, v3val1Par3, v3val1Par4
    v3val1Par1 = var7[2]
    v3val1Par2 = var7[3]
    v3val1Par3 = var7[4]
    v3val1Par4 = var7[5]
    # Variable 3 - Valor Linguistico 2
    global v3val2Par1, v3val2Par2, v3val2Par3, v3val2Par4
    v3val2Par1 = var8[2]
    v3val2Par2 = var8[3]
    v3val2Par3 = var8[4]
    v3val2Par4 = var8[5]
    # Variable 3 - Valor Linguistico 3
    global v3val3Par1, v3val3Par2, v3val3Par3, v3val3Par4
    v3val3Par1 = var9[2]
    v3val3Par2 = var9[3]
    v3val3Par3 = var9[4]
    v3val3Par4 = var9[5]
    # Variable 4 - Valor Linguistico 1
    global v4val1Par1, v4val1Par2, v4val1Par3, v4val1Par4
    v4val1Par1 = var10[2]
    v4val1Par2 = var10[3]
    v4val1Par3 = var10[4]
    v4val1Par4 = var10[5]
    # Variable 4 - Valor Linguistico 2
    global v4val2Par1, v4val2Par2, v4val2Par3, v4val2Par4
    v4val2Par1 = var11[2]
    v4val2Par2 = var11[3]
    v4val2Par3 = var11[4]
    v4val2Par4 = var11[5]
    # Variable 4 - Valor Linguistico 3
    global v4val3Par1, v4val3Par2, v4val3Par3, v4val3Par4
    v4val3Par1 = var12[2]
    v4val3Par2 = var12[3]
    v4val3Par3 = var12[4]
    v4val3Par4 = var12[5]
    # Variable 5 - Valor Linguistico 1
    global v5val1Par1, v5val1Par2, v5val1Par3, v5val1Par4
    v5val1Par1 = var13[2]
    v5val1Par2 = var13[3]
    v5val1Par3 = var13[4]
    v5val1Par4 = var13[5]
    # Variable 5 - Valor Linguistico 2
    global v5val2Par1, v5val2Par2, v5val2Par3, v5val2Par4
    v5val2Par1 = var14[2]
    v5val2Par2 = var14[3]
    v5val2Par3 = var14[4]
    v5val2Par4 = var14[5]
    # Variable 5 - Valor Linguistico 3
    global v5val3Par1, v5val3Par2, v5val3Par3, v5val3Par4
    v5val3Par1 = var15[2]
    v5val3Par2 = var15[3]
    v5val3Par3 = var15[4]
    v5val3Par4 = var15[5]
    # Variable 6 - Valor Linguistico 1
    global v6val1Par1, v6val1Par2, v6val1Par3, v6val1Par4
    v6val1Par1 = var16[2]
    v6val1Par2 = var16[3]
    v6val1Par3 = var16[4]
    v6val1Par4 = var16[5]
    # Variable 6 - Valor Linguistico 2
    global v6val2Par1, v6val2Par2, v6val2Par3, v6val2Par4
    v6val2Par1 = var17[2]
    v6val2Par2 = var17[3]
    v6val2Par3 = var17[4]
    v6val2Par4 = var17[5]
    # Variable 6 - Valor Linguistico 3
    global v6val3Par1, v6val3Par2, v6val3Par3, v6val3Par4
    v6val3Par1 = var18[2]
    v6val3Par2 = var18[3]
    v6val3Par3 = var18[4]
    v6val3Par4 = var18[5]

mostrar_variables()

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

    miCursor.execute(
        "SELECT (strftime('%Y', 'now') - strftime('%Y', Fech_Nac )) - (strftime('%m-%d', 'now') < strftime('%m-%d', Fech_Nac )) from CLIENTES WHERE DNI=" + cDNI.get())
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

#FALTA PROGRAMAR
def cerrar_sesion():
    cVID.place_forget()
    cVNombre.place_forget()
    cVTipo.place_forget()
    cValor1.place_forget()
    cValor2.place_forget()
    cValor3.place_forget()
    cBValor1.place_forget()
    cBValor2.place_forget()
    cBValor3.place_forget()
    cVal1Par1.place_forget()
    cVal1Par2.place_forget()
    cVal1Par3.place_forget()
    cVal1Par4.place_forget()
    cVal2Par1.place_forget()
    cVal2Par2.place_forget()
    cVal2Par3.place_forget()
    cVal2Par4.place_forget()
    cVal3Par1.place_forget()
    cVal3Par2.place_forget()
    cVal3Par3.place_forget()
    cVal3Par4.place_forget()
    bBuscar.place_forget()
    bModificar.place_forget()
    bLimpiar.place_forget()
    bGuardar.place_forget()
    bActualizar.place_forget()
    table.place_forget()


def ingresar_admin():
    close_loginScreen()
    MenuBar()

def variables_screen():
    global cVID, cVNombre, cVTipo, cValor1, cValor2, cValor3, cBValor1, cBValor2, cBValor3, \
        cVal1Par1, cVal1Par2, cVal1Par3, cVal1Par4, cVal2Par1, cVal2Par2, cVal2Par3, cVal2Par4, cVal3Par1, cVal3Par2, cVal3Par3, cVal3Par4

    global micVID, micVNombre, micVTipo, micValor1, micValor2, micValor3, micValor4, micBValor1, micBValor2, micBValor3, \
        micVal1Par1, micVal1Par2, micVal1Par3, micVal1Par4, micVal2Par1, micVal2Par2, micVal2Par3, micVal2Par4, micVal3Par1, \
        micVal3Par2, micVal3Par3, micVal3Par4

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
    micVal2Par4 = tk.StringVar()
    micVal3Par1 = tk.StringVar()
    micVal3Par2 = tk.StringVar()
    micVal3Par3 = tk.StringVar()
    micVal3Par4 = tk.StringVar()

    global lblVariable, lblID, lblNombre, lblTipo, lblValorL, lblFunPer, lblPar
    lblVariable = tk.Label(ventana, text="VARIABLES", font=font.Font(size=15, weight="bold"), bg="#FFFFFF")
    lblVariable.place(x=80, y=15)

    lblID = tk.Label(ventana, text="ID:", bg=Colors.ColorWhite)
    lblID.place(x=80, y=70)
    cVID = tk.Entry(ventana, textvariable=micVID, state=tk.NORMAL)
    cVID.place(x=155, y=70)
    lblNombre = tk.Label(ventana, text="Nombre:", bg=Colors.ColorWhite)
    lblNombre.place(x=80, y=100)
    cVNombre = tk.Entry(ventana, textvariable=micVNombre, state=tk.DISABLED)
    cVNombre.place(x=155, y=100)
    lblTipo = tk.Label(ventana, text="Tipo:", bg=Colors.ColorWhite)
    lblTipo.place(x=80, y=130)
    cVTipo = tk.Entry(ventana, textvariable=micVTipo, state=tk.DISABLED)
    cVTipo.place(x=155, y=130)

    lblValorL = tk.Label(ventana, text="Valor \nLinguistico", font=font.Font(size=10, weight="bold"), bg="#FFFFFF")
    lblValorL.place(x=325, y=28)

    lblFunPer = tk.Label(ventana, text="Función de \nPertenencia", font=font.Font(size=10, weight="bold"), bg="#FFFFFF")
    lblFunPer.place(x=447, y=28)

    lblPar = tk.Label(ventana, text="Parámetros", font=font.Font(size=10, weight="bold"), bg="#FFFFFF")
    lblPar.place(x=600, y=34)

    cValor1 = tk.Entry(ventana, textvariable=micValor1, state=tk.DISABLED)
    cValor1.place(x=325, y=70, width=75)
    cValor2 = tk.Entry(ventana, textvariable=micValor2, state=tk.DISABLED)
    cValor2.place(x=325, y=100, width=75)
    cValor3 = tk.Entry(ventana, textvariable=micValor3, state=tk.DISABLED)
    cValor3.place(x=325, y=130, width=75)

    cBValor1 = ttk.Combobox(state=tk.DISABLED, textvariable=micBValor1)
    cBValor1["values"] = ["TRIANGULAR", "TRAPEZOIDAL"]
    cBValor1.place(x=445, y=70, width=100)

    # readonly
    cBValor2 = ttk.Combobox(state=tk.DISABLED, textvariable=micBValor2)
    cBValor2["values"] = ["TRIANGULAR", "TRAPEZOIDAL"]
    cBValor2.place(x=445, y=100, width=100)

    cBValor3 = ttk.Combobox(state=tk.DISABLED, textvariable=micBValor3)
    cBValor3["values"] = ["TRIANGULAR", "TRAPEZOIDAL"]
    cBValor3.place(x=445, y=130, width=100)

    cVal1Par1 = tk.Entry(ventana, textvariable=micVal1Par1, state=tk.DISABLED)
    cVal1Par1.place(x=600, y=70, width=50)
    cVal1Par2 = tk.Entry(ventana, textvariable=micVal1Par2, state=tk.DISABLED)
    cVal1Par2.place(x=660, y=70, width=50)
    cVal1Par3 = tk.Entry(ventana, textvariable=micVal1Par3, state=tk.DISABLED)
    cVal1Par3.place(x=720, y=70, width=50)
    cVal1Par4 = tk.Entry(ventana, textvariable=micVal1Par4, state=tk.DISABLED)
    cVal1Par4.place(x=780, y=70, width=50)

    cVal2Par1 = tk.Entry(ventana, textvariable=micVal2Par1, state=tk.DISABLED)
    cVal2Par1.place(x=600, y=100, width=50)
    cVal2Par2 = tk.Entry(ventana, textvariable=micVal2Par2, state=tk.DISABLED)
    cVal2Par2.place(x=660, y=100, width=50)
    cVal2Par3 = tk.Entry(ventana, textvariable=micVal2Par3, state=tk.DISABLED)
    cVal2Par3.place(x=720, y=100, width=50)
    cVal2Par4 = tk.Entry(ventana, textvariable=micVal2Par4, state=tk.DISABLED)
    cVal2Par4.place(x=780, y=100, width=50)

    cVal3Par1 = tk.Entry(ventana, textvariable=micVal3Par1, state=tk.DISABLED)
    cVal3Par1.place(x=600, y=130, width=50)
    cVal3Par2 = tk.Entry(ventana, textvariable=micVal3Par2, state=tk.DISABLED)
    cVal3Par2.place(x=660, y=130, width=50)
    cVal3Par3 = tk.Entry(ventana, textvariable=micVal3Par3, state=tk.DISABLED)
    cVal3Par3.place(x=720, y=130, width=50)
    cVal3Par4 = tk.Entry(ventana, textvariable=micVal3Par4, state=tk.DISABLED)
    cVal3Par4.place(x=780, y=130, width=50)

    global bBuscar, bModificar, bLimpiar, bGuardar,bActualizar
    bBuscar = tk.Button(ventana, text="BUSCAR", image=Buscar23, compound="left", bg=Colors.ColorSecundary,
                        font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                        command=buscarVar)
    bBuscar.place(x=80, y=190, width=110, height=25)

    bModificar = tk.Button(ventana, text="MODIFICAR", image=Modificar23, compound="left", bg=Colors.ColorSecundary,
                           font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                           command=modificarVar)
    bModificar.place(x=237.5, y=190, width=110, height=25)

    bLimpiar = tk.Button(ventana, text="LIMPIAR", image=Borrar23, compound="left", bg=Colors.ColorSecundary,
                         font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                         command=limpiarVar)
    bLimpiar.place(x=395, y=190, width=110, height=25)

    bGuardar = tk.Button(ventana, text="GUARDAR", image=Guardar23, compound="left", bg=Colors.ColorSecundary,
                         font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                         command=guardarVar)
    bGuardar.place(x=552.5, y=190, width=110, height=25)

    bActualizar = tk.Button(ventana, text="ACTUALIZAR", image=Actualizar23, compound="left", bg=Colors.ColorSecundary,
                            font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                            command=verDataTable)
    bActualizar.place(x=710, y=190, width=120, height=25)

    global table
    table = ttk.Treeview(column=(
    "ID", "Variable", "Tipo", "Valor", "Función de Pertenencia", "Parametro1", "Parametro2", "Parametro3",
    "Parametro4",), show='headings')
    table.heading("ID", text="ID")
    table.heading("Variable", text="Variable")
    table.heading("Tipo", text="Tipo")
    table.heading("Valor", text="Valor")
    table.heading("Función de Pertenencia", text="Función de Pertenencia")
    table.heading("Parametro1", text="Parametro1")
    table.heading("Parametro2", text="Parametro2")
    table.heading("Parametro3", text="Parametro3")
    table.heading("Parametro4", text="Parametro4")
    table.place(x=10, y=250, width=900, height=330)

def verDataTable():
    table.delete(*table.get_children())
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()
    miCursor.execute("""SELECT VARIABLES.ID_Variable,VARIABLES.Nombre,VARIABLES.Tipo,VALORES_LINGUISTICOS.Nombre,
    VALORES_LINGUISTICOS.Func_Pertenencia, VALORES_LINGUISTICOS.Parametro1, VALORES_LINGUISTICOS.Parametro2,
    VALORES_LINGUISTICOS.Parametro3, VALORES_LINGUISTICOS.Parametro4 FROM VALORES_LINGUISTICOS
    JOIN VARIABLES ON VARIABLES.ID_Variable = VALORES_LINGUISTICOS.ID_Variable""")
    for row in miCursor:
        disp = (
            '{0} {1} {2} {3} {4} {5} {6} {7} {8}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                         row[8]))
        table.insert("", tk.END, values=disp)


def dataVarPar():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("""SELECT VARIABLES.ID_Variable, VALORES_LINGUISTICOS.ID_Valor FROM VALORES_LINGUISTICOS
            JOIN VARIABLES ON VARIABLES.ID_Variable = VALORES_LINGUISTICOS.ID_Variable
            WHERE VARIABLES.ID_Variable= """ + cVID.get())

    Datos = miCursor.fetchall()
    print(Datos)
    IDVar1, IDVar2, IDVar3 = Datos

    global IDValLin1, IDValLin2, IDValLin3
    IDValLin1 = IDVar1[1]
    IDValLin2 = IDVar2[1]
    IDValLin3 = IDVar3[1]

    miConexion.commit()


def guardarVar():
    dataVarPar()

    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("UPDATE VARIABLES SET Nombre='" + cVNombre.get() +
                     "',Tipo='" + cVTipo.get() +
                     "'WHERE ID_Variable=" + cVID.get())

    miCursor.execute("UPDATE VALORES_LINGUISTICOS SET Nombre='" + cValor1.get() +
                     "',Func_Pertenencia='" + cBValor1.get() +
                     "',Parametro1='" + cVal1Par1.get() +
                     "',Parametro2='" + cVal1Par2.get() +
                     "',Parametro3='" + cVal1Par3.get() +
                     "',Parametro4='" + cVal1Par4.get() +
                     "'WHERE ID_Valor='" + str(IDValLin1) + "' AND ID_Variable=" + cVID.get())
    miCursor.execute("UPDATE VALORES_LINGUISTICOS SET Nombre='" + cValor2.get() +
                     "',Func_Pertenencia='" + cBValor2.get() +
                     "',Parametro1='" + cVal2Par1.get() +
                     "',Parametro2='" + cVal2Par2.get() +
                     "',Parametro3='" + cVal2Par3.get() +
                     "',Parametro4='" + cVal2Par4.get() +
                     "'WHERE ID_Valor='" + str(IDValLin2) + "' AND ID_Variable=" + cVID.get())
    miCursor.execute("UPDATE VALORES_LINGUISTICOS SET Nombre='" + cValor3.get() +
                     "',Func_Pertenencia='" + cBValor3.get() +
                     "',Parametro1='" + cVal3Par1.get() +
                     "',Parametro2='" + cVal3Par2.get() +
                     "',Parametro3='" + cVal3Par3.get() +
                     "',Parametro4='" + cVal3Par4.get() +
                     "'WHERE ID_Valor='" + str(IDValLin3) + "' AND ID_Variable=" + cVID.get())
    messagebox.showinfo("DB", "LOS DATOS SE GUARDARON CORRECTAMENTE")
    miConexion.commit()
    bloqVar()


def modificarVar():
    cVNombre['state'] = tk.NORMAL
    cVTipo['state'] = tk.NORMAL
    cValor1['state'] = tk.NORMAL
    cValor2['state'] = tk.NORMAL
    cValor3['state'] = tk.NORMAL

    cBValor1['state'] = "readonly"
    cBValor2['state'] = "readonly"
    cBValor3['state'] = "readonly"

    cVal1Par1['state'] = tk.NORMAL
    cVal1Par2['state'] = tk.NORMAL
    cVal1Par3['state'] = tk.NORMAL
    cVal1Par4['state'] = tk.NORMAL

    cVal2Par1['state'] = tk.NORMAL
    cVal2Par2['state'] = tk.NORMAL
    cVal2Par3['state'] = tk.NORMAL
    cVal2Par4['state'] = tk.NORMAL

    cVal3Par1['state'] = tk.NORMAL
    cVal3Par2['state'] = tk.NORMAL
    cVal3Par3['state'] = tk.NORMAL
    cVal3Par4['state'] = tk.NORMAL


def bloqVar():
    cVNombre['state'] = tk.DISABLED
    cVTipo['state'] = tk.DISABLED
    cValor1['state'] = tk.DISABLED
    cValor2['state'] = tk.DISABLED
    cValor3['state'] = tk.DISABLED

    cBValor1['state'] = tk.DISABLED
    cBValor2['state'] = tk.DISABLED
    cBValor3['state'] = tk.DISABLED

    cVal1Par1['state'] = tk.DISABLED
    cVal1Par2['state'] = tk.DISABLED
    cVal1Par3['state'] = tk.DISABLED
    cVal1Par4['state'] = tk.DISABLED

    cVal2Par1['state'] = tk.DISABLED
    cVal2Par2['state'] = tk.DISABLED
    cVal2Par3['state'] = tk.DISABLED
    cVal2Par4['state'] = tk.DISABLED

    cVal3Par1['state'] = tk.DISABLED
    cVal3Par2['state'] = tk.DISABLED
    cVal3Par3['state'] = tk.DISABLED
    cVal3Par4['state'] = tk.DISABLED


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
    micVal2Par4.set("")


def MenuBar():
    BarraMenu = tk.Menu(ventana)
    ventana.config(menu=BarraMenu)

    sesionmenu = tk.Menu(BarraMenu, tearoff=0)
    sesionmenu.add_command(label="Cerrar Sesión",command=cerrar_sesion)
    sesionmenu.add_separator()
    sesionmenu.add_command(label="Salir", command=ventana.quit)

    helpmenu = tk.Menu(BarraMenu, tearoff=0)
    helpmenu.add_command(label="Ayuda")
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...")

    variablemenu = tk.Menu(BarraMenu, tearoff=0)
    variablemenu.add_command(label="Configuracion", command=abVar_crReg)

    reglamenu = tk.Menu(BarraMenu, tearoff=0)
    reglamenu.add_command(label="Configuracion",command=abReg_crVar)

    BarraMenu.add_cascade(label="Cuenta", menu=sesionmenu)
    BarraMenu.add_cascade(label="Variable", menu=variablemenu)
    BarraMenu.add_cascade(label="Reglas", menu=reglamenu)
    BarraMenu.add_cascade(label="Personal", menu=helpmenu)
    BarraMenu.add_cascade(label="Ayuda", menu=helpmenu)


def ingresar():
    close_loginScreen()
    varEntradas()
    grafVar1()
    bVariable1.place(x=413, y=50, width=80)
    bVariable3.place(x=493, y=50, width=47)
    bVariable2.place(x=540, y=50, width=150)
    bVariable4.place(x=690, y=50, width=60)
    bVariable5.place(x=750, y=50, width=50)
    bVariable6.place(x=800, y=50, width=85)
    bPrestamo.place(x=333, y=50, width=80)
    database.conexionBBDD()


# Rutas
RutaLogo = "Imagenes\Logo.png"
RutaBackground = "Imagenes\Background.png"
RutaSearch = "Imagenes\Search.png"
RutaAgregar = "Imagenes\Agregar.png"
RutaBorrar = "Imagenes\img_borrar.png"
RutaBorrar23 = "Imagenes\img_borrar23.png"
RutaModificar23 = "Imagenes\img_modificar23.png"
RutaBuscar23 = "Imagenes\img_buscar23.png"
RutaGuardar23 = "Imagenes\img_guardar23.png"
RutaActualizar23 = "Imagenes\img_actualizar23.png"
RutaUsuario = "Imagenes\img_usuario.png"
RutaContraseña = "Imagenes\img_contraseña.png"
RutaVerPass = "Imagenes\img_ver_pass.png"
RutaNoVerPass = "Imagenes\img_nover_pass.png"

Logo = PhotoImage(file=RutaLogo)
BG = PhotoImage(file=RutaBackground)
Search = PhotoImage(file=RutaSearch)
Agregar = PhotoImage(file=RutaAgregar)
Borrar = PhotoImage(file=RutaBorrar)
Borrar23 = PhotoImage(file=RutaBorrar23)
Modificar23 = PhotoImage(file=RutaModificar23)
Buscar23 = PhotoImage(file=RutaBuscar23)
Guardar23 = PhotoImage(file=RutaGuardar23)
Actualizar23 = PhotoImage(file=RutaActualizar23)
Usuario = PhotoImage(file=RutaUsuario)
Contraseña = PhotoImage(file=RutaContraseña)
VerPass = PhotoImage(file=RutaVerPass)
NoVerPass = PhotoImage(file=RutaNoVerPass)

# Labels y Buttons
FontTitle = font.Font(family="helvetica", size=10, weight="bold")
Ari18 = font.Font(family='Arial', size=18)
Ari14 = font.Font(family='Arial', size=14)
comp = font.Font(family='helvetica', size=10, weight="bold")

login_screen()


##Menu
def varEntradas():
    lblFormCliente = tk.Label(ventana, text="DATOS DEL CLIENTE", font=FontTitle, bg=Colors.ColorWhite)
    lblFormCliente.place(x=40, y=50)

    lblID = tk.Label(ventana, text="ID: ", bg=Colors.ColorWhite)
    lblID.place(x=40, y=90)
    global micID, micDNI, milENombre, milEApellido, milEEMail, milECelular, milEFech_Nac, micEdad
    micID = tk.StringVar()
    micDNI = tk.StringVar()
    milENombre = tk.StringVar()
    milEApellido = tk.StringVar()
    milEEMail = tk.StringVar()
    milECelular = tk.StringVar()
    milEFech_Nac = tk.StringVar()
    micEdad = tk.StringVar()

    global cID, cDNI, lENombre, lEApellido, lEEMail, lECelular, lEFech_Nac
    cID = tk.Entry(ventana, textvariable=micID, state=tk.DISABLED)
    cID.place(x=150, y=90)

    lblDNI = tk.Label(ventana, text="DNI: ", bg=Colors.ColorWhite)
    lblDNI.place(x=40, y=120)
    cDNI = tk.Entry(ventana, textvariable=micDNI)
    cDNI.place(x=150, y=120)

    bComprobar = tk.Button(ventana, image=Search)
    bComprobar.configure(relief=tk.GROOVE, background=Colors.ColorWhite, activebackground=Colors.ColorSecundaryDark,
                         command=buscarCliente)
    bComprobar.place(x=257, y=120, width=20, height=20)

    lblNombre = tk.Label(ventana, bg=Colors.ColorWhite, text="Nombres: ")
    lblNombre.place(x=40, y=150)
    lENombre = tk.Entry(ventana, textvariable=milENombre)
    lENombre.place(x=150, y=150)

    lblApellido = tk.Label(ventana, bg=Colors.ColorWhite, text="Apellidos: ")
    lblApellido.place(x=40, y=180)
    lEApellido = tk.Entry(ventana, textvariable=milEApellido)
    lEApellido.place(x=150, y=180)

    lblEmail = tk.Label(ventana, bg=Colors.ColorWhite, text="Correo: ")
    lblEmail.place(x=40, y=210)
    lEEMail = tk.Entry(ventana, textvariable=milEEMail)
    lEEMail.place(x=150, y=210)

    lblCelular = tk.Label(ventana, bg=Colors.ColorWhite, text="Celular: ")
    lblCelular.place(x=40, y=240)
    lECelular = tk.Entry(ventana, textvariable=milECelular)
    lECelular.place(x=150, y=240)

    lblFech_Nac = tk.Label(ventana, bg=Colors.ColorWhite, text="Fecha Nacimiento: ")
    lblFech_Nac.place(x=40, y=270)
    lEFech_Nac = tk.Entry(ventana, textvariable=milEFech_Nac)
    lEFech_Nac.place(x=150, y=270)

    bAgregar = tk.Button(ventana, text="AGREGAR", image=Agregar, compound="left", bg=Colors.ColorSecundary,
                         font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                         command=crearCliente)
    bAgregar.place(x=40, y=305, height=30)

    bBorrar = tk.Button(ventana, text="LIMPIAR", image=Borrar, compound="left", bg=Colors.ColorSecundary,
                        font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                        command=limpiarEntrys)
    bBorrar.place(x=180, y=305, height=30)

    Sep = ttk.Separator(ventana)
    Sep.place(x=40, y=340, relwidth=0.27)

    lblFormEval = tk.Label(ventana, text="EVALUAR PRÉSTAMO", bg=Colors.ColorWhite, font=FontTitle)
    lblFormEval.place(x=40, y=350)

    global cVar1, cVar2,cVar3, cVar4, cVar5, cVar6
    global lblVar1,lblVar2, lblVar3, lblVar4,lblVar5,lblVar6
    lblVar1 = tk.Label(ventana, bg=Colors.ColorWhite, text=NVariable1+": ")
    lblVar1.place(x=40, y=380)
    cVar1 = tk.Entry(ventana)
    cVar1.place(x=150, y=380)

    lblVar2 = tk.Label(ventana, bg=Colors.ColorWhite, text=NVariable2+": ")
    lblVar2.place(x=40, y=410)
    cVar2 = tk.Entry(ventana)
    cVar2.place(x=150, y=410)

    lblVar3 = tk.Label(ventana, bg=Colors.ColorWhite, text=NVariable3+": ")
    lblVar3.place(x=40, y=440)
    cVar3 = tk.Entry(ventana, textvariable=micEdad)
    cVar3.place(x=150, y=440)

    lblVar4 = tk.Label(ventana, bg=Colors.ColorWhite, text=NVariable4+": ")
    lblVar4.place(x=40, y=470)
    cVar4 = tk.Entry(ventana)
    cVar4.place(x=150, y=470)

    lblVar5 = tk.Label(ventana, bg=Colors.ColorWhite, text=NVariable5+": ")
    lblVar5.place(x=40, y=500)
    cVar5 = tk.Entry(ventana)
    cVar5.place(x=150, y=500)

    lblVar6 = tk.Label(ventana, bg=Colors.ColorWhite, text=NVariable6+": ")
    lblVar6.place(x=40, y=530)
    cVar6 = tk.Entry(ventana)
    cVar6.place(x=150, y=530)

    bEvaluar = tk.Button(ventana, bg=Colors.ColorSecundary, text="EVALUAR", font=comp, command=evaluar_prest)
    bEvaluar.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
    bEvaluar.place(x=120, y=550)


def panel_evaluacion():
    panel = tk.Label(ventana, width=80, height=10, borderwidth=1, relief="sunken", bg="white")
    panel.place(x=333, y=415)

    lblTitle = tk.Label(ventana, text="RESULTADOS DE EVALUACIÓN", bg="white",
                        font=font.Font(family='helvetica', size=15, weight="bold"))
    lblTitle.place(x=335, y=420)

    lblPrestamo = tk.Label(ventana, text="EL MONTO A PRESTAR ES DE: S/. ", bg="white")
    lblPrestamo.place(x=335, y=460)

    lblTipPr = tk.Label(ventana, text="TIPO DE PRESTAMO: ", bg="white")
    lblTipPr.place(x=335, y=490)

    global lblResp, lblcat
    lblResp = tk.Label(ventana, text="", bg="white")
    lblResp.place(x=515, y=460)

    lblcat = tk.Label(ventana, text="", bg="white")
    lblcat.place(x=450, y=490)


def switchVar3():
    if (bVariable3['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.DISABLED
        bVariable3['bg'] = Colors.ColorsDisabled
        grafVar3()
        # Ingreso
        bVariable1['state'] = tk.NORMAL
        bVariable1['bg'] = Colors.ColorSecundary
        # CapPago
        bVariable2['state'] = tk.NORMAL
        bVariable2['bg'] = Colors.ColorSecundary
        # Tiempo
        bVariable4['state'] = tk.NORMAL
        bVariable4['bg'] = Colors.ColorSecundary
        # Hijos
        bVariable5['state'] = tk.NORMAL
        bVariable5['bg'] = Colors.ColorSecundary
        # Deudas
        bVariable6['state'] = tk.NORMAL
        bVariable6['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida


def switchVar1():
    if (bVariable1['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.NORMAL
        bVariable3['bg'] = Colors.ColorSecundary
        # Ingreso
        bVariable1['state'] = tk.DISABLED
        bVariable1['bg'] = Colors.ColorsDisabled
        grafVar1()
        # CapPago
        bVariable2['state'] = tk.NORMAL
        bVariable2['bg'] = Colors.ColorSecundary
        # Tiempo
        bVariable4['state'] = tk.NORMAL
        bVariable4['bg'] = Colors.ColorSecundary
        # Hijos
        bVariable5['state'] = tk.NORMAL
        bVariable5['bg'] = Colors.ColorSecundary
        # Deudas
        bVariable6['state'] = tk.NORMAL
        bVariable6['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida


def switchVar2():
    if (bVariable2['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.NORMAL
        bVariable3['bg'] = Colors.ColorSecundary
        # Ingreso
        bVariable1['state'] = tk.NORMAL
        bVariable1['bg'] = Colors.ColorSecundary
        # CapPago
        bVariable2['state'] = tk.DISABLED
        bVariable2['bg'] = Colors.ColorsDisabled
        grafVar2()
        # Tiempo
        bVariable4['state'] = tk.NORMAL
        bVariable4['bg'] = Colors.ColorSecundary
        # Hijos
        bVariable5['state'] = tk.NORMAL
        bVariable5['bg'] = Colors.ColorSecundary
        # Deudas
        bVariable6['state'] = tk.NORMAL
        bVariable6['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida


def switchVar4():
    if (bVariable4['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.NORMAL
        bVariable3['bg'] = Colors.ColorSecundary
        # Ingreso
        bVariable1['state'] = tk.NORMAL
        bVariable1['bg'] = Colors.ColorSecundary
        # CapPago
        bVariable2['state'] = tk.NORMAL
        bVariable2['bg'] = Colors.ColorSecundary
        # Tiempo
        bVariable4['state'] = tk.DISABLED
        bVariable4['bg'] = Colors.ColorsDisabled
        grafVar4()
        # Hijos
        bVariable5['state'] = tk.NORMAL
        bVariable5['bg'] = Colors.ColorSecundary
        # Deudas
        bVariable6['state'] = tk.NORMAL
        bVariable6['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida


def switchVar5():
    if (bVariable5['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.NORMAL
        bVariable3['bg'] = Colors.ColorSecundary
        # Ingreso
        bVariable1['state'] = tk.NORMAL
        bVariable1['bg'] = Colors.ColorSecundary
        # CapPago
        bVariable2['state'] = tk.NORMAL
        bVariable2['bg'] = Colors.ColorSecundary
        # Tiempo
        bVariable4['state'] = tk.NORMAL
        bVariable4['bg'] = Colors.ColorSecundary
        # Hijos
        bVariable5['state'] = tk.DISABLED
        bVariable5['bg'] = Colors.ColorsDisabled
        grafVar5()
        # Deudas
        bVariable6['state'] = tk.NORMAL
        bVariable6['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida


def switchVar6():
    if (bVariable6['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.NORMAL
        bVariable3['bg'] = Colors.ColorSecundary
        # Ingreso
        bVariable1['state'] = tk.NORMAL
        bVariable1['bg'] = Colors.ColorSecundary
        # CapPago
        bVariable2['state'] = tk.NORMAL
        bVariable2['bg'] = Colors.ColorSecundary
        # Tiempo
        bVariable4['state'] = tk.NORMAL
        bVariable4['bg'] = Colors.ColorSecundary
        # Hijos
        bVariable5['state'] = tk.NORMAL
        bVariable5['bg'] = Colors.ColorSecundary
        # Deudas
        bVariable6['state'] = tk.DISABLED
        bVariable6['bg'] = Colors.ColorsDisabled
        grafVar6()
        # Préstamo
        bPrestamo['state'] = tk.NORMAL
        bPrestamo['bg'] = Colors.ColorSalida


def switchPrestamo():
    if (bPrestamo['state'] == tk.NORMAL):
        # Edad
        bVariable3['state'] = tk.NORMAL
        bVariable3['bg'] = Colors.ColorSecundary
        # Ingreso
        bVariable1['state'] = tk.NORMAL
        bVariable1['bg'] = Colors.ColorSecundary
        # CapPago
        bVariable2['state'] = tk.NORMAL
        bVariable2['bg'] = Colors.ColorSecundary
        # Tiempo
        bVariable4['state'] = tk.NORMAL
        bVariable4['bg'] = Colors.ColorSecundary
        # Hijos
        bVariable5['state'] = tk.NORMAL
        bVariable5['bg'] = Colors.ColorSecundary
        # Deudas
        bVariable6['state'] = tk.NORMAL
        bVariable6['bg'] = Colors.ColorSecundary
        # Préstamo
        bPrestamo['state'] = tk.DISABLED
        bPrestamo['bg'] = Colors.ColorsDisabled
        grafPrestamo()


SVar = font.Font(size=10, weight="bold")
#Variable1
bVariable1 = tk.Button(ventana, bg=Colors.ColorSecundary, text=NVariable1, state=tk.DISABLED, command=switchVar1,
                     font=SVar)
bVariable1.configure(relief=tk.GROOVE, background="#e2e2e0", activebackground=Colors.ColorSecundaryDark)
#Variable2
bVariable2 = tk.Button(ventana, bg=Colors.ColorSecundary, text=NVariable2, state=tk.NORMAL,
                     command=switchVar2, font=SVar)
bVariable2.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
#Variable3
bVariable3 = tk.Button(ventana, bg=Colors.ColorSecundary, text=NVariable3, state=tk.NORMAL, command=switchVar3, font=SVar)
bVariable3.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
#Variable4
bVariable4 = tk.Button(ventana, bg=Colors.ColorSecundary, text=NVariable4, state=tk.NORMAL, command=switchVar4, font=SVar)
bVariable4.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
#Variable5
bVariable5 = tk.Button(ventana, bg=Colors.ColorSecundary, text=NVariable5, state=tk.NORMAL, command=switchVar5, font=SVar)
bVariable5.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
#Variable6
bVariable6 = tk.Button(ventana, bg=Colors.ColorSecundary, text=NVariable6, state=tk.NORMAL, command=switchVar6, font=SVar)
bVariable6.configure(relief=tk.GROOVE, background=Colors.ColorSecundary, activebackground=Colors.ColorSecundaryDark)
#VariableSalida
bPrestamo = tk.Button(ventana, bg=Colors.ColorSecundary, text="PRÉSTAMO", state=tk.NORMAL, command=switchPrestamo,
                      font=SVar)
bPrestamo.configure(relief=tk.GROOVE, background=Colors.ColorSalida, activebackground=Colors.ColorSalidaDark)


def reglas_screen():
    global crID, crCondicion1, crCondicion2, crCondicion3, crCondicion4, crCondicion5, crCondicion6, crRegla
    global mirID, mirCondicion1, mirCondicion2, mirCondicion3, mirCondicion4, mirCondicion5, mirCondicion6, mirRegla

    mirID = tk.StringVar()
    mirCondicion1 = tk.StringVar()
    mirCondicion2 = tk.StringVar()
    mirCondicion3 = tk.StringVar()
    mirCondicion4 = tk.StringVar()
    mirCondicion5 = tk.StringVar()
    mirCondicion6 = tk.StringVar()
    mirRegla = tk.StringVar()
    global lblReglas,lblrID,lblrRegla,lblc1,lblc2,lblc3,lblc4,lblc5,lblc6
    lblReglas = tk.Label(ventana, text="REGLAS", font=font.Font(size=15, weight="bold"), bg="#FFFFFF")
    lblReglas.place(x=80, y=15)

    lblrID = tk.Label(ventana, text="ID:", bg=Colors.ColorWhite)
    lblrID.place(x=80, y=70)
    crID = tk.Entry(ventana, textvariable=mirID, state=tk.NORMAL)
    crID.place(x=155, y=70, width=75)
    lblrRegla = tk.Label(ventana, text="Regla:", bg=Colors.ColorWhite)
    lblrRegla.place(x=80, y=100)
    crRegla = tk.Entry(ventana, textvariable=mirRegla, state=tk.DISABLED)
    crRegla.place(x=155, y=100, width=75)

    lblc1 = tk.Label(ventana, text="Condicion 1:", bg=Colors.ColorWhite)
    lblc1.place(x=275, y=70)
    crCondicion1 = tk.Entry(ventana, textvariable=mirCondicion1, state=tk.DISABLED)
    crCondicion1.place(x=350, y=70, width=75)
    lblc2 = tk.Label(ventana, text="Condicion 2:", bg=Colors.ColorWhite)
    lblc2.place(x=275, y=100)
    crCondicion2 = tk.Entry(ventana, textvariable=mirCondicion2, state=tk.DISABLED)
    crCondicion2.place(x=350, y=100, width=75)

    lblc3 = tk.Label(ventana, text="Condicion 3:", bg=Colors.ColorWhite)
    lblc3.place(x=475, y=70)
    crCondicion3 = tk.Entry(ventana, textvariable=mirCondicion4, state=tk.DISABLED)
    crCondicion3.place(x=550, y=70, width=75)
    lblc4 = tk.Label(ventana, text="Condicion 4:", bg=Colors.ColorWhite)
    lblc4.place(x=475, y=100)
    crCondicion4 = tk.Entry(ventana, textvariable=mirCondicion4, state=tk.DISABLED)
    crCondicion4.place(x=550, y=100, width=75)

    lblc5 = tk.Label(ventana, text="Condicion 5:", bg=Colors.ColorWhite)
    lblc5.place(x=675, y=70)
    crCondicion5 = tk.Entry(ventana, textvariable=mirCondicion5, state=tk.DISABLED)
    crCondicion5.place(x=750, y=70, width=75)
    lblc6 = tk.Label(ventana, text="Condicion 6:", bg=Colors.ColorWhite)
    lblc6.place(x=675, y=100)
    crCondicion6 = tk.Entry(ventana, textvariable=mirCondicion6, state=tk.DISABLED)
    crCondicion6.place(x=750, y=100, width=75)

    #BOTONES
    global brBuscar, brModificar, brLimpiar, brGuardar, brActualizar
    brBuscar = tk.Button(ventana, text="BUSCAR", image=Buscar23, compound="left", bg=Colors.ColorSecundary,
                        font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                        command=buscarReglas)
    brBuscar.place(x=80, y=190, width=110, height=25)

    brModificar = tk.Button(ventana, text="MODIFICAR", image=Modificar23, compound="left", bg=Colors.ColorSecundary,
                           font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                           command=modificarReg)
    brModificar.place(x=237.5, y=190, width=110, height=25)

    brLimpiar = tk.Button(ventana, text="LIMPIAR", image=Borrar23, compound="left", bg=Colors.ColorSecundary,
                         font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                         command=limpiarReglas)
    brLimpiar.place(x=395, y=190, width=110, height=25)

    brGuardar = tk.Button(ventana, text="GUARDAR", image=Guardar23, compound="left", bg=Colors.ColorSecundary,
                         font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                         command=guardarReg)
    brGuardar.place(x=552.5, y=190, width=110, height=25)

    brActualizar = tk.Button(ventana, text="ACTUALIZAR", image=Actualizar23, compound="left", bg=Colors.ColorSecundary,
                            font=font.Font(size=10, weight="bold"), activebackground=Colors.ColorSecundary,
                            command=verTablaReglas)
    brActualizar.place(x=710, y=190, width=120, height=25)

    #TABLA DE REGLAS
    global tabla_regla
    tabla_regla = ttk.Treeview(column=(
    "ID_Regla", "Condicion1", "Condicion2", "Condicion3", "Condicion4", "Condicion5", "Condicion6", "Regla"), show='headings')
    tabla_regla.heading("ID_Regla", text="ID_Regla")
    tabla_regla.heading("Condicion1", text="Condicion1")
    tabla_regla.heading("Condicion2", text="Condicion2")
    tabla_regla.heading("Condicion3", text="Condicion3")
    tabla_regla.heading("Condicion4", text="Condicion4")
    tabla_regla.heading("Condicion5", text="Condicion5")
    tabla_regla.heading("Condicion6", text="Condicion6")
    tabla_regla.heading("Regla", text="Regla")
    tabla_regla.place(x=10, y=250, width=900, height=330)

def verTablaReglas():
    tabla_regla.delete(*tabla_regla.get_children())
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()
    miCursor.execute("""SELECT REGLAS.ID_Regla,REGLAS.Condicion1,REGLAS.Condicion2,REGLAS.Condicion3,REGLAS.Condicion4,
        REGLAS.Condicion5, REGLAS.Condicion6, REGLAS.Regla FROM REGLAS""")
    for row in miCursor:
        reglas = (
            '{0} {1} {2} {3} {4} {5} {6} {7}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],))
        tabla_regla.insert("", tk.END, values=reglas)

    miConexion.commit()

def buscarReglas():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("""SELECT ID_Regla, Condicion1, Condicion2, Condicion3, Condicion4, Condicion5, Condicion6, Regla FROM REGLAS
        WHERE ID_Regla= """ + crID.get())

    datosRegla = miCursor.fetchall()
    lista,*asaw=datosRegla
    mirCondicion1.set(lista[1])
    mirCondicion2.set(lista[2])
    mirCondicion3.set(lista[3])
    mirCondicion4.set(lista[4])
    mirCondicion5.set(lista[5])
    mirCondicion6.set(lista[6])
    mirRegla.set(lista[7])

    miConexion.commit()


def limpiarReglas():
    mirID.set("")
    mirCondicion1.set("")
    mirCondicion2.set("")
    mirCondicion3.set("")
    mirCondicion4.set("")
    mirCondicion5.set("")
    mirCondicion6.set("")
    mirRegla.set("")

def modificarReg():
    crCondicion1['state'] = tk.NORMAL
    crCondicion2['state'] = tk.NORMAL
    crCondicion3['state'] = tk.NORMAL
    crCondicion4['state'] = tk.NORMAL
    crCondicion5['state'] = tk.NORMAL
    crCondicion6['state'] = tk.NORMAL
    crRegla['state'] = tk.NORMAL

def bloqReg():
    crCondicion1['state'] = tk.DISABLED
    crCondicion2['state'] = tk.DISABLED
    crCondicion3['state'] = tk.DISABLED
    crCondicion4['state'] = tk.DISABLED
    crCondicion5['state'] = tk.DISABLED
    crCondicion6['state'] = tk.DISABLED
    crRegla['state'] = tk.DISABLED

def guardarReg():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("UPDATE REGLAS SET Condicion1='" + crCondicion1.get() +
                     "',Condicion2='" + crCondicion2.get() +
                     "',Condicion3='" + crCondicion3.get() +
                     "',Condicion4='" + crCondicion4.get() +
                     "',Condicion5='" + crCondicion5.get() +
                     "',Condicion6='" + crCondicion6.get() +
                     "',Regla='" + crRegla.get() +
                     "'WHERE ID_Regla=" + crID.get())

    messagebox.showinfo("DB", "LOS DATOS SE GUARDARON CORRECTAMENTE")
    miConexion.commit()
    bloqReg()

def abVar_crReg():
    cerrar_reglas()
    variables_screen()

def abReg_crVar():
    reglas_screen()
    cerrar_variables()

def cerrar_variables():
    cVID.place_forget()
    cVNombre.place_forget()
    cVTipo.place_forget()
    cValor1.place_forget()
    cValor2.place_forget()
    cValor3.place_forget()
    cBValor1.place_forget()
    cBValor2.place_forget()
    cBValor3.place_forget()
    cVal1Par1.place_forget()
    cVal1Par2.place_forget()
    cVal1Par3.place_forget()
    cVal1Par4.place_forget()
    cVal2Par1.place_forget()
    cVal2Par2.place_forget()
    cVal2Par3.place_forget()
    cVal2Par4.place_forget()
    cVal3Par1.place_forget()
    cVal3Par2.place_forget()
    cVal3Par3.place_forget()
    cVal3Par4.place_forget()

    lblVariable.place_forget()
    cVal3Par1.place_forget()
    lblVariable.place_forget()
    lblID.place_forget()
    lblNombre.place_forget()
    lblTipo.place_forget()
    lblValorL.place_forget()
    lblFunPer.place_forget()
    lblPar.place_forget()

    bBuscar.place_forget()
    bModificar.place_forget()
    bLimpiar.place_forget()
    bGuardar.place_forget()
    bActualizar.place_forget()

    table.place_forget()

def cerrar_reglas():
    crID.place_forget()
    crCondicion1.place_forget()
    crCondicion2.place_forget()
    crCondicion3.place_forget()
    crCondicion4.place_forget()
    crCondicion5.place_forget()
    crCondicion6.place_forget()
    crRegla.place_forget()

    lblReglas.place_forget()
    lblrID.place_forget()
    lblrRegla.place_forget()
    lblc1.place_forget()
    lblc2.place_forget()
    lblc3.place_forget()
    lblc4.place_forget()
    lblc5.place_forget()
    lblc6.place_forget()

    brBuscar.place_forget()
    brModificar.place_forget()
    brLimpiar.place_forget()
    brGuardar.place_forget()
    brActualizar.place_forget()
    tabla_regla.place_forget()

def mostrar_reglas():
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("""SELECT ID_Regla, Condicion1, Condicion2, Condicion3, Condicion4, Condicion5, Condicion6, Regla FROM REGLAS
                    WHERE ID_Regla=6""")

    ex_reglas=miCursor.fetchall()
    l_reglas,*nada=ex_reglas

    global idr,c1,c2,c3,c4,c5,c6,regla_out
    idr=l_reglas[0]
    c1=l_reglas[1]
    c2=l_reglas[2]
    c3=l_reglas[3]
    c4=l_reglas[4]
    c5=l_reglas[5]
    c6=l_reglas[6]
    regla_out=l_reglas[7]
    print(c1,c2,c3,c4,c5,c6)

mostrar_reglas()

def obtener_variablesC():
    global variable1,variable2,variable3,variable4,variable5,variable6
    variable1 = cVar1.get()
    variable2 = cVar2.get()
    variable3 = cVar3.get()
    variable4 = cVar4.get()
    variable5 = cVar5.get()
    variable6 = cVar6.get()



# SKFUZZY

# DEFINICION DE UNIVERSO
# Rango de la calidad del ingresos (soles)
x_variable1 = np.arange(v1val1Par1, v1val3Par4, 1)

# Rango del porcentaje de capapago (soles)
x_variable2 = np.arange(v2val1Par1, v2val3Par4, 1)

# Rango de la calidad de la edad (años)
x_variable3 = np.arange(v3val1Par1, v3val3Par4, 1)

# Rango del porcentaje de tiempo (meses)
x_variable4 = np.arange(v4val1Par1, v4val3Par4, 1)

# Rango del porcentaje de hijos (cantidad)
x_variable5 = np.arange(v5val1Par1, v5val3Par4, 1)

# Rango del porcentaje de deudas (semanas)
x_variable6 = np.arange(v6val1Par1, v6val3Par3, 1)

# Rango del porcentaje de préstamo (soles)
x_prestamo = np.arange(500, 50000, 1)

#CREACION DE VARIABLES DE ENTRADA(ANTECEDENT) y SALIDA(CONSEQUENT)
var1=ctrl.Antecedent(x_variable1, NVariable1)
var2=ctrl.Antecedent(x_variable2, NVariable2)
var3=ctrl.Antecedent(x_variable3, NVariable3)
var4=ctrl.Antecedent(x_variable4, NVariable4)
var5=ctrl.Antecedent(x_variable5, NVariable5)
var6=ctrl.Antecedent(x_variable6, NVariable6)
prestamo=ctrl.Consequent(x_prestamo,'prestamo')

# Ingreso Bajo
v1_val1 = fuzz.trapmf(x_variable1, [v1val1Par1, v1val1Par2, v1val1Par3, v1val1Par4])
# Ingreso Medio
v1_val2 = fuzz.trimf(x_variable1, [v1val2Par1, v1val2Par2, v1val2Par3])
# Ingreso Alto
v1_val3 = fuzz.trapmf(x_variable1, [v1val3Par1, v1val3Par2, v1val3Par3, v1val3Par4])

#Reasignacion de variables
var1[var1val1]=v1_val1
var1[var1val2]=v1_val2
var1[var1val3]=v1_val3

def grafVar1():
    figIng, ax1 = plt.subplots(figsize=(5.5, 3))

    ax1.plot(x_variable1, v1_val1, 'r', linewidth=2, label=var1val1)
    ax1.plot(x_variable1, v1_val2, 'g', linewidth=2, label=var1val2)
    ax1.plot(x_variable1, v1_val3, 'b', linewidth=2, label=var1val3)
    ax1.set_title(NVariable1)
    ax1.legend(loc='upper right')
    #ax1.set_xlabel("X_axis_title")
    #ax1.set_ylabel("Y_axis_title")

    canvas = FigureCanvasTkAgg(figIng, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

# CapPago Bajo
v2_val1 = fuzz.trapmf(x_variable2, [v2val1Par1, v2val1Par2, v2val1Par3, v2val1Par4])
# CapPago Medio
v2_val2 = fuzz.trimf(x_variable2, [v2val2Par1, v2val2Par2, v2val2Par3])
# CapPago Alto
v2_val3 = fuzz.trapmf(x_variable2, [v2val3Par1, v2val3Par2, v2val3Par3, v2val3Par4])

#Reasignacion de variables
var2[var2val1]=v2_val1
var2[var2val2]=v2_val2
var2[var2val3]=v2_val3

def grafVar2():
    figCP, ax2 = plt.subplots(figsize=(5.5, 3))

    ax2.plot(x_variable2, v2_val1, 'r', linewidth=2, label=var2val1)
    ax2.plot(x_variable2, v2_val2, 'g', linewidth=2, label=var2val2)
    ax2.plot(x_variable2, v2_val3, 'b', linewidth=2, label=var2val3)
    ax2.set_title(NVariable2)
    ax2.legend()

    canvas = FigureCanvasTkAgg(figCP, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

# Edad Joven
v3_val1 = fuzz.trapmf(x_variable3, [v3val1Par1, v3val1Par2, v3val1Par3, v3val1Par4])
# Edad Adulta
v3_val2 = fuzz.trimf(x_variable3, [v3val2Par1, v3val2Par2, v3val2Par3])
# Edad Anciano
v3_val3 = fuzz.trapmf(x_variable3, [v3val3Par1, v3val3Par2, v3val3Par3, v3val3Par4])

#Reasignacion de variables
var3[var3val1]=v3_val1
var3[var3val2]=v3_val2
var3[var3val3]=v3_val3

def grafVar3():
    figEdad, ax0 = plt.subplots(figsize=(5.5, 3))

    ax0.plot(x_variable3, v3_val1, 'r', linewidth=2, label=var3val1)
    ax0.plot(x_variable3, v3_val2, 'g', linewidth=2, label=var3val2)
    ax0.plot(x_variable3, v3_val3, 'b', linewidth=2, label=var3val3)
    ax0.set_title(NVariable3)
    ax0.legend()

    canvas = FigureCanvasTkAgg(figEdad, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

# Tiempo nuevo
v4_val1 = fuzz.trapmf(x_variable4, [v4val1Par1, v4val1Par2, v4val1Par3, v4val1Par4])
# Tiempo promedio
v4_val2 = fuzz.trimf(x_variable4, [v4val2Par1, v4val2Par2, v4val2Par3])
# Tiempo antiguo
v4_val3 = fuzz.trapmf(x_variable4, [v4val3Par1, v4val3Par2, v4val3Par3, v4val3Par4])

#Reasignacion de variables
var4[var4val1]=v4_val1
var4[var4val2]=v4_val2
var4[var4val3]=v4_val3

def grafVar4():
    figT, ax3 = plt.subplots(figsize=(5.5, 3))

    ax3.plot(x_variable4, v4_val1, 'r', linewidth=2, label=var4val1)
    ax3.plot(x_variable4, v4_val2, 'g', linewidth=2, label=var4val2)
    ax3.plot(x_variable4, v4_val3, 'b', linewidth=2, label=var4val3)
    ax3.set_title(NVariable4)
    ax3.legend()

    canvas = FigureCanvasTkAgg(figT, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

# Hijos bajo
v5_val1 = fuzz.trapmf(x_variable5, [v5val1Par1, v5val1Par2, v5val1Par3, v5val1Par4])
# Hijos moderado
v5_val2 = fuzz.trimf(x_variable5,  [v5val2Par1, v5val2Par2, v5val2Par3])
# Hijos alto
v5_val3 = fuzz.trapmf(x_variable5, [v5val3Par1, v5val3Par2,v5val3Par3, v5val3Par4])

#Reasignacion de variables
var5[var5val1]=v5_val1
var5[var5val2]=v5_val2
var5[var5val3]=v5_val3

def grafVar5():
    figHi, ax4 = plt.subplots(figsize=(5.5, 3))

    ax4.plot(x_variable5, v5_val1, 'r', linewidth=2, label=var5val1)
    ax4.plot(x_variable5, v5_val2, 'g', linewidth=2, label=var5val2)
    ax4.plot(x_variable5, v5_val3, 'b', linewidth=2, label=var5val3)
    ax4.set_title(NVariable5)
    ax4.legend()

    canvas = FigureCanvasTkAgg(figHi, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

# Deudas bajas
v6_val1 = fuzz.trimf(x_variable6, [v6val1Par1, v6val1Par2, v6val1Par3])
# Deudas medio
v6_val2 = fuzz.trimf(x_variable6, [v6val2Par1, v6val2Par2, v6val2Par3])
# Deudas alto
v6_val3 = fuzz.trimf(x_variable6, [v6val3Par1, v6val3Par2, v6val3Par3])

#Reasignacion de variables
var6[var6val1]=v6_val1
var6[var6val2]=v6_val2
var6[var6val3]=v6_val3

def grafVar6():
    figDe, ax5 = plt.subplots(figsize=(5.5, 3))

    ax5.plot(x_variable6, v6_val1, 'r', linewidth=2, label=var6val1)
    ax5.plot(x_variable6, v6_val2, 'g', linewidth=2, label=var6val2)
    ax5.plot(x_variable6, v6_val3, 'b', linewidth=2, label=var6val3)
    ax5.set_title(NVariable6)
    ax5.legend()

    canvas = FigureCanvasTkAgg(figDe, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

# Préstamo bajas
pr_ba = fuzz.trimf(x_prestamo, [500, 500, 7500])
# Préstamo medio
pr_me = fuzz.trimf(x_prestamo, [5000, 15000, 30000])
# Préstamo alto
pr_al = fuzz.trimf(x_prestamo, [25000, 50000, 50000])

#Reasignacion de variables
prestamo['BAJO']=pr_ba
prestamo['MODERADO']=pr_me
prestamo['ALTO']=pr_al

def grafPrestamo():
    figPr, ax6 = plt.subplots(figsize=(5.5, 3))
    ax6.plot(x_prestamo, pr_ba, 'r', linewidth=2, label='BAJO')
    ax6.plot(x_prestamo, pr_me, 'g', linewidth=2, label='MODERADO')
    ax6.plot(x_prestamo, pr_al, 'b', linewidth=2, label='ALTO')
    ax6.set_title("Préstamo")
    ax6.legend()

    canvas = FigureCanvasTkAgg(figPr, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().place(x=333, y=75)

    toolbar = NavigationToolbar2Tk(canvas, ventana)
    toolbar.place(x=333, y=375)
    toolbar.update()

"""def clientevarsalida():
    plt.plot([prestamos, prestamos], [0.0, 1.0], linestyle="--")
    plt.plot(prestamos, pr_ba)
    plt.plot(prestamos, pr_me)
    plt.plot(prestamos, pr_al)"""

def definir_reglas():
    global regla1,regla2,regla3
    regla1=ctrl.Rule(var1[var1val1] & var2[var2val1] & var3[var3val1] & var4[var4val1] & var5[var5val1] & var6[var6val1],prestamo['BAJO'])
    regla2=ctrl.Rule(var1[var1val2] & var2[var2val2] & var3[var3val2] & var4[var4val2] & var5[var5val2] & var6[var6val2],prestamo['MODERADO'])
    regla3=ctrl.Rule(var1[var1val3] & var2[var2val3] & var3[var3val3] & var4[var4val3] & var5[var5val3] & var6[var6val3],prestamo['ALTO'])

definir_reglas()
control = ctrl.ControlSystem([regla1, regla2, regla3])
controlar = ctrl.ControlSystemSimulation(control)

def evaluar_prest():
    panel_evaluacion()
    obtener_variablesC()
    controlar.input[NVariable1] = int(variable1)
    controlar.input[NVariable2] = int(variable2)
    controlar.input[NVariable3] = int(variable3)
    controlar.input[NVariable4] = int(variable4)
    controlar.input[NVariable5] = int(variable5)
    controlar.input[NVariable6] = int(variable6)
    controlar.compute()
    global resultado
    resultado=controlar.output['prestamo']
    lblResp.configure(text=str(round(resultado, 2)))
    prestamo.view(sim=controlar)

ventana.mainloop()