import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel
 
 
class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QLineEdit y QLabel")
        self.resize(200, 80)
 
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedSize(50, 30)
        self.line_edit.setMaxLength(5)
        self.line_edit.move(10, 10)
 
        self.label = QLabel(self)
        self.label.setFixedSize(50, 30)
        self.label.move(10 + 50, 10)  
        self.line_edit.textChanged.connect(self.actualizar_label)
 
    def actualizar_label(self, texto):
        self.label.setText(texto)
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())