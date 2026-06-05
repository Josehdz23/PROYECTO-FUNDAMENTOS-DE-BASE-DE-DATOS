from PySide6.QtCore import QSize, QDate, Qt
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QListWidgetItem
from conexion_db import conectar

class Principal:
    def __init__(self, ventana, rol):
        #Estos me inician el programa
        self.ventana = ventana
        self.rol = rol
        self.carrito = []
        self.ventana.setMaximumSize(QSize(1280, 720))
        self.ventana.setMinimumSize(QSize(1280, 720))
        self.configurar_permisos()

        #Aquí se cargan las tablas de datos
        self.cargar_alumnos()
        self.cargar_empleados()
        self.cargar_productos()
        self.cargar_invitados()
        self.cargar_carreras()
        self.cargar_eventos_en_tabla()
        self.cargar_inscripciones()
        self.cargar_proveedores()
        self.cargar_cursos()
        self.cargar_horarios()
        self.cargar_asignaciones()
        self.cargar_ventas()
        self.cargar_pagos()

        #Controlar mis inputs de asignación
        self.ventana.input_dpi_alumno.textChanged.connect(self.controlar_inputs_asignacion)
        self.ventana.input_dpi_docente.textChanged.connect(self.controlar_inputs_asignacion)

        # Cargar combos al iniciar
        self.cargar_datos_eventos()
        self.cargar_datos_ins()
        self.cargar_datos_cursos()
        self.cargar_datos_asignacion()
        self.cargar_datos_venta()
        self.cargar_combos_pagos()

        # Conectar botones
        self.ventana.btn_agregar_alumno.clicked.connect(self.agregar_alumno_a_lista)
        self.ventana.btn_guardar_evento.clicked.connect(self.guardar_evento_completo)
        self.ventana.btn_agregar_invitado.clicked.connect(self.agregar_invitado_a_lista)
        self.ventana.btn_agregar_carrito.clicked.connect(self.agregar_al_carrito)

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

        self.ventana.btn_limpiar_asignacion.clicked.connect(self.limpiar)

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
        self.ventana.btn_guardar_asignacion.clicked.connect(self.agregar_asignacion)
        self.ventana.btn_guardar_venta.clicked.connect(self.agregar_venta)
        self.ventana.btn_guardar_pago.clicked.connect(self.agregar_pago)

        # Inputs para buscar
        self.ventana.input_buscar.textChanged.connect(self.buscar_alumno)
        self.ventana.input_buscarempleado.textChanged.connect(self.buscar_empleado)
        self.ventana.input_buscarproducto.textChanged.connect(self.buscar_producto)
        self.ventana.input_buscarinvitado.textChanged.connect(self.buscar_invitado)
        self.ventana.input_buscarcarrera.textChanged.connect(self.buscar_carrera)
        self.ventana.input_buscarinscripcion.textChanged.connect(self.buscar_ins)
        self.ventana.input_buscarprov.textChanged.connect(self.buscar_proveedor)
        self.ventana.input_buscarcurso.textChanged.connect(self.buscar_curso)
        self.ventana.input_buscarasignacion.textChanged.connect(self.buscar_asignacion)
        self.ventana.input_buscarventa.textChanged.connect(self.cargar_ventas)

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

        #Tab Nueva asignación+
        self.ventana.input_dpi_docente.clear()
        self.ventana.input_dpi_alumno.clear()


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
            self.cargar_datos_venta()

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
            self.ventana.combo_carrera.addItem("Seleccione una carrera...", None)

            for carrera in cursor.fetchall():
                self.ventana.combo_carrera.addItem(carrera['nombre'], carrera['id'])

            cursor.execute("SELECT id, nombre FROM alumnos")
            self.ventana.combo_alumnos.clear()
            self.ventana.combo_alumnos.addItem("Seleccione un alumno...", None)

            for alumno in cursor.fetchall():
                self.ventana.combo_alumnos.addItem(alumno['nombre'], alumno['id'])

            cursor.execute("SELECT id, nombre FROM invitados")
            self.ventana.combo_invitados.clear()
            self.ventana.combo_invitados.addItem("Seleccione un invitado...", None)

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
            self.ventana.combo_carrera_ins.addItem("Seleccione una carrera...", None)

            for carrera in cursor.fetchall():
                self.ventana.combo_carrera_ins.addItem(carrera['nombre'], carrera['id'])

            cursor.execute("SELECT id, nombre FROM alumnos")
            self.ventana.combo_alumnos_ins.clear()
            self.ventana.combo_alumnos_ins.addItem("Seleccione un alumno...", None)

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
            self.cargar_cursos()
            self.cargar_datos_asignacion()

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
            self.ventana.combo_carrera_curso.addItem("Seleccione una carrera...", None)

            for carrera in cursor.fetchall():
                self.ventana.combo_carrera_curso.addItem(carrera['nombre'], carrera['id'])

            cursor.execute("SELECT id FROM horarios")
            self.ventana.combo_horario.clear()
            self.ventana.combo_horario.addItem("Seleccione un horario...", None)

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

    def cargar_cursos(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = """
                        SELECT c.id, \
                               c.nombre                                AS nombre_curso, \
                               CONCAT(h.hora_inicio, ', ', h.hora_fin) AS horario_completo, \
                               ca.nombre                               AS nombre_carrera
                        FROM cursos c
                                 LEFT JOIN horarios h ON c.Horario = h.id
                                 LEFT JOIN carreras ca ON c.carrera = ca.id; \
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT c.id, \
                               c.nombre                                AS nombre_curso, \
                               CONCAT(h.hora_inicio, ', ', h.hora_fin) AS horario_completo, \
                               ca.nombre                               AS nombre_carrera
                        FROM cursos c
                                 LEFT JOIN horarios h ON c.Horario = h.id
                                 LEFT JOIN carreras ca ON c.carrera = ca.id
                        WHERE c.nombre LIKE %s \
                           OR ca.nombre LIKE %s; \
                        """
                termino = f"%{busqueda}%"
                cursor.execute(query, (termino, termino))

            cursos = cursor.fetchall()

            self.ventana.tabla_cursos.setRowCount(0)
            self.ventana.tabla_cursos.setColumnCount(4)
            self.ventana.tabla_cursos.setHorizontalHeaderLabels(
                ['ID', 'Nombre', 'Horario', 'Carrera'])

            self.ventana.tabla_cursos.setColumnWidth(0, 50)
            self.ventana.tabla_cursos.setColumnWidth(1, 300)
            self.ventana.tabla_cursos.setColumnWidth(2, 300)

            self.ventana.tabla_cursos.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

            for fila_idx, curso in enumerate(cursos):
                self.ventana.tabla_cursos.insertRow(fila_idx)

                self.ventana.tabla_cursos.setItem(fila_idx, 0, QTableWidgetItem(str(curso['id'])))
                self.ventana.tabla_cursos.setItem(fila_idx, 1, QTableWidgetItem(str(curso['nombre_curso'])))
                self.ventana.tabla_cursos.setItem(fila_idx, 2, QTableWidgetItem(str(curso['horario_completo'])))
                self.ventana.tabla_cursos.setItem(fila_idx, 3, QTableWidgetItem(str(curso['nombre_carrera'])))

        except Exception as e:
            print(f"Error al cargar la tabla de cursos: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_curso(self):
        texto_busqueda = self.ventana.input_buscarcurso.text()
        self.cargar_cursos(texto_busqueda)

    #Manejo Asignación
    def controlar_inputs_asignacion(self):
        texto_alumno = self.ventana.input_dpi_alumno.text().strip()
        texto_docente = self.ventana.input_dpi_docente.text().strip()

        if texto_alumno:
            self.ventana.input_dpi_docente.setEnabled(False)
        else:
            self.ventana.input_dpi_docente.setEnabled(True)

        if texto_docente:
            self.ventana.input_dpi_alumno.setEnabled(False)
        else:
            self.ventana.input_dpi_alumno.setEnabled(True)

    def cargar_datos_asignacion(self):
        conexion = conectar()
        if conexion is None: return

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre FROM cursos")
            self.ventana.combo_cursos.clear()
            self.ventana.combo_cursos.addItem("Seleccione un curso...", None)

            for curso in cursor.fetchall():
                self.ventana.combo_cursos.addItem(curso['nombre'], curso['id'])

        except Exception as e:
            print(f"Error al cargar datos para horarios: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_asignacion(self):
        dpi_alumno = self.ventana.input_dpi_alumno.text().strip()
        dpi_docente = self.ventana.input_dpi_docente.text().strip()
        id_curso = self.ventana.combo_cursos.currentData()

        if not dpi_alumno and not dpi_docente:
            QMessageBox.warning(self.ventana, "Advertencia", "Debes ingresar el DPI de un alumno o de un docente.")
            return

        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)
            id_alumno_real = None
            id_docente_real = None

            if dpi_alumno:
                cursor.execute("SELECT id FROM alumnos WHERE dpi = %s", (dpi_alumno,))
                resultado = cursor.fetchone()
                if not resultado:
                    QMessageBox.critical(self.ventana, "Error", "No existe ningún alumno con ese DPI.")
                    return
                id_alumno_real = resultado['id']

                cursor.execute("SELECT id FROM asignaciones WHERE curso = %s AND alumno = %s",
                               (id_curso, id_alumno_real))
                if cursor.fetchone():
                    QMessageBox.warning(self.ventana, "Advertencia",
                                        "¡Este alumno ya se encuentra asignado a este curso!")
                    return

            elif dpi_docente:
                cursor.execute("SELECT id FROM empleados WHERE dpi = %s AND tipo = 'docente'", (dpi_docente,))
                resultado = cursor.fetchone()
                if not resultado:
                    QMessageBox.critical(self.ventana, "Error", "El DPI no existe o el empleado NO es un docente.")
                    return
                id_docente_real = resultado['id']

                cursor.execute("SELECT id FROM asignaciones WHERE curso = %s AND docente = %s",
                               (id_curso, id_docente_real))
                if cursor.fetchone():
                    QMessageBox.warning(self.ventana, "Advertencia", "¡Este docente ya está a cargo de este curso!")
                    return

            query_insert = """
                           INSERT INTO asignaciones (curso, alumno, docente)
                           VALUES (%s, %s, %s) \
                           """
            cursor.execute(query_insert, (id_curso, id_alumno_real, id_docente_real))
            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito", "Asignación registrada correctamente.")

            self.ventana.input_dpi_alumno.clear()
            self.ventana.input_dpi_docente.clear()
            self.cargar_asignaciones()


        except Exception as e:
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_asignaciones(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = """
                        SELECT asig.id, \
                               cu.nombre AS nombre_curso, \
                               al.nombre AS nombre_alumno, \
                               em.nombre AS nombre_docente
                        FROM asignaciones asig
                                 LEFT JOIN cursos cu ON asig.curso = cu.id
                                 LEFT JOIN alumnos al ON asig.alumno = al.id
                                 LEFT JOIN empleados em ON asig.docente = em.id \
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT asig.id, \
                               cu.nombre AS nombre_curso, \
                               al.nombre AS nombre_alumno, \
                               em.nombre AS nombre_docente
                        FROM asignaciones asig
                                 LEFT JOIN cursos cu ON asig.curso = cu.id
                                 LEFT JOIN alumnos al ON asig.alumno = al.id
                                 LEFT JOIN empleados em ON asig.docente = em.id
                        WHERE cu.nombre LIKE %s
                           OR al.nombre LIKE %s
                           OR em.nombre LIKE %s \
                        """
                termino = f"%{busqueda}%"
                cursor.execute(query, (termino, termino, termino))

            asignaciones = cursor.fetchall()

            self.ventana.tabla_asignaciones.setRowCount(0)
            self.ventana.tabla_asignaciones.setColumnCount(4)
            self.ventana.tabla_asignaciones.setHorizontalHeaderLabels(
                ['ID', 'Curso', 'Alumno Asignado', 'Docente a Cargo'])

            self.ventana.tabla_asignaciones.setColumnWidth(0, 50)
            self.ventana.tabla_asignaciones.setColumnWidth(2, 250)
            self.ventana.tabla_asignaciones.setColumnWidth(3, 250)

            self.ventana.tabla_asignaciones.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

            for fila_idx, asig in enumerate(asignaciones):
                self.ventana.tabla_asignaciones.insertRow(fila_idx)

                alumno_texto = asig['nombre_alumno'] if asig['nombre_alumno'] else "-"
                docente_texto = asig['nombre_docente'] if asig['nombre_docente'] else "-"

                self.ventana.tabla_asignaciones.setItem(fila_idx, 0, QTableWidgetItem(str(asig['id'])))
                self.ventana.tabla_asignaciones.setItem(fila_idx, 1, QTableWidgetItem(str(asig['nombre_curso'])))
                self.ventana.tabla_asignaciones.setItem(fila_idx, 2, QTableWidgetItem(str(alumno_texto)))
                self.ventana.tabla_asignaciones.setItem(fila_idx, 3, QTableWidgetItem(str(docente_texto)))

        except Exception as e:
            print(f"Error al cargar la tabla de asignaciones: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_asignacion(self):
        texto_busqueda = self.ventana.input_buscarasignacion.text()
        self.cargar_asignaciones(texto_busqueda)

    #Manejo para la venta
    def agregar_al_carrito(self):
        id_producto = self.ventana.combo_productos.currentData()
        nombre_producto = self.ventana.combo_productos.currentText()

        if not id_producto:
            QMessageBox.warning(self.ventana, "Advertencia", "Selecciona un producto válido.")
            return

        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT precio FROM productos WHERE id = %s", (id_producto,))
            resultado = cursor.fetchone()

            if resultado:
                precio = float(resultado['precio'])

                self.carrito.append({'id_producto': id_producto, 'precio': precio, 'nombre': nombre_producto})

                texto_pantalla = f"{nombre_producto} - Q{precio:.2f}"
                self.ventana.lista_carrito.addItem(texto_pantalla)

                total_actual = sum(item['precio'] for item in self.carrito)
                self.ventana.lbl_total_venta.setText(f"Total: Q{total_actual:.2f}")

        except Exception as e:
            print(f"Error al agregar al carrito: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_venta(self):
        if not self.carrito:
            QMessageBox.warning(self.ventana, "Advertencia", "El carrito está vacío.")
            return

        dpi_cliente = self.ventana.input_dpi_cliente.text().strip()

        if not dpi_cliente:
            QMessageBox.warning(self.ventana, "Advertencia", "Debes ingresar el DPI del alumno (cliente).")
            return

        total_venta = sum(item['precio'] for item in self.carrito)
        fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")

        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("SELECT id FROM alumnos WHERE dpi = %s", (dpi_cliente,))
            resultado_cliente = cursor.fetchone()

            if not resultado_cliente:
                QMessageBox.critical(self.ventana, "Error", "No existe ningún alumno con ese DPI registrado.")
                return

            id_cliente_real = resultado_cliente['id']

            query_venta = "INSERT INTO ventas (cliente, total, fecha) VALUES (%s, %s, %s)"
            cursor.execute(query_venta, (id_cliente_real, total_venta, fecha_actual))

            id_nueva_venta = cursor.lastrowid

            query_detalle = "INSERT INTO detalle_venta (venta_id, producto, subtotal) VALUES (%s, %s, %s)"
            for item in self.carrito:
                cursor.execute(query_detalle, (id_nueva_venta, item['id_producto'], item['precio']))

            conexion.commit()
            QMessageBox.information(self.ventana, "Éxito", "Venta registrada y asignada al alumno correctamente.")

            self.carrito.clear()
            self.ventana.lista_carrito.clear()
            self.ventana.lbl_total_venta.setText("Total: Q0.00")
            self.ventana.input_dpi_cliente.clear()
            self.cargar_ventas()

        except Exception as e:
            conexion.rollback()
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar la venta: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_datos_venta(self):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre FROM productos")
            productos = cursor.fetchall()

            self.ventana.combo_productos.clear()

            self.ventana.combo_productos.addItem("Seleccione un producto...", None)

            for prod in productos:
                self.ventana.combo_productos.addItem(prod['nombre'], prod['id'])

        except Exception as e:
            print(f"Error al cargar los productos: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_ventas(self, busqueda=""):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            if busqueda == "":
                query = """
                        SELECT v.id, \
                               a.nombre AS nombre_cliente, \
                               v.total, \
                               v.fecha
                        FROM ventas v
                                 LEFT JOIN alumnos a ON v.cliente = a.id \
                        """
                cursor.execute(query)
            else:
                query = """
                        SELECT v.id, \
                               a.nombre AS nombre_cliente, \
                               v.total, \
                               v.fecha
                        FROM ventas v
                                 LEFT JOIN alumnos a ON v.cliente = a.id
                        WHERE a.nombre LIKE %s \
                        """
                termino = f"%{busqueda}%"
                cursor.execute(query, (termino,))

            ventas = cursor.fetchall()

            self.ventana.tabla_ventas.setRowCount(0)
            self.ventana.tabla_ventas.setColumnCount(4)
            self.ventana.tabla_ventas.setHorizontalHeaderLabels(
                ['ID Venta', 'Cliente', 'Total', 'Fecha'])

            self.ventana.tabla_ventas.setColumnWidth(0, 80)
            self.ventana.tabla_ventas.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.ventana.tabla_ventas.setColumnWidth(2, 120)
            self.ventana.tabla_ventas.setColumnWidth(3, 100)

            for fila_idx, venta in enumerate(ventas):
                self.ventana.tabla_ventas.insertRow(fila_idx)

                cliente_texto = venta['nombre_cliente'] if venta['nombre_cliente'] else "Cliente General"

                total_formateado = f"Q{float(venta['total']):.2f}"

                self.ventana.tabla_ventas.setItem(fila_idx, 0, QTableWidgetItem(str(venta['id'])))
                self.ventana.tabla_ventas.setItem(fila_idx, 1, QTableWidgetItem(str(cliente_texto)))
                self.ventana.tabla_ventas.setItem(fila_idx, 2, QTableWidgetItem(total_formateado))
                self.ventana.tabla_ventas.setItem(fila_idx, 3, QTableWidgetItem(str(venta['fecha'])))

        except Exception as e:
            print(f"Error al cargar la tabla de ventas: {e}")

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_venta(self):
        texto_busqueda = self.ventana.input_buscarventa.text()
        self.cargar_ventas(texto_busqueda)

    #Manejo para los pagos
    def cargar_combos_pagos(self):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                           SELECT i.id, a.nombre
                           FROM inscripciones i
                                    LEFT JOIN alumnos a ON i.alumno = a.id
                           """)
            inscripciones = cursor.fetchall()

            self.ventana.combo_inscripcion.clear()
            self.ventana.combo_inscripcion.addItem("Ninguna...", None)  # Opción por defecto

            for ins in inscripciones:
                texto = f"Insc #{ins['id']} - {ins['nombre']}"
                self.ventana.combo_inscripcion.addItem(texto, ins['id'])

            cursor.execute("""
                           SELECT v.id, a.nombre, v.total
                           FROM ventas v
                                    LEFT JOIN alumnos a ON v.cliente = a.id
                           """)
            ventas = cursor.fetchall()

            self.ventana.combo_venta.clear()
            self.ventana.combo_venta.addItem("Ninguna...", None)

            for v in ventas:
                texto = f"Venta #{v['id']} - {v['nombre']} (Q{v['total']})"
                self.ventana.combo_venta.addItem(texto, v['id'])

        except Exception as e:
            print(f"Error al cargar combos de pago: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def agregar_pago(self):
        id_inscripcion = self.ventana.combo_inscripcion.currentData()
        id_venta = self.ventana.combo_venta.currentData()

        if not id_inscripcion and not id_venta:
            QMessageBox.warning(self.ventana, "Advertencia",
                                "Debes seleccionar al menos una inscripción o una venta para registrar el pago.")
            return

        fecha_actual = QDate.currentDate().toString("yyyy-MM-dd")

        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)
            monto_total_calculado = 0.0

            if id_inscripcion:
                query_insc = """
                             SELECT c.precio
                             FROM inscripciones i
                                      JOIN carreras c ON i.carrera = c.id
                             WHERE i.id = %s \
                             """
                cursor.execute(query_insc, (id_inscripcion,))
                resultado_insc = cursor.fetchone()

                if resultado_insc and resultado_insc['precio']:
                    monto_total_calculado += float(resultado_insc['precio'])

            if id_venta:
                query_venta = "SELECT total FROM ventas WHERE id = %s"
                cursor.execute(query_venta, (id_venta,))
                resultado_venta = cursor.fetchone()

                if resultado_venta and resultado_venta['total']:
                    monto_total_calculado += float(resultado_venta['total'])

            query_pago = """
                         INSERT INTO pagos (inscripcion, venta, fecha, Monto)
                         VALUES (%s, %s, %s, %s) \
                         """
            cursor.execute(query_pago, (id_inscripcion, id_venta, fecha_actual, monto_total_calculado))
            conexion.commit()

            QMessageBox.information(self.ventana, "Éxito",
                                    f"Pago registrado correctamente por un total de Q{monto_total_calculado:.2f}.")

            self.ventana.combo_inscripcion.setCurrentIndex(0)
            self.ventana.combo_venta.setCurrentIndex(0)

            self.cargar_pagos()

        except Exception as e:
            conexion.rollback()
            QMessageBox.critical(self.ventana, "Error", f"No se pudo guardar el pago: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def cargar_pagos(self):
        conexion = conectar()
        if conexion is None:
            return

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, inscripcion, venta, fecha, Monto FROM pagos")
            pagos = cursor.fetchall()

            self.ventana.tabla_pagos.setRowCount(0)
            self.ventana.tabla_pagos.setColumnCount(5)
            self.ventana.tabla_pagos.setHorizontalHeaderLabels(
                ['ID Pago', 'ID Inscripción', 'ID Venta', 'Fecha', 'Monto'])

            self.ventana.tabla_pagos.setColumnWidth(0, 70)
            self.ventana.tabla_pagos.setColumnWidth(1, 120)
            self.ventana.tabla_pagos.setColumnWidth(2, 120)
            self.ventana.tabla_pagos.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

            for fila_idx, pago in enumerate(pagos):
                self.ventana.tabla_pagos.insertRow(fila_idx)

                insc_texto = str(pago['inscripcion']) if pago['inscripcion'] else "-"
                venta_texto = str(pago['venta']) if pago['venta'] else "-"
                monto_formateado = f"Q{float(pago['Monto']):.2f}"

                self.ventana.tabla_pagos.setItem(fila_idx, 0, QTableWidgetItem(str(pago['id'])))
                self.ventana.tabla_pagos.setItem(fila_idx, 1, QTableWidgetItem(insc_texto))
                self.ventana.tabla_pagos.setItem(fila_idx, 2, QTableWidgetItem(venta_texto))
                self.ventana.tabla_pagos.setItem(fila_idx, 3, QTableWidgetItem(str(pago['fecha'])))
                self.ventana.tabla_pagos.setItem(fila_idx, 4, QTableWidgetItem(monto_formateado))

        except Exception as e:
            print(f"Error al cargar la tabla de pagos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()