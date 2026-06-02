from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMessageBox
from conexion_db import conectar

class Login:
    def __init__(self, ventana, abrir_principal):
        self.ventana = ventana
        self.abrir_principal = abrir_principal
        self.ventana.setMinimumSize(QSize(399, 321))
        self.ventana.setMaximumSize(QSize(399, 321))

        self.ventana.btn_login.clicked.connect(self.verificar_login)
        self.ventana.btn_salir.clicked.connect(self.salir)

    def salir(self):
        self.ventana.close()

    def verificar_login(self):
        usuario_ingresado = self.ventana.input_user.text()
        password_ingresada = self.ventana.input_password.text()

        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            query = "SELECT * FROM empleados WHERE nombre = %s AND contraseña = %s"
            valores = (usuario_ingresado, password_ingresada)

            cursor.execute(query, valores)
            usuario_db = cursor.fetchone()

            if usuario_db:
                QMessageBox.information(self.ventana, "Éxito", f"¡Bienvenido {usuario_db['nombre']}!")

                self.ventana.close()
                self.abrir_principal(usuario_db)

            else:
                QMessageBox.warning(self.ventana, "Error", "Usuario o contraseña incorrectos.")

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"Error en la consulta: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()


