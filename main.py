import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from login import Login
from autenticacion import Auth
from maincontrol import Principal

app = QApplication(sys.argv)

loader = QUiLoader()

# 🔹 Cargar login
archivo = QFile("login.ui")
archivo.open(QFile.ReadOnly)
ventana_login = loader.load(archivo)
archivo.close()

# 🔹 Función para abrir principal
ventana_principal = None

def abrir_principal(rol):
    global ventana_principal

    archivo = QFile("ventana.ui")
    archivo.open(QFile.ReadOnly)
    ventana_principal = loader.load(archivo)
    archivo.close()

    Principal(ventana_principal, rol)
    ventana_principal.show()

# 🔹 Inyecciones (SOLID)
auth = Auth()
login_controller = Login(ventana_login, auth, abrir_principal)

ventana_login.show()
sys.exit(app.exec())