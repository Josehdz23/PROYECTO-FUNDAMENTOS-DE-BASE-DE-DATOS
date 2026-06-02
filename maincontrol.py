from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from conexion_db import conectar

class Principal:
    def __init__(self, ventana, rol):
        self.ventana = ventana
        self.rol = rol
        self.configurar_permisos()
        self.ventana.setMaximumSize(QSize(1280, 720))
        self.ventana.setMinimumSize(QSize(1280, 720))
        self.cargar_alumnos()
        self.ventana.btn_guardar_alumno.clicked.connect(self.agregar_alumno)
        self.ventana.input_buscar.textChanged.connect(self.buscar_alumno)
        self.ventana.tabla_alumnos.setStyleSheet("""
                    QTableWidget {
                        background-color: #FFFFFF; /* Fondo blanco */
                        color: #000000;            /* Texto negro */
                    }
                    QHeaderView::section {
                        background-color: #E0E0E0; /* Fondo gris para los títulos */
                        color: #000000;            /* Texto negro para los títulos */
                        font-weight: bold;         /* Títulos en negrita */
                    }
                """)

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
            self.cargar_alumnos()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_alumnos(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = "SELECT * FROM alumnos"
                cursor.execute(query)
            else:
                query = "SELECT * FROM alumnos WHERE nombre LIKE %s"
                termino = f"{busqueda}%"
                cursor.execute(query, (termino,))

            alumnos = cursor.fetchall()

            self.ventana.tabla_alumnos.setRowCount(0)

            self.ventana.tabla_alumnos.setColumnCount(6)
            self.ventana.tabla_alumnos.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Correo', 'Teléfono', 'DPI', 'Fecha Nac.'])

            self.ventana.tabla_alumnos.setColumnWidth(0, 50)  # ID fijo
            self.ventana.tabla_alumnos.setColumnWidth(1, 300)  # Nombre fijo

            # 🔹 Esta línea hace que el Correo (columna 2) se estire llenando el espacio vacío
            self.ventana.tabla_alumnos.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

            self.ventana.tabla_alumnos.setColumnWidth(3, 100)  # Teléfono fijo
            self.ventana.tabla_alumnos.setColumnWidth(4, 150)  # DPI fijo
            self.ventana.tabla_alumnos.setColumnWidth(5, 100)  # Fecha fijo

            for fila_idx, alumno in enumerate(alumnos):
                self.ventana.tabla_alumnos.insertRow(fila_idx)

                self.ventana.tabla_alumnos.setItem(fila_idx, 0, QTableWidgetItem(str(alumno['id'])))
                self.ventana.tabla_alumnos.setItem(fila_idx, 1, QTableWidgetItem(str(alumno['nombre'])))
                self.ventana.tabla_alumnos.setItem(fila_idx, 2, QTableWidgetItem(str(alumno['correo'])))
                self.ventana.tabla_alumnos.setItem(fila_idx, 3, QTableWidgetItem(str(alumno['telefono'])))
                self.ventana.tabla_alumnos.setItem(fila_idx, 4, QTableWidgetItem(str(alumno['dpi'])))
                self.ventana.tabla_alumnos.setItem(fila_idx, 5, QTableWidgetItem(str(alumno['fecha_nacimiento'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_alumno(self):
        texto_busqueda = self.ventana.input_buscar.text()
        self.cargar_alumnos(texto_busqueda)