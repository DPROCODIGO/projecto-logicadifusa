import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from tkinter import messagebox

def recuperar_contraseña(correo_usuario):
    miConexion = sqlite3.connect("BDPrestamoPersonal")

    miCursor = miConexion.cursor()

    miCursor.execute("SELECT Usuario, Contraseña FROM EMPLEADOS WHERE Correo=" + "'" + correo_usuario + "'")

    DatosMail = miCursor.fetchall()
    Data1, *Data2 = DatosMail
    Rec_Usuario = Data1[0]
    Rec_Pass = Data1[1]

    miConexion.commit()

    msg = MIMEMultipart()

    message="HOLA!\n\nTú estas recibiendo este correo porque nosotros recibimos una solicitud de envio de datos para tu cuenta de correo.\n\n\n"
    messageUser = "Usuario: " + Rec_Usuario
    messagePass = "Contraseña: " + Rec_Pass

    password = "udella2020"
    msg['From'] = "udella.project@gmail.com"
    msg['To'] = correo_usuario
    msg['Subject'] = "RECUPERACIÓN DE CONTRASEÑA - UDELLA"

    msg.attach(MIMEText(message, 'plain'))
    msg.attach(MIMEText(messageUser, 'plain'))
    msg.attach(MIMEText(messagePass, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    messagebox.showinfo("DB","Enviado exitosamente.\nPor Favor, revise su correo.")
    server.quit()
