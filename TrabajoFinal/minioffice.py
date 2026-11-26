import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
)
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Word")
        self.resize(1000, 700)

        # --- Ventana y redimensionar ---
        self.editor = QTextEdit()
        self.editor.setStyleSheet(
            "QTextEdit { background: white; color: black; "
            "border: 1px solid #b0b0b0; padding: 40px 72px 40px 72px; "
            "selection-background-color: #ffa726; selection-color: black; }"
        )

        self.setCentralWidget(self.editor)

        # --- Panel Buscar y Reemplazar (izquierda, oculto al inicio) ---
        self.palabra = QLineEdit()
        self.palabra.setPlaceholderText("Texto a buscar")
        self.palabra.textChanged.connect(self.buscar_texto)
        self.palabra.returnPressed.connect(self.buscar_siguiente)
        self.editor.textChanged.connect(self.buscar_texto)

        self.boton_anterior = QPushButton("Anterior")
        self.boton_anterior.clicked.connect(self.buscar_anterior)
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.clicked.connect(self.buscar_siguiente)
        self.boton_todos = QPushButton("Todos")
        self.boton_todos.clicked.connect(self.buscar_todos)
        self.contador = QLabel("")

        self.reemplazo = QLineEdit()
        self.reemplazo.setPlaceholderText("Texto nuevo")
        self.boton_reemplazar = QPushButton("Reemplazar")
        self.boton_reemplazar.clicked.connect(self.reemplazar_texto)

        fila_navegacion = QHBoxLayout()
        fila_navegacion.addWidget(self.boton_anterior)
        fila_navegacion.addWidget(self.boton_siguiente)

        contenido_panel = QWidget()
        layout = QVBoxLayout(contenido_panel)
        layout.addWidget(QLabel("Buscar:"))
        layout.addWidget(self.palabra)
        layout.addLayout(fila_navegacion)
        layout.addWidget(self.boton_todos)
        layout.addWidget(self.contador)
        layout.addSpacing(20)
        layout.addWidget(QLabel("Reemplazar por:"))
        layout.addWidget(self.reemplazo)
        layout.addWidget(self.boton_reemplazar)
        layout.addStretch()  # empuja los controles hacia arriba

        self.panel = QDockWidget("Buscar y reemplazar", self)
        self.panel.setWidget(contenido_panel)
        self.panel.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.panel.setMinimumWidth(240)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.panel)
        self.panel.hide()
        self.panel.visibilityChanged.connect(self.cambio_panel)

        # --- Acciones ---
        self.nuevo = QAction("Nuevo", self)
        self.nuevo.setShortcut("Ctrl+N")
        self.nuevo.triggered.connect(self.nuevo_documento)

        self.abrir = QAction("Abrir...", self)
        self.abrir.setShortcut("Ctrl+O")
        self.abrir.triggered.connect(self.abrir_archivo)

        self.guardar = QAction("Guardar como...", self)
        self.guardar.setShortcut("Ctrl+S")
        self.guardar.triggered.connect(self.guardar_archivo)

        self.salir = QAction("Salir", self)
        self.salir.setShortcut("Ctrl+Q")
        self.salir.triggered.connect(self.close)

        self.deshacer = QAction("Deshacer", self)
        self.deshacer.setShortcut("Ctrl+Z")
        self.deshacer.triggered.connect(self.editor.undo)

        self.rehacer = QAction("Rehacer", self)
        self.rehacer.setShortcut("Ctrl+Y")
        self.rehacer.triggered.connect(self.editor.redo)

        self.cortar = QAction("Cortar", self)
        self.cortar.setShortcut("Ctrl+X")
        self.cortar.triggered.connect(self.editor.cut)

        self.copiar = QAction("Copiar", self)
        self.copiar.setShortcut("Ctrl+C")
        self.copiar.triggered.connect(self.editor.copy)

        self.pegar = QAction("Pegar", self)
        self.pegar.setShortcut("Ctrl+V")
        self.pegar.triggered.connect(self.editor.paste)

        self.accion_buscar = QAction("Buscar", self)
        self.accion_buscar.setShortcut("Ctrl+F")
        self.accion_buscar.triggered.connect(self.mostrar_panel)

        # Formato (acciones marcables)
        self.negrita = QAction("N", self)
        self.negrita.setToolTip("Negrita (Ctrl+B)")
        self.negrita.setCheckable(True)
        self.negrita.setShortcut("Ctrl+B")
        self.negrita.triggered.connect(self.toggle_negrita)

        self.cursiva = QAction("C", self)
        self.cursiva.setToolTip("Cursiva (Ctrl+I)")
        self.cursiva.setCheckable(True)
        self.cursiva.setShortcut("Ctrl+I")
        self.cursiva.triggered.connect(self.toggle_cursiva)

        self.subrayado = QAction("S", self)
        self.subrayado.setToolTip("Subrayado (Ctrl+U)")
        self.subrayado.setCheckable(True)
        self.subrayado.setShortcut("Ctrl+U")
        self.subrayado.triggered.connect(self.toggle_subrayado)

        self.editor.currentCharFormatChanged.connect(self.actualizar_formato)

        # --- Menús ---
        menu_archivo = self.menuBar().addMenu("Archivo")
        menu_archivo.addAction(self.nuevo)
        menu_archivo.addAction(self.abrir)
        menu_archivo.addAction(self.guardar)
        menu_archivo.addSeparator()
        menu_archivo.addAction(self.salir)

        menu_editar = self.menuBar().addMenu("Editar")
        menu_editar.addAction(self.deshacer)
        menu_editar.addAction(self.rehacer)
        menu_editar.addSeparator()
        menu_editar.addAction(self.cortar)
        menu_editar.addAction(self.copiar)
        menu_editar.addAction(self.pegar)
        menu_editar.addSeparator()
        menu_editar.addAction(self.accion_buscar)

        # --- Barra de herramientas ---
        barra = self.addToolBar("Herramientas")
        barra.setMovable(False)
        barra.addAction(self.nuevo)
        barra.addAction(self.abrir)
        barra.addAction(self.guardar)
        barra.addSeparator()
        barra.addAction(self.negrita)
        barra.addAction(self.cursiva)
        barra.addAction(self.subrayado)
        barra.addSeparator()
        barra.addAction(self.accion_buscar)

        # --- Barra de estado ---
        self.statusBar().showMessage("Listo")

    # ---------- Formato ----------
    def aplicar_formato(self, formato):
        self.editor.mergeCurrentCharFormat(formato)
        self.editor.setFocus()

    def toggle_negrita(self):
        formato = QTextCharFormat()
        formato.setFontWeight(
            QFont.Weight.Bold if self.negrita.isChecked() else QFont.Weight.Normal
        )
        self.aplicar_formato(formato)

    def toggle_cursiva(self):
        formato = QTextCharFormat()
        formato.setFontItalic(self.cursiva.isChecked())
        self.aplicar_formato(formato)

    def toggle_subrayado(self):
        formato = QTextCharFormat()
        formato.setFontUnderline(self.subrayado.isChecked())
        self.aplicar_formato(formato)

    def actualizar_formato(self, f):
        self.negrita.setChecked(f.fontWeight() >= 700)
        self.cursiva.setChecked(f.fontItalic())
        self.subrayado.setChecked(f.fontUnderline())

    def nuevo_documento(self):
        self.editor.clear()
        self.statusBar().showMessage("Documento nuevo", 3000)

    def abrir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Abrir", "", "Texto (*.txt);;HTML (*.html)"
        )
        if not ruta:
            return
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        if ruta.endswith(".html"):
            self.editor.setHtml(contenido)
        else:
            self.editor.setPlainText(contenido)
        self.statusBar().showMessage(f"Abierto: {ruta}", 3000)

    def guardar_archivo(self):
        ruta, filtro = QFileDialog.getSaveFileName(
            self, "Guardar como", "", "Texto (*.txt);;HTML (*.html)"
        )
        if not ruta:
            return
        with open(ruta, "w", encoding="utf-8") as f:
            if ruta.endswith(".html"):
                f.write(self.editor.toHtml())
            else:
                f.write(self.editor.toPlainText())
        self.statusBar().showMessage(f"Guardado: {ruta}", 3000)

    # ---------- Buscar y reemplazar ----------
    def mostrar_panel(self):
        self.panel.show()
        self.palabra.setFocus()
        self.palabra.selectAll()
        self.buscar_texto()

    def cambio_panel(self, visible):
        if visible:
            self.buscar_texto()
        else:
            self.editor.setExtraSelections([])  # quitar resaltado al cerrar

    def buscar_texto(self):
        """Resalta todas las coincidencias y actualiza el contador."""
        texto = self.palabra.text()
        if not texto or self.panel.isHidden():
            self.editor.setExtraSelections([])
            self.contador.setText("")
            return

        formato = QTextCharFormat()
        formato.setBackground(QColor("#80c8ff"))
        formato.setForeground(QColor("black"))

        selecciones = []
        resultado = self.editor.document().find(texto, 0)
        while not resultado.isNull():
            seleccion = QTextEdit.ExtraSelection()
            seleccion.cursor = resultado
            seleccion.format = formato
            selecciones.append(seleccion)
            resultado = self.editor.document().find(texto, resultado)

        self.editor.setExtraSelections(selecciones)
        self.contador.setText(f"{len(selecciones)} coincidencias")

    def buscar_siguiente(self):
        self.ir_a_coincidencia(hacia_atras=False)

    def buscar_anterior(self):
        self.ir_a_coincidencia(hacia_atras=True)

    def ir_a_coincidencia(self, hacia_atras):
        texto = self.palabra.text()
        if not texto:
            return

        documento = self.editor.document()
        opciones = QTextDocument.FindFlag(0)
        if hacia_atras:
            opciones = QTextDocument.FindFlag.FindBackward

        resultado = documento.find(texto, self.editor.textCursor(), opciones)

        if resultado.isNull():  # dar la vuelta al documento
            inicio = QTextCursor(documento)
            if hacia_atras:
                inicio.movePosition(QTextCursor.MoveOperation.End)
            resultado = documento.find(texto, inicio, opciones)

        if resultado.isNull():
            self.statusBar().showMessage("No hay coincidencias", 3000)
            return

        self.editor.setTextCursor(resultado)
        self.editor.ensureCursorVisible()

    def buscar_todos(self):
        if not self.palabra.text():
            return
        # Quitar la selección actual para que todas se vean del mismo color
        cursor = self.editor.textCursor()
        cursor.clearSelection()
        self.editor.setTextCursor(cursor)
        self.buscar_texto()

    def reemplazar_texto(self):
        texto = self.palabra.text()
        reemplazo = self.reemplazo.text()

        if not texto or not reemplazo:
            return

        cursor = self.editor.textCursor()
        # Si no hay una coincidencia seleccionada, primero se selecciona
        if cursor.selectedText().lower() != texto.lower():
            self.buscar_siguiente()
            return

        cursor.insertText(reemplazo)
        self.editor.setTextCursor(cursor)
        self.buscar_siguiente()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())