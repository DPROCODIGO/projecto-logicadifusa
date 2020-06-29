import sqlite3
from tkinter import messagebox


global table

def conexionBBDD():
    try:
        miConexion = sqlite3.connect("BDPrestamoPersonal")
        miCursor = miConexion.cursor()

        miCursor.execute("""
                CREATE TABLE PRESTAMOS(
                ID_Prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
                Cantidad INTEGER,
                Categoria VARCHAR(30),
                Fecha_Eval DATETIME
                )
            """)

        miCursor.execute("""
                CREATE TABLE CLIENTES(
                ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                DNI INTEGER(8) UNIQUE,
                Nombre VARCHAR(50) NOT NULL,
                Apellido VARCHAR(50) NOT NULL,
                Correo VARCHAR(50),
                Celular INTEGER(9),
                Fech_Nac DATE NOT NULL,
                ID_Prestamo INTEGER,
                ID_Empleado INTEGER,
                FOREIGN KEY (ID_Prestamo)
                    REFERENCES PRESTAMOS (ID_Prestamo)
                FOREIGN KEY (ID_Empleado)
                    REFERENCES EMPLEADOS (ID_Empleado)
                )
            """)

        miCursor.execute("""
                CREATE TABLE EMPLEADOS(
                ID_Empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                Usuario TEXT,
                Contraseña TEXT,
                Rol VARCHAR(30),
                Nombre VARCHAR(30),
                Apellido VARCHAR(30),
                Correo VARCHAR(50)
                )
            """)

        miCursor.execute("""
                CREATE TABLE PRESTAMO_VARIABLE(
                ID_Prestamo INTEGER,
                ID_Variable INTEGER,
                FOREIGN KEY (ID_Prestamo)
                    REFERENCES PRESTAMOS (ID_Prestamo)
                FOREIGN KEY (ID_Variable)
                    REFERENCES VARIABLES (ID_Variable)
                )
            """)

        miCursor.execute("""
                CREATE TABLE VARIABLES(
                ID_Variable INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre VARCHAR(30),
                Tipo VARCHAR(30),
                ID_Empleado INTEGER,
                FOREIGN KEY (ID_Empleado)
                    REFERENCES EMPLEADOS (ID_Empleado)
                )
             """)

        miCursor.execute("""
                CREATE TABLE VALORES_LINGUISTICOS(
                ID_Valor INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre VARCHAR(30),
                Func_Pertenencia VARCHAR(30),
                Parametro1 INTEGER,
                Parametro2 INTEGER,
                Parametro3 INTEGER,
                Parametro4 INTEGER,
                ID_Variable INTEGER,
                FOREIGN KEY (ID_Variable)
                    REFERENCES VARIABLES (ID_Variable)
                )
            """)

        messagebox.showinfo("BBDD", "La base de datos se ha creado exitosamente")

    except:
        messagebox.showinfo("BBDD","Ingreso Satisfactoriamente")


