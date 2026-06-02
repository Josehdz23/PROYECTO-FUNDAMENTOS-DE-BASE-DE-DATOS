import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from login import Login
from maincontrol import Principal

app = QApplication(sys.argv)

loader = QUiLoader()

# Abro el login
archivo = QFile("login.ui")
archivo.open(QFile.ReadOnly)
ventana_login = loader.load(archivo)
archivo.close()

# Para abrir mi ventana
ventana_principal = None

def abrir_principal(usuario_db):
    global ventana_principal

    archivo = QFile("ventana.ui")
    archivo.open(QFile.ReadOnly)
    ventana_principal = loader.load(archivo)
    archivo.close()

    rol_usuario = usuario_db['tipo']
    ventana_principal.controlador = Principal(ventana_principal, rol_usuario)

    ventana_principal.show()

login_controller = Login(ventana_login, abrir_principal)

ventana_login.show()
sys.exit(app.exec())