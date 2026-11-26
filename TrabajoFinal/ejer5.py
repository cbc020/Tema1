import sys
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QColor, QFont, QTextCharFormat
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class BotonHover(QPushButton):
    hover = Signal()

    def enterEvent(self, event):
        self.hover.emit()
        super().enterEvent(event)


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi bloc de notas")
        self.resize(900, 500)

        central = QWidget()
        self.setCentralWidget(central)

        self.archivo = QPushButton("Archivo")
        self.formato = QPushButton("Formato")
        self.editar = BotonHover("Editar")
        self.btnNegrita = QPushButton("N")
        self.boton4 = QPushButton("C")
        self.boton5 = QPushButton("S")
        self.boton6 = QPushButton("Nuevo")
        self.boton7 = QPushButton("Insertar palabra")
        self.editor = QTextEdit()

        self.menu_editar = QMenu(self)

        self.deshacer = QAction("Deshacer", self)
        self.deshacer.triggered.connect(self.editor.undo)
        self.deshacer.setShortcut("Ctrl+Z")

        self.rehacer = QAction("Rehacer", self)
        self.rehacer.triggered.connect(self.editor.redo)
        self.rehacer.setShortcut("Ctrl+Y")

        self.cortar = QAction("Cortar", self)
        self.cortar.triggered.connect(self.editor.cut)
        self.cortar.setShortcut("Ctrl+X")

        self.copiar = QAction("Copiar", self)
        self.copiar.triggered.connect(self.editor.copy)
        self.copiar.setShortcut("Ctrl+C")

        self.pegar = QAction("Pegar", self)
        self.pegar.triggered.connect(self.editor.paste)
        self.pegar.setShortcut("Ctrl+V")

        # Negrita
        self.btnNegrita.setCheckable(True)
        self.btnNegrita.setShortcut("Ctrl+B")
        self.btnNegrita.clicked.connect(self.toggle_negrita)
        # El botón se marca solo según el texto donde esté el cursor
        self.editor.currentCharFormatChanged.connect(
            lambda f: self.btnNegrita.setChecked(f.fontWeight() >= 700)
        )

        self.menu_editar.addAction(self.deshacer)
        self.menu_editar.addAction(self.rehacer)
        self.menu_editar.addAction(self.cortar)
        self.menu_editar.addAction(self.copiar)
        self.menu_editar.addAction(self.pegar)

        self.editar.hover.connect(self.mostrar_menu_editar)

        self.buscar = QLabel("Buscar:")
        self.palabra = QLineEdit()
        self.palabra.setPlaceholderText("Texto a buscar")
        self.palabra.textChanged.connect(self.buscar_texto)
        self.editor.textChanged.connect(self.buscar_texto)

        self.reemplazar = QLabel("Reemplazar:")
        self.reemplazo = QLineEdit()
        self.reemplazo.setPlaceholderText("Texto nuevo")
        self.boton7.clicked.connect(self.reemplazar_texto)

        grupo_1 = QHBoxLayout()
        grupo_1.addWidget(self.archivo)
        grupo_1.addWidget(self.formato)
        grupo_1.addWidget(self.editar)

        grupo_2 = QHBoxLayout()
        grupo_2.addWidget(self.btnNegrita)
        grupo_2.addWidget(self.boton4)
        grupo_2.addWidget(self.boton5)
        grupo_2.addWidget(self.boton6)

        grupo_3 = QVBoxLayout()
        grupo_3.addLayout(grupo_1)
        grupo_3.addLayout(grupo_2)

        fila_buscar = QHBoxLayout()
        fila_buscar.addWidget(self.buscar)
        fila_buscar.addWidget(self.palabra)

        fila_reemplazar = QHBoxLayout()
        fila_reemplazar.addWidget(self.reemplazar)
        fila_reemplazar.addWidget(self.reemplazo)
        fila_reemplazar.addWidget(self.boton7)

        grupo_4 = QVBoxLayout()
        grupo_4.addLayout(fila_buscar)
        grupo_4.addLayout(fila_reemplazar)

        contenido = QHBoxLayout()
        contenido.addWidget(self.editor, 3)
        contenido.addLayout(grupo_4, 1)

        layout = QVBoxLayout(central)
        layout.addLayout(grupo_3)
        layout.addLayout(contenido)

    def toggle_negrita(self):
        formato = QTextCharFormat()
        if self.btnNegrita.isChecked():
            formato.setFontWeight(QFont.Weight.Bold)
        else:
            formato.setFontWeight(QFont.Weight.Normal)
        self.editor.mergeCurrentCharFormat(formato)
        self.editor.setFocus()

    def buscar_texto(self):
        texto = self.palabra.text()
        if not texto:
            self.editor.setExtraSelections([])
            return

        formato = QTextCharFormat()
        formato.setBackground(QColor("#80c8ff"))
        formato.setForeground(QColor("black"))

        selecciones = []
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)

        while True:
            resultado = self.editor.document().find(texto, cursor)
            if resultado.isNull():
                break

            seleccion = QTextEdit.ExtraSelection()
            seleccion.cursor = resultado
            seleccion.format = formato
            selecciones.append(seleccion)

            cursor.setPosition(resultado.selectionEnd())

        self.editor.setExtraSelections(selecciones)

    def reemplazar_texto(self):
        texto = self.palabra.text()
        reemplazo = self.reemplazo.text()

        if not texto or not reemplazo:
            return

        cursor = self.editor.textCursor()
        resultado = self.editor.document().find(texto, cursor)

        if resultado.isNull():
            return

        self.editor.setTextCursor(resultado)
        self.editor.textCursor().insertText(reemplazo)

    def mostrar_menu_editar(self):
        posicion = self.editar.mapToGlobal(self.editar.rect().bottomLeft())
        self.menu_editar.popup(posicion)    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())