#!/usr/bin/python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
# Obtener datos del Analizador de Red Schneider PowerLogic PM5110 modbus TCP con python
# - Producto https://www.se.com/ww/en/product-range/61281-powerlogic-pm5000-series/
# - Manual usuario: http://pdfstream.manualsonline.com/a/a3ae7da6-b5c2-4d0d-9465-e7166dc7d750.pdf
# - Lista de registros modbus: https://www.se.com/ww/en/faqs/FA234017/
#
# Dado que estos equipos son Modbus RTU, para obtener los datos mediante Modbus TCP usamos una pasarela EGX150 de Schneider, Link 150.
# - Modelo: https://www.se.com/es/es/product/EGX150/link-150---ethernet-gateway---2-ethernetport---24-v-dc-and-poe/
# - User Guide: https://download.schneider-electric.com/files?p_enDocType=User+guide&p_File_Name=DOCA0110EN-04.pdf&p_Doc_Ref=DOCA0110EN
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# Librerías:
# - struct: https://docs.python.org/3/library/struct.html
# - comando instalación: pip install pymodbus
# - pymodbus instalación: https://pypi.org/project/pymodbus/
# - pymodbus: https://pymodbus.readthedocs.io/en/latest/
# --------------------------------------------------------------------------- #
import struct
from pymodbus.client.sync import ModbusTcpClient

# --------------------------------------------------------------------------- #
# configure the client logging debug:
#
# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# configure BBDD
# instalar como administrador: pip install mysql-connector-python (https://pypi.org/project/mysql-connector-python/)
# conector: https://dev.mysql.com/downloads/connector/python/8.0.html
# documentación: https://dev.mysql.com/doc/connector-python/en/
# --------------------------------------------------------------------------- #
import mysql.connector as my_dbapi

# --------------------------------------------------------------------------- # 
# Mandar email
# smptlib is part of python's standard library, so you do not have to install it.
#
# Installar email:
# easy_install --upgrade setuptools
# pip install email
# o en windows usar easy_install email
# --------------------------------------------------------------------------- # 
import smtplib
from email.mime.text import MIMEText

destinatarios = ['micorreo@midominio.es']

# --------------------------------------------------------------------------- #
# Funciones: envio de correo
# --------------------------------------------------------------------------- #

def manda_correo(subject, texto, toaddr):
    msg = MIMEText(texto)
    fromaddr = "PowerMeter_PM5110@midominio.es"
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    msg['Subject'] = subject
    s = smtplib.SMTP('miservidordecorreo.com')
    # Next, log in to the server
    # s.login("youremailusername", "password")
    s.sendmail(fromaddr, toaddr, msg.as_string())
    s.quit()
    print(subject)
    print(texto)

values = ['I_A','I_B','I_C','I_N','V_A','V_B','V_C','V_N','P_A','P_B','P_C','potencia_activa_total','potencia_reactiva_total',
          'factor_potencia_total','frecuencia','THD_I_A','THD_I_B','THD_I_C','THD_V_A','THD_V_B','THD_V_C']

monitores_energia = {'primer_PM5110':{'ip':'10.10.10.10','id':1,'I_A':0,'I_B':0,'I_C':0,'I_N':0,'V_A':0,'V_B':0,'V_C':0,'V_N':0,
	'P_A':0,'P_B':0,'P_C':0,'potencia_activa_total':0,'potencia_reactiva_total':0,'factor_potencia_total':0,
	'frecuencia':0,'THD_I_A':0,'THD_I_B':0,'THD_I_C':0,'THD_V_A':0,'THD_V_B':0,'THD_V_C':0},
	'segundo_PM5110':{'ip':'10.10.10.11','id':2,'I_A':0,'I_B':0,'I_C':0,'I_N':0,'V_A':0,'V_B':0,'V_C':0,'V_N':0,
	'P_A':0,'P_B':0,'P_C':0,'potencia_activa_total':0,'potencia_reactiva_total':0,'factor_potencia_total':0,
	'frecuencia':0,'THD_I_A':0,'THD_I_B':0,'THD_I_C':0,'THD_V_A':0,'THD_V_B':0,'THD_V_C':0}}
	
modbus_registers = {'I_A':3000,'I_B':3002,'I_C':3004,'I_N':3006,'V_A':3028,'V_B':3030,'V_C':3032,'V_N':3034,
	'P_A':3054,'P_B':3056,'P_C':3058,'potencia_activa_total':3060,'potencia_reactiva_total':3068,'factor_potencia_total':3084,
	'frecuencia':3110,'THD_I_A':21300,'THD_I_B':21302,'THD_I_C':21304,'THD_V_A':21330,'THD_V_B':21332,'THD_V_C':21334}

