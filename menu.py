import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import TDA as tda

import xml.etree.ElementTree as ET

from reproductor_normal import VentanaReproductorNormal
from reproductor_aleatorio import VentanaReproductorAleatorio
from crear_lista import VentanaLista

import os
import webbrowser

class VentanaMenu(QWidget):
    def __init__(self):
        super().__init__()

        # Crear una biblioteca de canciones
        self.biblioteca = tda.ListaArtistas()
        self.listas_reproduccion = []

        color_fondo = "#BB9CC0"
        color_botones = "#67729D"
        color_hover = "#59648E"
        color_texto = "#FFFFFF"

        # Configurar la ventana
        self.setWindowTitle('IPC MUSIC')

        # No permitir cambiar el tamaño de la ventana
        self.setFixedSize(500, 385)

        # Configurar el color de fondo
        self.setStyleSheet(f"background-color: {color_fondo};")

        # Agregar un icono a la ventana
        icono = QIcon("images/musica.ico")
        self.setWindowIcon(icono)

        # Label lista en reproducciopn
        label_ipc_music = QLabel('MENÚ', self)
        label_ipc_music.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_ipc_music.setStyleSheet(f"font-size: 25px; color: {color_texto}; font-weight: bold;")

        # Crear botones
        btn_cargar = QPushButton(QIcon('images/music-folder.png'),'Cargar biblioteca', self)
        btn_reproducir_normal = QPushButton(QIcon('images/ondas-sonoras.png'),'Reproductor de música normal', self)
        btn_reproducir_aleatoria = QPushButton(QIcon('images/dados.png'),'Reproductor de música aleatoria', self)
        btn_crear_lista = QPushButton(QIcon('images/notas-musicales.png'),'Listas de reproducción', self)
        btn_reporte_historial = QPushButton(QIcon('images/archivo-de-musica.png'),'Reporte música más reproducida', self)
        btn_reporte_biblioteca = QPushButton(QIcon('images/archivo-de-musica.png'),'Reporte biblioteca', self)

        for boton in [btn_cargar, btn_reproducir_normal, btn_reproducir_aleatoria, btn_crear_lista, btn_reporte_historial, btn_reporte_biblioteca]: # Modificar botones
            boton.setFixedSize(400, 45)
            boton.setStyleSheet(f"background-color: {color_botones}; font-size: {15}px; border-radius: {5}px;")
            boton.enterEvent = lambda event, boton=boton, color_hover=color_hover: self.cambiar_estilo(boton, color_hover, 15, 5, True)
            boton.leaveEvent = lambda event, boton=boton, color_botones=color_botones: self.cambiar_estilo(boton, color_botones, 15, 5, False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Conectar funciones a los botones
        btn_cargar.clicked.connect(self.cargar_biblioteca)
        btn_reproducir_normal.clicked.connect(self.reproducir)
        btn_reproducir_aleatoria.clicked.connect(self.reproducir_aleatoria)
        btn_crear_lista.clicked.connect(self.crear_lista)
        btn_reporte_historial.clicked.connect(self.reporte_historial)
        btn_reporte_biblioteca.clicked.connect(self.reporte_biblioteca)

        # Mostrar tooltips a los botones
        btn_cargar.setToolTip("Cargar una biblioteca de música")
        btn_reproducir_normal.setToolTip("Reproducir la lista de reproducción elegida")
        btn_reproducir_aleatoria.setToolTip("Reproducir toda la bilbioteca de forma aleatoria")
        btn_crear_lista.setToolTip("Modifica las listas de reproducción")
        btn_reporte_historial.setToolTip("Generar un reporte de la música más reproducida en página web")
        btn_reporte_biblioteca.setToolTip("Generar un reporte de la biblioteca en formato png")

        # Crear un diseño vertical y agregar widgets
        layout = QVBoxLayout(self)
        layout.addWidget(label_ipc_music)
        layout.addWidget(btn_cargar)
        layout.addWidget(btn_reproducir_normal)
        layout.addWidget(btn_reproducir_aleatoria)
        layout.addWidget(btn_crear_lista)
        layout.addWidget(btn_reporte_historial)
        layout.addWidget(btn_reporte_biblioteca)

        # Alinear el contenido del layout al centro
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Agregar el layout al widget
        self.setLayout(layout)

    # Definir las funciones para cada botón
    def cargar_biblioteca(self):
        try:
            """
            filename = filedialog.askopenfilename(
                initialdir="/",
                title="Select a File",
                filetypes=(("XML files", "*.xml"), ("Text files", "*.txt"))
            ) 
            """

            filename = QFileDialog.getOpenFileName(self, 'Cargar archivo xml', '.', 'XML (*.xml)')

            
            # Parsear el archivo XML
            tree = ET.parse(filename[0])
            root = tree.getroot()

            contador_canciones = 0
            # Iterar sobre las canciones
            for cancion_elem in root.findall(".//cancion"):
                nombre_cancion = cancion_elem.get("nombre")
                artista = cancion_elem.find("artista").text
                album = cancion_elem.find("album").text
                imagen = cancion_elem.find("imagen").text
                ruta = cancion_elem.find("ruta").text

                for item in [nombre_cancion, artista, album, imagen, ruta]:
                    if item is None:
                        raise Exception("Faltan datos en el archivo XML")
                    
                    if item.startswith("\"") and item.endswith("\""):
                        item = item[1:-1]

                # Agregar artista a la biblioteca
                self.biblioteca.agregar(artista)

                # Obtener la lista de albumes del artista
                lde_albumes = self.biblioteca.get_albumes(artista)

                # Agregar album a la lista de albumes
                lde_albumes.agregar(album, imagen)

                # Obtener la lista de canciones del album
                lde_canciones = lde_albumes.get_canciones(album)

                # Agregar canción a la lista de canciones

                if not lde_canciones.existe(nombre_cancion):
                    lde_canciones.agregar(nombre_cancion, ruta, imagen, artista, album)
                    contador_canciones += 1

            QMessageBox.information(self, "Carga biblioteca", f"Se ha leido {contador_canciones} canciones.")

        except:
            QMessageBox.critical(self, "Error", f"No se cargó ningún archivo.")

    def reproducir(self):
        # Verificar que la biblioteca tenga canciones
        if len(self.biblioteca) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "No hay canciones en la biblioteca",
                QMessageBox.StandardButton.Ok
            )
            return
        # Abrir la ventana del reproductor
        ventana_reproductor = VentanaReproductorNormal(self.biblioteca, self.listas_reproduccion)
        ventana_reproductor.show()

    def reproducir_aleatoria(self):
        # Verificar que la biblioteca tenga canciones
        if len(self.biblioteca) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "No hay canciones en la biblioteca",
                QMessageBox.StandardButton.Ok
            )
            return
        # Abrir la ventana del reproductor
        ventana_reproductor = VentanaReproductorAleatorio(self.biblioteca)
        ventana_reproductor.show()

    def cambiar_estilo(self, boton, color, font_size, border_radius, hover=True):

        if hover:
            boton.setStyleSheet(f"background-color: {color}; font-size: {font_size+2}px; border-radius: {border_radius}px; border: 2px solid white;")
        else:
            boton.setStyleSheet(f"background-color: {color}; font-size: {font_size}px; border-radius: {border_radius}px; border: 0px;")

    def crear_lista(self):  

        # Verificar que la biblioteca tenga canciones
        if len(self.biblioteca) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "No hay canciones en la biblioteca",
                QMessageBox.StandardButton.Ok
            )
            #return

        # Abrir la ventana de crear lista
        ventana_crear_lista = VentanaLista(self.biblioteca, self.listas_reproduccion)
        ventana_crear_lista.show()

    def reporte_historial(self):
        
        if len(self.biblioteca) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "No hay canciones en la biblioteca",
                QMessageBox.StandardButton.Ok
            )
            return

        ruta_html = "reporte_canciones/reporte.html"

        canciones_temp = self.biblioteca.get_all_canciones()

        numero_canciones = len(canciones_temp)
        if numero_canciones > 10:
            numero_canciones = 10

        top_canciones = canciones_temp.get_top_canciones(numero_canciones)

        contenido_html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Top {numero_canciones} Canciones</title>
                <link rel="icon" type="image/png" href="../images/musica.ico">
                <link rel="stylesheet" href="reporte.css">
            </head>
            <body>
                <header>
                    <h1>Top {numero_canciones} canciones más escuchadas</h1>
                </header>

            <div class="wrapper">
        """

        contador_cancion = 0
        for cancion in top_canciones:
            contador_cancion += 1
            img_cancion = "../images/nota.png"

            if cancion.datos.imagen != "" and os.path.isfile(cancion.datos.imagen):
                img_cancion = cancion.datos.imagen

            contenido_html += f"""
                <div class="cancion">
                    <img src="{img_cancion}" alt="Imagen de la canción">
                    <div class="info">
                        <h2>{cancion.datos.nombre}</h2>
                        <h3>Reproducciones: {cancion.datos.reproducciones}</h3>
                        <h3>Artista: {cancion.datos.artista}</h3>
                        <h4>Album: {cancion.datos.album}</h4>
                    </div>
                    <h1>No. {contador_cancion}</h1>
                </div>
            """

        contenido_html += """

                <!-- Repite la estructura para las otras 9 canciones -->
            </div>
            </body>
            </html>
        """

        with open(ruta_html, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_html)

        webbrowser.open(f'file://{os.path.realpath(ruta_html)}')

    def reporte_biblioteca(self):

        # Verificar que la biblioteca tenga canciones
        if len(self.biblioteca) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "No hay canciones en la biblioteca",
                QMessageBox.StandardButton.Ok
            )
            return

        self.biblioteca.graficar()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaMenu()
    ventana.show()
    sys.exit(app.exec())
