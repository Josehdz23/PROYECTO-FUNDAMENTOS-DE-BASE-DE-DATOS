from PySide6.QtWidgets import QMessageBox
from conexion_db import conectar

class Principal:
    def __init__(self, ventana, rol):
        self.ventana = ventana
        self.rol = rol
        self.ventana.showMaximized()
        self.configurar_permisos()
        self.ventana.btn_guardar_alumno.clicked.connect(self.agregar_alumno)

    def configurar_permisos(self):
        if self.rol != "admin":
            self.ventana.tabWidget.removeTab(17)
            self.ventana.tabWidget.removeTab(16)
            self.ventana.tabWidget.removeTab(14)
            self.ventana.tabWidget.removeTab(12)
            self.ventana.tabWidget.removeTab(9)
            self.ventana.tabWidget.removeTab(7)
            self.ventana.tabWidget.removeTab(6)
            self.ventana.tabWidget.removeTab(5)
            self.ventana.tabWidget.removeTab(4)
            self.ventana.tabWidget.removeTab(3)
            self.ventana.tabWidget.removeTab(2)

    def agregar_alumno(self):
        nombre = self.ventana.input_nombre.text()
        correo = self.ventana.input_correo.text()
        telefono = self.ventana.input_telefono.text()
        dpi = self.ventana.input_dpi.text()
        fecha_nac = self.ventana.input_fecha.date().toString("yyyy-MM-dd")

        if not nombre or not dpi or not correo:
            QMessageBox.warning(self.ventana, "Advertencia", "El nombre, el DPI y correo son obligatorios.")
            return
        else:
            if "@gmail.com" not in correo and "@hotmail.com" not in correo:
                QMessageBox.warning(self.ventana, "Advertencia", "El correo debe ser de dominio @gmail o @hotmail.")
                return


        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            query = """
                    INSERT INTO alumnos (nombre, correo, telefono, dpi, fecha_nacimiento)
                    VALUES (%s, %s, %s, %s, %s) \
                    """
            valores = (nombre, correo, telefono, dpi, fecha_nac)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Alumno registrado correctamente.")

            self.ventana.input_nombre.clear()
            self.ventana.input_correo.clear()
            self.ventana.input_telefono.clear()
            self.ventana.input_dpi.clear()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()