modbus_words = {'I_A':2,'I_B':2,'I_C':2,'I_N':2,'V_A':2,'V_B':2,'V_C':2,'V_N':2,
	'P_A':2,'P_B':2,'P_C':2,'potencia_activa_total':2,'potencia_reactiva_total':2,'factor_potencia_total':2,
	'frecuencia':2,'THD_I_A':2,'THD_I_B':2,'THD_I_C':2,'THD_V_A':2,'THD_V_B':2,'THD_V_C':2}
	
modbus_unidades = {'I_A':'A','I_B':'A','I_C':'A','I_N':'A','V_A':'V','V_B':'V','V_C':'V','V_N':'V',
	'P_A':'kW','P_B':'kW','P_C':'kW','potencia_activa_total':'kW','potencia_reactiva_total':'kVAR','factor_potencia_total':'4Q_FP',
	'frecuencia':'Hz','THD_I_A':'%','THD_I_B':'%','THD_I_C':'%','THD_V_A':'%','THD_V_B':'%','THD_V_C':'%'}
	
# --------------------------------------------------------------------------- # 
# Server: miservidor.com
# BBDD: PM5110
# Tablas:
#   - PMs: Guarda el estado de cada monitor para saber si está conectado o no
#   - Datos_xxxx: Guarda los datos de cada monitor
# --------------------------------------------------------------------------- # 
cnx_my = my_dbapi.connect(user='usuario', password='password', host='miservidor.com', database='PM5110')
cursor_my = cnx_my.cursor()

# Consulta monitores modelo
for monitor in monitores_energia:
    try:
        client = ModbusTcpClient(monitores_energia[monitor]['ip'], port=502, timeout=10)
        client.connect()

        #actualizar estado conexión
        query_conexion = "SELECT * FROM PMs WHERE Name = '" + monitor + "'"
        cursor_my.execute(query_conexion)
        myresult = cursor_my.fetchone()
        conexion = myresult[2]
        if conexion == 0:
            query_update = "UPDATE PMs SET Connection = 1 WHERE Name = '" + monitor + "'"
            cursor_my.execute(query_update)
            cnx_my.commit()
            print("Recuperada conexión en Power Meter " + monitor)
            subj = "Recuperada conexión en Power Meter " + monitor
            text = "El Power Meter " + monitor + " ha recuperado la conexion"
            manda_correo(subj, text, destinatarios)

        for medida, registro in modbus_registers.items():
            try:
                read = client.read_holding_registers(registro-1, modbus_words[medida],unit=monitores_energia[monitor]['id']) #resto 1 al desplazamiento al empezar desde cero
                #cuando hay dos valores hay que hacer el cálculo
                dato = struct.pack("<H",read.registers[0]) #primer registro 
                dato2 = struct.pack("<H",read.registers[1]) #segundo registro
                valor = struct.unpack("<f",dato2+dato) #float32 como concatenación de dos int16
                #print(valor[0])
                
                #El factor de potencia es tipo de datos 4Q FP PF - Four Quadrant Floating Point Power Factor
                #Q1: 0 < x < 1
                #Q2: -2 < x < -1
                #Q3: -1 < x < 0
                #Q4: 1 < x < 2

                if (medida == 'factor_potencia_total') and (valor[0] > 1): #si es capacitiva Q4 adapto el valor
                    monitores_energia[monitor][medida] = -( 2 - valor[0])
                    print(monitor + "--> " + medida + " : " + str(monitores_energia[monitor][medida]))
                else:
                    monitores_energia[monitor][medida] = valor[0]
                    print(monitor + "--> " + medida + " : " + str(monitores_energia[monitor][medida]))
            except:
                print("error registro modbus")

        #grabo en BBDD
        try:
            query_my = "INSERT INTO Datos_" + monitor + " (" + ",".join(values) +\
            ") VALUES (" + ",".join([str(monitores_energia[monitor][key]) for key in values]) + ")"
            cursor_my.execute(query_my)
            cnx_my.commit()

        except:
            print("Error BBDD")
            
        client.close()

    except:
        #actualizar estado conexión
        query_conexion = "SELECT * FROM PMs WHERE Name = '" + monitor + "'"
        cursor_my.execute(query_conexion)
        myresult = cursor_my.fetchone()
        conexion = myresult[2]
        if conexion == 1:
            query_update = "UPDATE PMs SET Connection = 0 WHERE Name = '" + monitor + "'"
            cursor_my.execute(query_update)
            cnx_my.commit()
            print("Perdida conexión en Power Meter " + monitor)
            subj = "Perdida conexión en Power Meter " + monitor
            text = "El Power Meter " + monitor + " ha perdido la conexion"
            manda_correo(subj, text, destinatarios)

cnx_my.close()

#publica en MQTT hecho con Node-RED
