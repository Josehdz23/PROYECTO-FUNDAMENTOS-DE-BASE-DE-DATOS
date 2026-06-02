import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='academia_de_belleza',
            user='root',
            password='Jose2301Fortnite'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None