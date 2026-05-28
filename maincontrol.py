class Principal:
    def __init__(self, ventana, rol):
        self.ventana = ventana
        self.rol = rol
        self.ventana.showMaximized()
        self.configurar_permisos()

    def configurar_permisos(self):
        if self.rol != "admin":
            self.ventana.tabWidget.removeTab(4)
            self.ventana.tabWidget.removeTab(3)
