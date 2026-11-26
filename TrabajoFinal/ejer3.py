import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QGridLayout, QPushButton


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(200, 50)

        layout = QGridLayout(self)
        self.setGeometry(100, 100, 300, 100)

        self.usuario = QLabel("Usuario:")
        layout.addWidget(self.usuario, 0, 0)

        self.inputUsuario = QLineEdit()
        layout.addWidget(self.inputUsuario, 0, 1)
        self.inputUsuario.setPlaceholderText("Ingrese su usuario")

        self.contraseña = QLabel("Contraseña:")
        layout.addWidget(self.contraseña, 1, 0)

        self.inputContraseña = QLineEdit()
        layout.addWidget(self.inputContraseña, 1, 1)
        self.inputContraseña.setPlaceholderText("Ingrese su contraseña")
        self.inputContraseña.setEchoMode(QLineEdit.Password)

        self.boton = QPushButton("Iniciar sesión")
        layout.addWidget(self.boton, 2, 0, 1, 2)

        self.label = QLabel("")
        layout.addWidget(self.label, 3, 0, 1, 2)

        self.boton.clicked.connect(self.comprobarCredenciales)

    def comprobarCredenciales(self):
        usuario = self.inputUsuario.text()
        contraseña = self.inputContraseña.text()

        if usuario == "admin" and contraseña == "admin":
            self.label.setText("Inicio de sesión exitoso")
        else:
            self.label.setText("Usuario o contraseña incorrectos")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())