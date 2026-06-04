from PySide6.QtCore import QSize, QDate, Qt
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QListWidgetItem
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
        self.cargar_productos()
        self.cargar_invitados()
        self.cargar_carreras()
        self.cargar_eventos_en_tabla()
        self.cargar_inscripciones()
        self.cargar_proveedores()
        #self.cargar_cursos()
        self.cargar_horarios()

        # Cargar combos al iniciar
        self.cargar_datos_eventos()
        self.cargar_datos_ins()
        self.cargar_datos_cursos()

        # Conectar botones
        self.ventana.btn_agregar_alumno.clicked.connect(self.agregar_alumno_a_lista)
        self.ventana.btn_guardar_evento.clicked.connect(self.guardar_evento_completo)
        self.ventana.btn_agregar_invitado.clicked.connect(self.agregar_invitado_a_lista)

        # Estas son variables al momento de buscar para modificar
        self.id_alumno_modificar = None
        self.id_empleado_modficar = None
        self.id_producto_modificar = None

        # Botones para las modificaciones
        self.ventana.btn_buscar_mod.clicked.connect(self.buscar_para_modificar)
        self.ventana.btn_guardar_mod.clicked.connect(self.actualizar_alumno)

        self.ventana.btn_buscar_mod_empleado.clicked.connect(self.buscar_para_modificar_empleado)
        self.ventana.btn_guardar_mod_empleado.clicked.connect(self.actualizar_empleado)

        self.ventana.btn_buscar_mod_producto.clicked.connect(self.buscar_para_modificar_producto)
        self.ventana.btn_guardar_producto_mod.clicked.connect(self.actualizar_producto)

        # Botones para la limpieza
        self.ventana.btn_limpiar.clicked.connect(self.limpiar)
        self.ventana.btn_limpiar_mod.clicked.connect(self.limpiar)

        self.ventana.btn_limpiar_empleado.clicked.connect(self.limpiar)
        self.ventana.btn_limpiar_mod_empleado.clicked.connect(self.limpiar)

        self.ventana.btn_limpiar_producto.clicked.connect(self.limpiar)
        self.ventana.btn_limpiar_producto_mod.clicked.connect(self.limpiar)

        self.ventana.btn_limpiar_invitado.clicked.connect(self.limpiar)

        self.ventana.btn_limpiar_carrera.clicked.connect(self.limpiar)

        self.ventana.btn_limpiar_prov.clicked.connect(self.limpiar)

        self.ventana.btn_limpiar_curso.clicked.connect(self.limpiar)

        # Botones para guardar
        self.ventana.btn_guardar_alumno.clicked.connect(self.agregar_alumno)
        self.ventana.btn_guardar_empleado.clicked.connect(self.agregar_empleado)
        self.ventana.btn_guardar_producto.clicked.connect(self.agregar_producto)
        self.ventana.btn_guardar_invitado.clicked.connect(self.agregar_invitado)
        self.ventana.btn_guardar_carrera.clicked.connect(self.agregar_carrera)
        self.ventana.btn_guardar_ins.clicked.connect(self.agregar_inscripcion)
        self.ventana.btn_guardar_prov.clicked.connect(self.agregar_proveedor)
        self.ventana.btn_guardar_curso.clicked.connect(self.agregar_curso)
        self.ventana.btn_guardar_horario.clicked.connect(self.agregar_horario)

        # Inputs para buscar
        self.ventana.input_buscar.textChanged.connect(self.buscar_alumno)
        self.ventana.input_buscarempleado.textChanged.connect(self.buscar_empleado)
        self.ventana.input_buscarproducto.textChanged.connect(self.buscar_producto)
        self.ventana.input_buscarinvitado.textChanged.connect(self.buscar_invitado)
        self.ventana.input_buscarcarrera.textChanged.connect(self.buscar_carrera)
        self.ventana.input_buscarinscripcion.textChanged.connect(self.buscar_ins)
        self.ventana.input_buscarprov.textChanged.connect(self.buscar_proveedor)

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

        #Tab Nuevo Producto
        self.ventana.input_nombre_producto.clear()
        self.ventana.input_precio.clear()
        self.ventana.input_proveedor.clear()

        #Tab Modificar Producto
        self.ventana.input_buscar_id_mod.clear()
        self.ventana.input_nombre_producto_mod.clear()
        self.ventana.input_precio_mod.clear()
        self.ventana.input_proveedor_mod.clear()

        #Tab Nuevo Invitado
        self.ventana.input_nombre_invitado.clear()
        self.ventana.input_correo_invitado.clear()
        self.ventana.input_telefono_invitado.clear()
        self.ventana.input_dpi_invitado.clear()

        #Tab Nueva Carrera
        self.ventana.input_nombre_carrera.clear()
        self.ventana.input_precio_carrera.clear()

        #Tab Nuevo Proveedor
        self.ventana.input_nombre_prov.clear()
        self.ventana.input_correo_prov.clear()
        self.ventana.input_telefono_prov.clear()
        self.ventana.input_calle.clear()
        self.ventana.input_zona.clear()
        self.ventana.input_avenida.clear()
        self.ventana.input_nit.clear()

        #Tab Nuevo curso
        self.ventana.input_nombre_curso.clear()
        self.ventana.input_hora_inicio.clear()
        self.ventana.input_hora_fin.clear()


    def configurar_permisos(self):
        if self.rol != "admin":
            self.ventana.tabWidget.removeTab(21)
            self.ventana.tabWidget.removeTab(17)
            self.ventana.tabWidget.removeTab(13)
            self.ventana.tabWidget.removeTab(11)
            self.ventana.tabWidget.removeTab(9)
            self.ventana.tabWidget.removeTab(8)
            self.ventana.tabWidget.removeTab(6)
            self.ventana.tabWidget.removeTab(5)
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
            self.cargar_datos_eventos()

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

        if not nombre or not dpi or not correo or not telefono or not password or not tipo:
            QMessageBox.warning(self.ventana, "Advertencia", "Todos los campos son obligatorios.")
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

    # Manejo datos Productos
    def agregar_producto(self):
        nombre = self.ventana.input_nombre_producto.text()
        texto_precio = self.ventana.input_precio.text().strip()
        texto_proveedor = self.ventana.input_proveedor.text().strip()
        fecha_cad = self.ventana.input_fecha_cad.date().toString("yyyy-MM-dd")

        try:
            precio = float(texto_precio)
        except Exception as e:
            QMessageBox.warning(self.ventana, "Error", "Por favor ingresa un precio válido (solo números y punto).")
            return

        try:
            proveedor = int(texto_proveedor)
        except Exception as e:
            QMessageBox.warning(self.ventana, "Error", "Por favor ingresa un dato válido para el proveedor.")
            return

        if not nombre or not precio or not proveedor:
            QMessageBox.warning(self.ventana, "Advertencia", "El nombre, el precio y proveedor son obligatorios.")
            return

        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            query = """
                    INSERT INTO productos (nombre, precio, fecha_caducidad, proveedor)
                    VALUES (%s, %s, %s, %s) \
                    """
            valores = (nombre, precio, fecha_cad, proveedor)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Producto registrado correctamente.")

            self.ventana.input_nombre_producto.clear()
            self.ventana.input_precio.clear()
            self.ventana.input_proveedor.clear()
            self.cargar_productos()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_productos(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = "SELECT * FROM productos"
                cursor.execute(query)
            else:
                query = "SELECT * FROM productos WHERE nombre LIKE %s"
                termino = f"{busqueda}%"
                cursor.execute(query, (termino,))

            productos = cursor.fetchall()

            self.ventana.tabla_productos.setRowCount(0)

            self.ventana.tabla_productos.setColumnCount(5)
            self.ventana.tabla_productos.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Precio', 'Proveedor', 'Fecha Caducidad'])

            self.ventana.tabla_productos.setColumnWidth(0, 50)
            self.ventana.tabla_productos.setColumnWidth(2, 300)

            self.ventana.tabla_productos.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            self.ventana.tabla_productos.setColumnWidth(3, 100)
            self.ventana.tabla_productos.setColumnWidth(4, 150)

            for fila_idx, producto in enumerate(productos):
                self.ventana.tabla_productos.insertRow(fila_idx)

                self.ventana.tabla_productos.setItem(fila_idx, 0, QTableWidgetItem(str(producto['id'])))
                self.ventana.tabla_productos.setItem(fila_idx, 1, QTableWidgetItem(str(producto['nombre'])))
                self.ventana.tabla_productos.setItem(fila_idx, 2, QTableWidgetItem(str(producto['precio'])))
                self.ventana.tabla_productos.setItem(fila_idx, 3, QTableWidgetItem(str(producto['proveedor'])))
                self.ventana.tabla_productos.setItem(fila_idx, 4, QTableWidgetItem(str(producto['fecha_caducidad'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_producto(self):
        texto_busqueda = self.ventana.input_buscarproducto.text()
        self.cargar_productos(texto_busqueda)

    def buscar_para_modificar_producto(self):
        id_buscadovalidacion = self.ventana.input_buscar_id_mod.text().strip()

        try:
            id_buscado = int(id_buscadovalidacion)
        except:
            QMessageBox.warning(self.ventana, "Error", "Por favor ingresa un id válido.")
            return

        if not id_buscado:
            QMessageBox.warning(self.ventana, "Advertencia", "Ingresa un ID para buscar.")
            return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM productos WHERE id = %s"
            cursor.execute(query, (id_buscado,))
            producto = cursor.fetchone()

            if producto:
                self.id_producto_modificar = producto['id']

                self.ventana.input_nombre_producto_mod.setText(producto['nombre'])
                self.ventana.input_precio_mod.setText(str(producto['precio']))
                self.ventana.input_proveedor_mod.setText(str(producto['proveedor']))
                fecha_mysql = producto['fecha_caducidad']
                fecha_qt = QDate(fecha_mysql.year, fecha_mysql.month, fecha_mysql.day)
                self.ventana.input_fecha_cad_mod.setDate(fecha_qt)

                QMessageBox.information(self.ventana, "Encontrado", "Modifica los datos y presiona Guardar.")
            else:
                QMessageBox.warning(self.ventana, "Error", "No se encontró ningún producto con ese ID.")

        except Exception as e:
            print(f"Error al buscar para modificar: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def actualizar_producto(self):
        if self.id_producto_modificar is None:
            QMessageBox.warning(self.ventana, "Advertencia", "Primero busca un producto para modificar.")
            return

        nuevo_nombre = self.ventana.input_nombre_producto_mod.text()
        nuevo_precio = self.ventana.input_precio_mod.text()
        nuevo_proveedor = self.ventana.input_proveedor_mod.text()
        nueva_fecha_cad = self.ventana.input_fecha_cad_mod.text()

        if not nuevo_nombre or not nuevo_precio or not nuevo_proveedor:
            QMessageBox.warning(self.ventana, "Advertencia", "El nombre, el precio y proveedor son obligatorios.")
            return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor()

            query = """
                    UPDATE productos
                    SET nombre   = %s, \
                        precio   = %s, \
                        proveedor = %s, \
                        fecha_caducidad      = %s
                    WHERE id = %s \
                    """
            valores = (nuevo_nombre, nuevo_precio, nuevo_proveedor, nueva_fecha_cad, self.id_producto_modificar)

            cursor.execute(query, valores)
            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Producto actualizado correctamente.")

            self.id_producto_modificar = None
            self.ventana.input_buscar_id_mod.clear()
            self.ventana.input_nombre_producto_mod.clear()
            self.ventana.input_precio_mod.clear()
            self.ventana.input_proveedor_mod.clear()

            self.cargar_productos()

        except Exception as e:
            print(f"Error al actualizar: {e}")
            QMessageBox.critical(self.ventana, "Error", f"No se pudo actualizar: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Manejo datos Invitados
    def agregar_invitado(self):
        nombre = self.ventana.input_nombre_invitado.text()
        correo = self.ventana.input_correo_invitado.text()
        telefono = self.ventana.input_telefono_invitado.text()
        dpi = self.ventana.input_dpi_invitado.text()

        if not nombre or not dpi or not telefono or not correo:
            QMessageBox.warning(self.ventana, "Advertencia", "Todos los campos son obligatorios.")
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
                    INSERT INTO invitados (nombre, correo, telefono, dpi)
                    VALUES (%s, %s, %s, %s) \
                    """
            valores = (nombre, correo, telefono, dpi)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Invitado registrado correctamente.")

            self.ventana.input_nombre_invitado.clear()
            self.ventana.input_correo_invitado.clear()
            self.ventana.input_telefono_invitado.clear()
            self.ventana.input_dpi_invitado.clear()
            self.cargar_invitados()
            self.cargar_datos_eventos()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_invitados(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = "SELECT * FROM invitados"
                cursor.execute(query)
            else:
                query = "SELECT * FROM invitados WHERE nombre LIKE %s"
                termino = f"{busqueda}%"
                cursor.execute(query, (termino,))

            invitados = cursor.fetchall()

            self.ventana.tabla_invitados.setRowCount(0)

            self.ventana.tabla_invitados.setColumnCount(5)
            self.ventana.tabla_invitados.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Correo', 'Teléfono', 'DPI'])

            self.ventana.tabla_invitados.setColumnWidth(0, 50)
            self.ventana.tabla_invitados.setColumnWidth(1, 300)

            self.ventana.tabla_invitados.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

            self.ventana.tabla_invitados.setColumnWidth(3, 100)
            self.ventana.tabla_invitados.setColumnWidth(4, 150)

            for fila_idx, invitado in enumerate(invitados):
                self.ventana.tabla_invitados.insertRow(fila_idx)

                self.ventana.tabla_invitados.setItem(fila_idx, 0, QTableWidgetItem(str(invitado['id'])))
                self.ventana.tabla_invitados.setItem(fila_idx, 1, QTableWidgetItem(str(invitado['nombre'])))
                self.ventana.tabla_invitados.setItem(fila_idx, 2, QTableWidgetItem(str(invitado['correo'])))
                self.ventana.tabla_invitados.setItem(fila_idx, 3, QTableWidgetItem(str(invitado['telefono'])))
                self.ventana.tabla_invitados.setItem(fila_idx, 4, QTableWidgetItem(str(invitado['dpi'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_invitado(self):
        texto_busqueda = self.ventana.input_buscarinvitado.text()
        self.cargar_invitados(texto_busqueda)

    #Manejo datos Carrera
    def agregar_carrera(self):
        nombre = self.ventana.input_nombre_carrera.text()
        texto_precio = self.ventana.input_precio_carrera.text().strip()

        try:
            precio = float(texto_precio)
        except:
            QMessageBox.critical(self.ventana, "Error", "Ingrese un precio Válido.")
            return

        if not nombre or not precio:
            QMessageBox.warning(self.ventana, "Advertencia", "Todos los campos son obligatorios.")
            return

        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            query = """
                    INSERT INTO carreras (nombre, precio)
                    VALUES (%s, %s) \
                    """
            valores = (nombre, precio)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Carrera registrada correctamente.")

            self.ventana.input_nombre_carrera.clear()
            self.ventana.input_precio_carrera.clear()
            self.cargar_carreras()
            self.cargar_datos_eventos()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_carreras(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = "SELECT * FROM carreras"
                cursor.execute(query)
            else:
                query = "SELECT * FROM carreras WHERE nombre LIKE %s"
                termino = f"{busqueda}%"
                cursor.execute(query, (termino,))

            carreras = cursor.fetchall()

            self.ventana.tabla_carreras.setRowCount(0)

            self.ventana.tabla_carreras.setColumnCount(3)
            self.ventana.tabla_carreras.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Precio'])

            self.ventana.tabla_carreras.setColumnWidth(0, 50)
            self.ventana.tabla_carreras.setColumnWidth(2, 300)

            self.ventana.tabla_carreras.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            for fila_idx, carrera in enumerate(carreras):
                self.ventana.tabla_carreras.insertRow(fila_idx)

                self.ventana.tabla_carreras.setItem(fila_idx, 0, QTableWidgetItem(str(carrera['id'])))
                self.ventana.tabla_carreras.setItem(fila_idx, 1, QTableWidgetItem(str(carrera['nombre'])))
                self.ventana.tabla_carreras.setItem(fila_idx, 2, QTableWidgetItem(str(carrera['precio'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_carrera(self):
        texto_busqueda = self.ventana.input_buscarcarrera.text()
        self.cargar_carreras(texto_busqueda)

    #Manejo creación eventos
    def cargar_datos_eventos(self):
        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("SELECT id, nombre FROM carreras")
            self.ventana.combo_carrera.clear()
            for carrera in cursor.fetchall():
                self.ventana.combo_carrera.addItem(carrera['nombre'], carrera['id'])

            cursor.execute("SELECT id, nombre FROM alumnos")
            self.ventana.combo_alumnos.clear()
            for alumno in cursor.fetchall():
                self.ventana.combo_alumnos.addItem(alumno['nombre'], alumno['id'])

            cursor.execute("SELECT id, nombre FROM invitados")
            self.ventana.combo_invitados.clear()
            for invitado in cursor.fetchall():
                self.ventana.combo_invitados.addItem(invitado['nombre'], invitado['id'])

        except Exception as e:
            print(f"Error al cargar datos para eventos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_alumno_a_lista(self):
        nombre_alumno = self.ventana.combo_alumnos.currentText()
        id_alumno = self.ventana.combo_alumnos.currentData()

        if id_alumno is None:
            return

        for i in range(self.ventana.lista_alumnos_evento.count()):
            item_existente = self.ventana.lista_alumnos_evento.item(i)
            if item_existente.data(Qt.ItemDataRole.UserRole) == id_alumno:
                QMessageBox.warning(self.ventana, "Aviso", "Este alumno ya está en la lista.")
                return

        nuevo_item = QListWidgetItem(nombre_alumno)
        nuevo_item.setData(Qt.ItemDataRole.UserRole, id_alumno)

        self.ventana.lista_alumnos_evento.addItem(nuevo_item)

    def agregar_invitado_a_lista(self):
        nombre_invitado = self.ventana.combo_invitados.currentText()
        id_invitado = self.ventana.combo_invitados.currentData()

        if id_invitado is None:
            return

        for i in range(self.ventana.lista_invitados_evento.count()):
            item_existente = self.ventana.lista_invitados_evento.item(i)
            if item_existente.data(Qt.ItemDataRole.UserRole) == id_invitado:
                QMessageBox.warning(self.ventana, "Aviso", "Este invitado ya está en la lista.")
                return

        nuevo_item = QListWidgetItem(nombre_invitado)
        nuevo_item.setData(Qt.ItemDataRole.UserRole, id_invitado)

        self.ventana.lista_invitados_evento.addItem(nuevo_item)

    def guardar_evento_completo(self):
        nombre_evento = self.ventana.input_nombre_evento.text().strip()
        fecha_evento = self.ventana.input_fecha_evento.date().toString("yyyy-MM-dd")
        id_carrera = self.ventana.combo_carrera.currentData()

        if not nombre_evento or id_carrera is None:
            QMessageBox.warning(self.ventana, "Advertencia", "El nombre y la carrera son obligatorios.")
            return

        if self.ventana.lista_alumnos_evento.count() == 0 or self.ventana.lista_invitados_evento.count() == 0:
            QMessageBox.warning(self.ventana, "Advertencia",
                                "Debes tener al menos un alumno y un invitado en las listas.")
            return

        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 AS nuevo_id FROM listas_alumnos")
            nuevo_id_lista_alumnos = cursor.fetchone()['nuevo_id']

            query_lista_alumnos = "INSERT INTO listas_alumnos (id, alumno) VALUES (%s, %s)"
            for i in range(self.ventana.lista_alumnos_evento.count()):
                item = self.ventana.lista_alumnos_evento.item(i)
                id_alumno_oculto = item.data(Qt.ItemDataRole.UserRole)
                cursor.execute(query_lista_alumnos, (nuevo_id_lista_alumnos, id_alumno_oculto))

            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 AS nuevo_id FROM lista_invitados")
            nuevo_id_lista_invitados = cursor.fetchone()['nuevo_id']

            query_lista_invitados = "INSERT INTO lista_invitados (id, invitado) VALUES (%s, %s)"
            for i in range(self.ventana.lista_invitados_evento.count()):
                item = self.ventana.lista_invitados_evento.item(i)
                id_invitado_oculto = item.data(Qt.ItemDataRole.UserRole)
                cursor.execute(query_lista_invitados, (nuevo_id_lista_invitados, id_invitado_oculto))

            cursor = conexion.cursor()
            query_evento = """
                           INSERT INTO eventos (nombre, fecha, carrera, alumnos, invitados)
                           VALUES (%s, %s, %s, %s, %s) \
                           """
            valores = (nombre_evento, fecha_evento, id_carrera, nuevo_id_lista_alumnos, nuevo_id_lista_invitados)
            cursor.execute(query_evento, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito",
                                    "Evento creado con sus listas de alumnos e invitados de forma exitosa.")

            self.ventana.input_nombre_evento.clear()
            self.ventana.lista_alumnos_evento.clear()
            self.ventana.lista_invitados_evento.clear()
            self.ventana.input_fecha_evento.setDate(QDate.currentDate())
            self.cargar_eventos_en_tabla()

        except Exception as e:
            conexion.rollback()
            print(f"Error al guardar evento completo: {e}")
            QMessageBox.critical(self.ventana, "Error", f"Fallo al guardar: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_eventos_en_tabla(self):
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            query = """
                    SELECT e.id                                           AS id_evento, \
                           e.nombre                                       AS nombre_evento, \
                           e.fecha                                        AS fecha_evento, \
                           GROUP_CONCAT(DISTINCT a.nombre SEPARATOR ', ') AS alumnos_inscritos, \
                           GROUP_CONCAT(DISTINCT i.nombre SEPARATOR ', ') AS invitados_confirmados
                    FROM eventos e
                             LEFT JOIN listas_alumnos la ON e.alumnos = la.id
                             LEFT JOIN alumnos a ON la.alumno = a.id
                             LEFT JOIN lista_invitados li ON e.invitados = li.id
                             LEFT JOIN invitados i ON li.invitado = i.id
                    GROUP BY e.id; \
                    """

            cursor.execute(query)
            eventos = cursor.fetchall()

            self.ventana.tabla_eventos.setColumnCount(5)
            self.ventana.tabla_eventos.setRowCount(0)
            self.ventana.tabla_eventos.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Fecha', 'Lista Alumnos', 'Lista Invitados'])

            self.ventana.tabla_eventos.setColumnWidth(0, 10)
            self.ventana.tabla_eventos.setColumnWidth(1, 200)
            self.ventana.tabla_eventos.setColumnWidth(2, 75)
            self.ventana.tabla_eventos.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
            self.ventana.tabla_eventos.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

            for fila_idx, evento in enumerate(eventos):
                self.ventana.tabla_eventos.insertRow(fila_idx)
                for col_idx, dato in enumerate(evento):
                    valor = str(dato) if dato is not None else ""
                    item = QTableWidgetItem(valor)
                    self.ventana.tabla_eventos.setItem(fila_idx, col_idx, item)

            cursor.close()
            conexion.close()

        except Exception as e:
            print(f"Error al cargar la tabla de eventos: {e}")

    #Manejo nueva inscripcion
    def agregar_inscripcion(self):
        id_alumno = self.ventana.combo_alumnos_ins.currentData()
        id_carrera = self.ventana.combo_carrera_ins.currentData()
        fecha_ins = self.ventana.input_fecha_ins.text()

        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            query_validacion = """
                               SELECT id \
                               FROM inscripciones
                               WHERE alumno = %s \
                                 AND carrera = %s \
                               """
            cursor.execute(query_validacion, (id_alumno, id_carrera))
            duplicado = cursor.fetchone()

            if duplicado:
                QMessageBox.warning(self.ventana, "Advertencia", "¡Este alumno ya está inscrito en esta carrera!")
                return

            query_insert = """
                           INSERT INTO inscripciones (carrera, alumno, fecha)
                           VALUES (%s, %s, %s) \
                           """
            valores = (id_carrera, id_alumno, fecha_ins)

            cursor.execute(query_insert, valores)
            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Alumno inscrito correctamente.")
            self.cargar_inscripciones()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print("No se pudo guardar", e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_datos_ins(self):
        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("SELECT id, nombre FROM carreras")
            self.ventana.combo_carrera_ins.clear()
            for carrera in cursor.fetchall():
                self.ventana.combo_carrera_ins.addItem(carrera['nombre'], carrera['id'])

            cursor.execute("SELECT id, nombre FROM alumnos")
            self.ventana.combo_alumnos_ins.clear()
            for alumno in cursor.fetchall():
                self.ventana.combo_alumnos_ins.addItem(alumno['nombre'], alumno['id'])

        except Exception as e:
            print(f"Error al cargar datos para eventos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_inscripciones(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = """
                        SELECT i.id, \
                               a.nombre AS alumno, \
                               c.nombre AS carrera, \
                               i.fecha
                        FROM inscripciones i
                                 LEFT JOIN alumnos a ON i.alumno = a.id
                                 LEFT JOIN carreras c ON i.carrera = c.id \
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT i.id, \
                               a.nombre AS alumno, \
                               c.nombre AS carrera, \
                               i.fecha
                        FROM inscripciones i
                                 LEFT JOIN alumnos a ON i.alumno = a.id
                                 LEFT JOIN carreras c ON i.carrera = c.id
                        WHERE i.id LIKE %s \
                           OR a.nombre LIKE %s \
                           OR c.nombre LIKE %s \
                        """
                termino = f"%{busqueda}%"
                cursor.execute(query, (termino, termino, termino))

            inscripciones = cursor.fetchall()

            self.ventana.tabla_inscripciones.setRowCount(0)

            self.ventana.tabla_inscripciones.setColumnCount(4)
            self.ventana.tabla_inscripciones.setHorizontalHeaderLabels(
                ['ID', 'Nombre Alumno', 'Carrera', 'Fecha'])

            self.ventana.tabla_inscripciones.setColumnWidth(0, 50)
            self.ventana.tabla_inscripciones.setColumnWidth(2, 300)

            self.ventana.tabla_inscripciones.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            self.ventana.tabla_inscripciones.setColumnWidth(3, 100)

            for fila_idx, inscripcion in enumerate(inscripciones):
                self.ventana.tabla_inscripciones.insertRow(fila_idx)

                self.ventana.tabla_inscripciones.setItem(fila_idx, 0, QTableWidgetItem(str(inscripcion['id'])))
                self.ventana.tabla_inscripciones.setItem(fila_idx, 1, QTableWidgetItem(str(inscripcion['alumno'])))
                self.ventana.tabla_inscripciones.setItem(fila_idx, 2, QTableWidgetItem(str(inscripcion['carrera'])))
                self.ventana.tabla_inscripciones.setItem(fila_idx, 3, QTableWidgetItem(str(inscripcion['fecha'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_ins(self):
        texto_busqueda = self.ventana.input_buscarinscripcion.text()
        self.cargar_inscripciones(texto_busqueda)

    #Manejo nuevo proveedor
    def agregar_proveedor(self):
        nombre = self.ventana.input_nombre_prov.text()
        correo = self.ventana.input_correo_prov.text()
        telefono = self.ventana.input_telefono_prov.text()
        calle = self.ventana.input_calle.text()
        zona = self.ventana.input_zona.text()
        avenida = self.ventana.input_avenida.text()
        nit = self.ventana.input_nit.text()

        if not nombre or not nit or not correo or not telefono or not calle or not avenida or not zona:
            QMessageBox.warning(self.ventana, "Advertencia", "Todos los campos son obligatorios.")
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
                    INSERT INTO proveedores (nombre, correo, telefono, direccion_calle, direccion_zona, direccion_avenida, nit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) \
                    """
            valores = (nombre, correo, telefono, calle, zona, avenida, nit)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Proveedor registrado correctamente.")

            self.limpiar()
            self.cargar_proveedores()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_proveedores(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = "SELECT * FROM proveedores"
                cursor.execute(query)
            else:
                query = "SELECT * FROM proveedores WHERE nombre LIKE %s"
                termino = f"{busqueda}%"
                cursor.execute(query, (termino,))

            proveedores = cursor.fetchall()

            self.ventana.tabla_proveedores.setRowCount(0)

            self.ventana.tabla_proveedores.setColumnCount(8)
            self.ventana.tabla_proveedores.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Correo', 'Teléfono', 'Calle', 'Zona', 'Avenida', 'Nit'])

            self.ventana.tabla_proveedores.setColumnWidth(0, 50)
            self.ventana.tabla_proveedores.setColumnWidth(1, 100)

            self.ventana.tabla_proveedores.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

            self.ventana.tabla_proveedores.setColumnWidth(3, 100)
            self.ventana.tabla_proveedores.setColumnWidth(4, 150)
            self.ventana.tabla_proveedores.setColumnWidth(5, 100)
            self.ventana.tabla_proveedores.setColumnWidth(6, 100)
            self.ventana.tabla_proveedores.setColumnWidth(7, 100)

            for fila_idx, proveedor in enumerate(proveedores):
                self.ventana.tabla_proveedores.insertRow(fila_idx)

                self.ventana.tabla_proveedores.setItem(fila_idx, 0, QTableWidgetItem(str(proveedor['id'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 1, QTableWidgetItem(str(proveedor['nombre'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 2, QTableWidgetItem(str(proveedor['correo'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 3, QTableWidgetItem(str(proveedor['telefono'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 4, QTableWidgetItem(str(proveedor['direccion_calle'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 5, QTableWidgetItem(str(proveedor['direccion_zona'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 6, QTableWidgetItem(str(proveedor['direccion_avenida'])))
                self.ventana.tabla_proveedores.setItem(fila_idx, 7, QTableWidgetItem(str(proveedor['nit'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_proveedor(self):
        texto_busqueda = self.ventana.input_buscarprov.text()
        self.cargar_proveedores(texto_busqueda)

    #Manjeo nuevo curso
    def agregar_curso(self):
        nombre = self.ventana.input_nombre_curso.text()
        carrera = self.ventana.combo_carrera_curso.currentData()
        hora = self.ventana.combo_horario.currentData()


        if not nombre:
            QMessageBox.warning(self.ventana, "Advertencia", "Todos los campos son obligatorios.")
            return


        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            query = """
                    INSERT INTO cursos (nombre, horario, carrera)
                    VALUES (%s, %s, %s) \
                    """
            valores = (nombre, hora, carrera)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Curso registrado correctamente.")

            self.limpiar()
            #self.cargar_cursos()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_datos_cursos(self):
        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("SELECT id, nombre FROM carreras")
            self.ventana.combo_carrera_curso.clear()
            for carrera in cursor.fetchall():
                self.ventana.combo_carrera_curso.addItem(carrera['nombre'], carrera['id'])

            cursor.execute("SELECT id FROM horarios")
            self.ventana.combo_horario.clear()
            for horario in cursor.fetchall():
                self.ventana.combo_horario.addItem(str(horario['id']), horario['id'])

        except Exception as e:
            print(f"Error al cargar datos para horarios: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_horarios(self):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            query = "SELECT * FROM horarios"
            cursor.execute(query)

            horarios = cursor.fetchall()

            self.ventana.tabla_horarios.setRowCount(0)

            self.ventana.tabla_horarios.setColumnCount(3)
            self.ventana.tabla_horarios.setHorizontalHeaderLabels(
                ['ID', 'Hora Inicio', 'Hora Fin'])

            self.ventana.tabla_horarios.setColumnWidth(0, 30)
            self.ventana.tabla_horarios.setColumnWidth(1, 200)
            self.ventana.tabla_horarios.setColumnWidth(2, 200)


            for fila_idx, horario in enumerate(horarios):
                self.ventana.tabla_horarios.insertRow(fila_idx)

                self.ventana.tabla_horarios.setItem(fila_idx, 0, QTableWidgetItem(str(horario['id'])))
                self.ventana.tabla_horarios.setItem(fila_idx, 1, QTableWidgetItem(str(horario['hora_inicio'])))
                self.ventana.tabla_horarios.setItem(fila_idx, 2, QTableWidgetItem(str(horario['hora_fin'])))

        except Exception as e:
            print(f"Error al cargar la tabla: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_horario(self):
        hora_inicio = self.ventana.input_hora_inicio.text()
        hora_fin = self.ventana.input_hora_fin.text()


        if not hora_fin or not hora_inicio:
            QMessageBox.warning(self.ventana, "Advertencia", "Todos los campos son obligatorios.")
            return


        conexion = conectar()
        if conexion is None:
            QMessageBox.critical(self.ventana, "Error", "No hay conexión a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            query = """
                    INSERT INTO horarios (hora_inicio, hora_fin)
                    VALUES (%s, %s) \
                    """
            valores = (hora_inicio, hora_fin)

            cursor.execute(query, valores)

            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Horario registrado correctamente.")

            self.ventana.input_hora_inicio.clear()
            self.ventana.input_hora_fin.clear()
            self.cargar_horarios()
            self.cargar_datos_cursos()

        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")
            print(e)

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()