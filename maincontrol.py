class Principal:
    def __init__(self, ventana, rol):
        self.ventana = ventana
        self.rol = rol
        self.ventana.showMaximized()
        self.configurar_permisos()

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