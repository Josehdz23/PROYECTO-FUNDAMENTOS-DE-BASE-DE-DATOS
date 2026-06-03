from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from conexion_db import conectar

class Principal:
    def __init__(self, ventana, rol):
        #Estos me inician el programa
        self.ventana = ventana
        self.rol = rol
        self.ventana.setMaximumSize(QSize(1280, 720))
        self.ventana.setMinimumSize(QSize(1280, 720))
        self.configurar_permisos()
        self.cargar_alumnos()
        self.cargar_empleados()

        # Estos me sirven para mis tabs
        self.id_alumno_modificar = None
        self.id_empleado_modficar = None

        # Botones para las modificaciones
        self.ventana.btn_buscar_mod.clicked.connect(self.buscar_para_modificar)
        self.ventana.btn_guardar_mod.clicked.connect(self.actualizar_alumno)
        self.ventana.btn_buscar_mod_empleado.clicked.connect(self.buscar_para_modificar_empleado)
        self.ventana.btn_guardar_mod_empleado.clicked.connect(self.actualizar_empleado)

        # Botones para la limpieza
        self.ventana.btn_limpiar.clicked.connect(self.limpiar)
        self.ventana.btn_limpiar_mod.clicked.connect(self.limpiar)
        self.ventana.btn_limpiar_empleado.clicked.connect(self.limpiar)
        self.ventana.btn_limpiar_mod_empleado.clicked.connect(self.limpiar)

        # Botones para guardar
        self.ventana.btn_guardar_alumno.clicked.connect(self.agregar_alumno)
        self.ventana.btn_guardar_empleado.clicked.connect(self.agregar_empleado)

        # Botonoes para buscar
        self.ventana.input_buscar.textChanged.connect(self.buscar_alumno)
        self.ventana.input_buscarempleado.textChanged.connect(self.buscar_empleado)

    def limpiar(self):
        #Tab Agregar Alumno
        self.ventana.input_nombre.clear()
        self.ventana.input_correo.clear()
        self.ventana.input_telefono.clear()
        self.ventana.input_dpi.clear()

        #Tab Modificar Alumno
        self.ventana.input_buscar_dpi_mod.clear()
        self.ventana.input_mod_nombre.clear()
        self.ventana.input_mod_correo.clear()
        self.ventana.input_mod_telefono.clear()
        self.ventana.input_mod_dpi.clear()

        #Tab Nuevo Empleado
        self.ventana.input_nombre_empleado.clear()
        self.ventana.input_correo_empleado.clear()
        self.ventana.input_dpi_empleado.clear()
        self.ventana.input_telefono_empleado.clear()
        self.ventana.input_rol.clear()
        self.ventana.input_password.clear()

        #Tab Modificar Empleado
        self.ventana.input_buscar_dpi_mod_empleado.clear()
        self.ventana.input_mod_nombre_empleado.clear()
        self.ventana.input_mod_correo_empleado.clear()
        self.ventana.input_mod_telefono_empleado.clear()
        self.ventana.input_mod_dpi_empleado.clear()
        self.ventana.input_rol_mod.clear()
        self.ventana.input_password_mod.clear()

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

    # Manejo de datos alumnos
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

            self.ventana.tabla_alumnos.setColumnWidth(0, 50)
            self.ventana.tabla_alumnos.setColumnWidth(1, 300)

            self.ventana.tabla_alumnos.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

            self.ventana.tabla_alumnos.setColumnWidth(3, 100)
            self.ventana.tabla_alumnos.setColumnWidth(4, 150)
            self.ventana.tabla_alumnos.setColumnWidth(5, 100)

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

    def buscar_para_modificar(self):
        dpi_buscado = self.ventana.input_buscar_dpi_mod.text()

        if not dpi_buscado:
            QMessageBox.warning(self.ventana, "Advertencia", "Ingresa un DPI para buscar.")
            return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM alumnos WHERE dpi = %s"
            cursor.execute(query, (dpi_buscado,))
            alumno = cursor.fetchone()

            if alumno:
                self.id_alumno_modificar = alumno['id']

                self.ventana.input_mod_nombre.setText(alumno['nombre'])
                self.ventana.input_mod_correo.setText(alumno['correo'])
                self.ventana.input_mod_telefono.setText(alumno['telefono'])
                self.ventana.input_mod_dpi.setText(alumno['dpi'])

                QMessageBox.information(self.ventana, "Encontrado", "Modifica los datos y presiona Guardar.")
            else:
                QMessageBox.warning(self.ventana, "Error", "No se encontró ningún alumno con ese DPI.")

        except Exception as e:
            print(f"Error al buscar para modificar: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def actualizar_alumno(self):
        if self.id_alumno_modificar is None:
            QMessageBox.warning(self.ventana, "Advertencia", "Primero busca un alumno para modificar.")
            return

        nuevo_nombre = self.ventana.input_mod_nombre.text()
        nuevo_correo = self.ventana.input_mod_correo.text().lower().strip()
        nuevo_telefono = self.ventana.input_mod_telefono.text()
        nuevo_dpi = self.ventana.input_mod_dpi.text()

        if not nuevo_nombre or not nuevo_dpi or not nuevo_correo:
            QMessageBox.warning(self.ventana, "Advertencia", "El nombre, el DPI y correo son obligatorios.")
            return
        else:
            if "@gmail.com" not in nuevo_correo and "@hotmail.com" not in nuevo_correo:
                QMessageBox.warning(self.ventana, "Advertencia", "El correo debe ser de dominio @gmail o @hotmail.")
                return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor()

            query = """
                    UPDATE alumnos
                    SET nombre   = %s, \
                        correo   = %s, \
                        telefono = %s, \
                        dpi      = %s
                    WHERE id = %s \
                    """
            valores = (nuevo_nombre, nuevo_correo, nuevo_telefono, nuevo_dpi, self.id_alumno_modificar)

            cursor.execute(query, valores)
            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Alumno actualizado correctamente.")

            self.id_alumno_modificar = None
            self.ventana.input_buscar_dpi_mod.clear()
            self.ventana.input_mod_nombre.clear()
            self.ventana.input_mod_correo.clear()
            self.ventana.input_mod_telefono.clear()
            self.ventana.input_mod_dpi.clear()

            self.cargar_alumnos()

        except Exception as e:
            print(f"Error al actualizar: {e}")
            QMessageBox.critical(self.ventana, "Error", f"No se pudo actualizar: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Manejo datos Empleados
    def agregar_empleado(self):
        nombre = self.ventana.input_nombre_empleado.text()
        correo = self.ventana.input_correo_empleado.text()
        telefono = self.ventana.input_telefono_empleado.text()
        dpi = self.ventana.input_dpi_empleado.text()
        tipo = self.ventana.input_rol.text()
        password = self.ventana.input_password.text()
        fecha_nac = self.ventana.input_fecha_empleado.date().toString("yyyy-MM-dd")

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
                    INSERT INTO empleados (nombre, correo, telefono, dpi, fecha_nacimiento, tipo, contraseña)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) \
                    """
            valores = (nombre, correo, telefono, dpi, fecha_nac, tipo, password)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Empleado registrado correctamente.")

            self.ventana.input_nombre_empleado.clear()
            self.ventana.input_correo_empleado.clear()
            self.ventana.input_dpi_empleado.clear()
            self.ventana.input_telefono_empleado.clear()
            self.ventana.input_rol.clear()
            self.ventana.input_password.clear()
            self.cargar_empleados()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_empleados(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = "SELECT * FROM empleados"
                cursor.execute(query)
            else:
                query = "SELECT * FROM empleados WHERE nombre LIKE %s"
                termino = f"{busqueda}%"
                cursor.execute(query, (termino,))

            empleados = cursor.fetchall()

            self.ventana.tabla_empleados.setRowCount(0)

            self.ventana.tabla_empleados.setColumnCount(7)
            self.ventana.tabla_empleados.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Correo', 'Teléfono', 'DPI', 'Fecha Nac.', 'Tipo'])

            self.ventana.tabla_empleados.setColumnWidth(0, 50)
            self.ventana.tabla_empleados.setColumnWidth(1, 300)

            self.ventana.tabla_empleados.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

            self.ventana.tabla_empleados.setColumnWidth(3, 100)
            self.ventana.tabla_empleados.setColumnWidth(4, 150)
            self.ventana.tabla_empleados.setColumnWidth(5, 100)
            self.ventana.tabla_empleados.setColumnWidth(6, 100)

            for fila_idx, empleado in enumerate(empleados):
                self.ventana.tabla_empleados.insertRow(fila_idx)

                self.ventana.tabla_empleados.setItem(fila_idx, 0, QTableWidgetItem(str(empleado['id'])))
                self.ventana.tabla_empleados.setItem(fila_idx, 1, QTableWidgetItem(str(empleado['nombre'])))
                self.ventana.tabla_empleados.setItem(fila_idx, 2, QTableWidgetItem(str(empleado['correo'])))
                self.ventana.tabla_empleados.setItem(fila_idx, 3, QTableWidgetItem(str(empleado['telefono'])))
                self.ventana.tabla_empleados.setItem(fila_idx, 4, QTableWidgetItem(str(empleado['dpi'])))
                self.ventana.tabla_empleados.setItem(fila_idx, 5, QTableWidgetItem(str(empleado['fecha_nacimiento'])))
                self.ventana.tabla_empleados.setItem(fila_idx, 6, QTableWidgetItem(str(empleado['tipo'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_empleado(self):
        texto_busqueda = self.ventana.input_buscarempleado.text()
        self.cargar_empleados(texto_busqueda)

    def buscar_para_modificar_empleado(self):
        dpi_buscado = self.ventana.input_buscar_dpi_mod_empleado.text()

        if not dpi_buscado:
            QMessageBox.warning(self.ventana, "Advertencia", "Ingresa un DPI para buscar.")
            return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM empleados WHERE dpi = %s"
            cursor.execute(query, (dpi_buscado,))
            empleado = cursor.fetchone()

            if empleado:
                self.id_empleado_modificar = empleado['id']

                self.ventana.input_mod_nombre_empleado.setText(empleado['nombre'])
                self.ventana.input_mod_correo_empleado.setText(empleado['correo'])
                self.ventana.input_mod_telefono_empleado.setText(str(empleado['telefono']))
                self.ventana.input_mod_dpi_empleado.setText(empleado['dpi'])
                self.ventana.input_rol_mod.setText(empleado['tipo'])
                self.ventana.input_password_mod.setText(empleado['contraseña'])

                QMessageBox.information(self.ventana, "Encontrado", "Modifica los datos y presiona Guardar.")
            else:
                QMessageBox.warning(self.ventana, "Error", "No se encontró ningún empleado con ese DPI.")

        except Exception as e:
            print(f"Error al buscar para modificar: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def actualizar_empleado(self):
        if self.id_empleado_modificar is None:
            QMessageBox.warning(self.ventana, "Advertencia", "Primero busca un empleado para modificar.")
            return

        nuevo_nombre = self.ventana.input_mod_nombre_empleado.text()
        nuevo_correo = self.ventana.input_mod_correo_empleado.text().lower().strip()
        nuevo_telefono = self.ventana.input_mod_telefono_empleado.text()
        nuevo_dpi = self.ventana.input_mod_dpi_empleado.text()
        nuevo_rol = self.ventana.input_rol_mod.text()
        nueva_pas = self.ventana.input_password_mod.text()

        if not nuevo_nombre or not nuevo_dpi or not nuevo_correo:
            QMessageBox.warning(self.ventana, "Advertencia", "El nombre, el DPI y correo son obligatorios.")
            return
        else:
            if "@gmail.com" not in nuevo_correo and "@hotmail.com" not in nuevo_correo:
                QMessageBox.warning(self.ventana, "Advertencia", "El correo debe ser de dominio @gmail o @hotmail.")
                return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor()

            query = """
                    UPDATE empleados
                    SET nombre   = %s, \
                        correo   = %s, \
                        telefono = %s, \
                        dpi      = %s, \
                        tipo = %s, \
                        contraseña = %s
                    WHERE id = %s \
                    """
            valores = (nuevo_nombre, nuevo_correo, nuevo_telefono, nuevo_dpi, nuevo_rol, nueva_pas, self.id_empleado_modificar)

            cursor.execute(query, valores)
            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Empleado actualizado correctamente.")

            self.id_empleado_modificar = None
            self.ventana.input_buscar_dpi_mod_empleado.clear()
            self.ventana.input_mod_nombre_empleado.clear()
            self.ventana.input_mod_correo_empleado.clear()
            self.ventana.input_mod_telefono_empleado.clear()
            self.ventana.input_mod_dpi_empleado.clear()
            self.ventana.input_rol_mod.clear()
            self.ventana.input_password_mod.clear()

            self.cargar_empleados()

        except Exception as e:
            print(f"Error al actualizar: {e}")
            QMessageBox.critical(self.ventana, "Error", f"No se pudo actualizar: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()