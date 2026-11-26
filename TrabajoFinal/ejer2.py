

import sys
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ponte a prueba 2")
        self.resize(200, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.combo = QComboBox(self)

        meses = [
            "Meses del año", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
            "Diciembre",
        ]
        self.combo.addItems(meses)

        layout.addWidget(self.combo)

        self.combo.currentIndexChanged.connect(self.mostrar_mes)

    def mostrar_mes(self, index):
        texto = self.combo.currentText()
        if index == 0:
            return  
        print(f"{texto} es el mes número {index}.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())