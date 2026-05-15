import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

app = QApplication(sys.argv)

loader = QUiLoader()
archivo = QFile("interfaz.ui")
archivo.open(QFile.ReadOnly)

ventana = loader.load(archivo)
archivo.close()

# 🔹 Función del login
def verificar_login():
    usuario = ventana.input_user.text()
    password = ventana.input_password.text()

    # 👇 Usuario y contraseña "correctos"
    if usuario == "admin" and password == "1234":
        ventana.label_resultado.setText("✅ Bienvenido bro 😎")
    else:
        ventana.label_resultado.setText("❌ Usuario o contraseña incorrectos")

# 🔹 Conectar botón
ventana.btn_login.clicked.connect(verificar_login)

ventana.show()
sys.exit(app.exec())