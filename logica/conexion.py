import mysql.connector
#TODO: Hola Mundo
#! Hola Mundo
#* Hola mundo
#? Hola Mundo
#& Hola Mundo

def conectar():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="coltis_productos",
        port=3308
    )
    return db