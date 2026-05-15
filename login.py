class Login:
    def __init__(self, ventana, auth, abrir_principal):
        self.ventana = ventana
        self.auth = auth
        self.abrir_principal = abrir_principal

        self.ventana.btn_login.clicked.connect(self.verificar_login)

    def verificar_login(self):
        print("FUNCION EJECUTADA 🔥")

        usuario = self.ventana.input_user.text()
        password = self.ventana.input_password.text()

        rol = self.auth.login(usuario, password)

        print("ROL:", rol)

        if rol:
            self.ventana.close()
            self.abrir_principal(rol)
        else:
            self.ventana.label_resultado.setText("❌ Incorrecto")