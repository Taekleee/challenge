import pymysql

def conexion():

    return pymysql.connect(host='localhost', user='root', password='mypassword', db='CHALLENGE')
    print("Conectado")