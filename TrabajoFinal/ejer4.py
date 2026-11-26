"""QT6 - 8: QDockWidget + acción compartida + ayuda contextual (QWhatsThis).

Ejecución:
    pip install PySide6
    python main.py
"""
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QLabel,
    QMainWindow,
    QTextEdit,
    QWhatsThis,
)

AYUDA = (
    "Al ejecutar esta acción, se añadirá el texto «Acción pulsada» en el dock. "
    "Se puede lanzar por Menú > Imprimir en dock, con Ctrl + P o haciendo clic "
    "en el botón correspondiente de la barra de herramientas."
)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QT6 - 8 · Dock y acciones compartidas")
        self.resize(700, 450)

        # Componente central
        central = QLabel("Componente central")
        central.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(central)

        # Dock con un QTextEdit, acoplado arriba al iniciar
        # (se mantienen las áreas permitidas por defecto: se puede mover/flotar)
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        self.dock = QDockWidget("Dock", self)
        self.dock.setWidget(self.editor)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock)

        # Una única acción compartida por menú, barra de herramientas y Ctrl+P
        self.accion_imprimir = QAction("Imprimir en dock", self)
        self.accion_imprimir.setShortcut(QKeySequence("Ctrl+P"))
        self.accion_imprimir.setToolTip("Imprimir en dock (Ctrl+P)")
        self.accion_imprimir.setWhatsThis(AYUDA)
        self.accion_imprimir.triggered.connect(self.imprimir_en_dock)

        # Menú
        menu = self.menuBar().addMenu("Menu")
        menu.addAction(self.accion_imprimir)

        # Barra de herramientas
        barra = self.addToolBar("Herramientas")
        barra.addAction(self.accion_imprimir)

        # Botón «¿Qué es esto?» (activa el modo de ayuda contextual)
        accion_ayuda = QWhatsThis.createAction(self)
        accion_ayuda.setText("¿Qué es esto?")
        accion_ayuda.setToolTip("¿Qué es esto? (Shift+F1)")
        barra.addAction(accion_ayuda)

    def imprimir_en_dock(self):
        self.editor.append("Acción pulsada")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())