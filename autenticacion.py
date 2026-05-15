class Auth:
    def login(self, usuario, password):
        if usuario == "admin" and password == "1234":
            return "admin"
        elif usuario == "user" and password == "1234":
            return "user"
        return None