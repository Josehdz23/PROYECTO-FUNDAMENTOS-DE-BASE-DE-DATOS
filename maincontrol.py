class Principal:
    def __init__(self, ventana, rol):
        self.ventana = ventana
        self.rol = rol

        self.configurar_permisos()

    def configurar_permisos(self):
        if self.rol != "admin":
            # Ejemplo: desactivar botón eliminar
            self.ventana.btn_eliminar.setEnabled(False)