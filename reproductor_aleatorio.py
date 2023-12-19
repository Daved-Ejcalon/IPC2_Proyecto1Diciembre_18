from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap, QMovie
from PyQt6.QtCore import Qt
import os
import TDA as tda
import random

class VentanaReproductorAleatorio(QWidget):
    def __init__(self, biblioteca):
        super().__init__()

        self.biblioteca = biblioteca

        self.playlist_actual = None
        self.cancion_repruduciendo = None
        self.reproduciendo_musica = False
        self.pila_reproduccion = []
        
        color_fondo = "#BB9CC0"
        color_botones = "#67729D"
        color_texto = "#FFFFFF"
        color_hover = "#59648E"

        # Configurar la ventana del reproductor
        self.setWindowTitle('IPC MUSIC')

        # No permitir cambiar el tamaño de la ventana
        self.setFixedSize(600, 350)

        # Agregar un icono a la ventana
        icono = QIcon("images/musica.ico")
        self.setWindowIcon(icono)

        # Configurar el color de fondo
        self.setStyleSheet(f"background-color: {color_fondo};")

        # Crear la interfaz del reproductor

        # Botones para manejar reproduccion
        self.regresar_btn = QPushButton(QIcon('images/regresar.png'), None, self)
        self.regresar_btn.setStyleSheet(f"background-color: {color_botones}; font-size: {15}px; border-radius: {5}px;")
        self.regresar_btn.enterEvent = lambda event, boton=self.regresar_btn, color_hover=color_hover: self.cambiar_estilo(boton, color_hover, 15, 5, True)
        self.regresar_btn.leaveEvent = lambda event, boton=self.regresar_btn, color_botones=color_botones: self.cambiar_estilo(boton, color_botones, 15, 5, False)
        self.regresar_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
        self.regresar_btn.setFixedSize(35, 35)

        # Botones para la musica

        self.anterior_btn = QPushButton(QIcon('images/atras.png'), None, self)
        self.play_btn = QPushButton(QIcon('images/pause_play.png'), None,self)
        self.siguiente_btn = QPushButton(QIcon('images/siguiente.png'), None,self)
        for boton in [self.anterior_btn, self.play_btn, self.siguiente_btn]: # Modificar botones
            boton.setFixedSize(50, 50)
            boton.setStyleSheet(f"background-color: white; font-size: {15}px; border-radius: {10}px;")
            boton.enterEvent = lambda event, boton=boton, color_hover="#DADCE4": self.cambiar_estilo(boton, color_hover, 15, 10, True)
            boton.leaveEvent = lambda event, boton=boton, color_botones="white": self.cambiar_estilo(boton, color_botones, 15, 10, False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Tooltip para los botones
        self.anterior_btn.setToolTip("Anterior canción")
        self.play_btn.setToolTip("Reproducir/Pausar canción")
        self.siguiente_btn.setToolTip("Siguiente canción")

        # Datos de la cancion

        self.cancion_label = QLabel('Canción:', self)
        self.artista_label = QLabel('Artista:', self)
        self.album_label = QLabel('Álbum:', self)
        for label in [self.cancion_label, self.artista_label, self.album_label]: # Modificar etiquetas
            label.setStyleSheet(f"font-size: 15px; color: {color_texto}; font-weight: bold;")

        # Crear la imagen cuadrada
        self.label_portada = QLabel(self)
        imagen_path = 'images/nota.png'  # Reemplaza con la ruta de tu imagen cuadrada
        imagen = QPixmap(imagen_path)
        self.label_portada.setPixmap(imagen.scaledToHeight(250))
        self.label_portada.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label para el ecualizador
        self.label_equalizer = QLabel(self)
        self.label_equalizer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_equalizer.setFixedSize(250, 50)

        # Conectar funciones a los botones
        self.regresar_btn.clicked.connect(self.regresar)

        self.anterior_btn.clicked.connect(self.anterior)
        self.play_btn.clicked.connect(self.play)
        self.siguiente_btn.clicked.connect(self.siguiente)

        # Layout principal
        layout_principal = QHBoxLayout()

        # Layout para los botones de la ventana
        layout_botones_ventana = QHBoxLayout()
        layout_botones_ventana.addWidget(self.regresar_btn)
        layout_botones_ventana.setContentsMargins(10, 10, 10, 10)
        layout_botones_ventana.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Layout para los botones del reproductor
        layout_botones_reproductor = QHBoxLayout()
        layout_botones_reproductor.addWidget(self.anterior_btn)
        layout_botones_reproductor.addWidget(self.play_btn)
        layout_botones_reproductor.addWidget(self.siguiente_btn)
        layout_botones_reproductor.setContentsMargins(25, 15, 25, 15)
        layout_botones_reproductor.setSpacing(25)

        # Layout para las etiquetas
        layout_etiquetas = QVBoxLayout()
        layout_etiquetas.addWidget(self.cancion_label)
        layout_etiquetas.addWidget(self.artista_label)
        layout_etiquetas.addWidget(self.album_label)
        layout_etiquetas.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_etiquetas.setContentsMargins(10, 45, 10, 10)

        # Layout izquierda
        layout_izquierda = QVBoxLayout()
        layout_izquierda.addWidget(self.label_portada)
        layout_izquierda.addWidget(self.label_equalizer)

        # Layout derecha
        layout_derecha = QVBoxLayout()
        layout_derecha.addLayout(layout_botones_ventana)
        layout_derecha.addLayout(layout_botones_reproductor)
        layout_derecha.addLayout(layout_etiquetas)

        # Layout principal
        layout_principal.addLayout(layout_izquierda)
        layout_principal.addLayout(layout_derecha)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Establecer el diseño horizontal en la ventana del reproductor
        self.setLayout(layout_principal)

        # Funcion del ecualizador
        self.actualizar_ecualizador() # Al inicio sera pausado

        # Obtener la playlist
        self.obtener_toda_playlist() # Obtener toda la playlist

    # Definir las funciones para cada botón
    
    def actualizar_datos_cancion_actual(self):

        str_imagen = 'images/nota.png'
        str_cancion = ''
        str_artista = ''
        str_album = ''

        if self.cancion_actual:
            str_cancion = self.cancion_actual.nombre
            str_artista = self.cancion_actual.artista
            str_album = self.cancion_actual.album

            #Verificar que el archivo de la portada exista
            if os.path.isfile(self.cancion_actual.imagen):
                str_imagen = self.cancion_actual.imagen
            else:
                print(f"La ruta de la imagen no existe: {self.cancion_actual.imagen}")
        
        # Actualizar las etiquetas
        self.cancion_label.setText(f"Canción: {str_cancion}")
        self.artista_label.setText(f"Artista: {str_artista}")
        self.album_label.setText(f"Álbum: {str_album}")

        # Actualizar la portada
        imagen = QPixmap(str_imagen)
        self.label_portada.setPixmap(imagen.scaledToHeight(250))
        self.label_portada.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def actualizar_ecualizador(self):
        if self.reproduciendo_musica:
            self.movie = QMovie('images/equalizer_playing.gif')
            self.label_equalizer.setMovie(self.movie)
            self.movie.start()
        else:
            pixmap = QPixmap('images/equalizer_stop.png')
            self.label_equalizer.setPixmap(pixmap)
            self.label_equalizer.setScaledContents(True)

    def cambiar_estilo(self, boton, color, font_size, border_radius, hover=True):
        if hover:
            boton.setStyleSheet(f"background-color: {color}; font-size: {font_size+2}px; border-radius: {border_radius}px; border: 2px solid white;")
        else:
            boton.setStyleSheet(f"background-color: {color}; font-size: {font_size}px; border-radius: {border_radius}px; border: 0px;") 

    def reproduccion_cancion(self):
        # Actualizar datos de la cancion
        cancion_temp = self.biblioteca.get_cancion(self.cancion_actual.artista, self.cancion_actual.album, self.cancion_actual.nombre)
        if not cancion_temp:
            print("No se pudo obtener la cancion")

        if self.reproduciendo_musica: # Si se esta reproduciendo la musica
            cancion_temp.aumentar_reproducciones()

        self.actualizar_ecualizador()

    def regresar(self):
        # Cerrar la ventana actual
        self.close()

    def play(self):
        if self.cancion_actual:
            self.reproduciendo_musica = not self.reproduciendo_musica
            self.reproduccion_cancion()
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"No hay canción en reproducción"
            )

    def obtener_toda_playlist(self):
        reg_temp = tda.Registro_Playlist('Todas')
        reg_temp.reproducciones = 0

        contenido_completo = tda.Playlist()

        for ct in self.biblioteca.get_all_canciones():
            cancion_temp = tda.Cancion(ct.datos.nombre, ct.datos.ruta, ct.datos.imagen, ct.datos.artista, ct.datos.album)
            contenido_completo.agregar_cancion(cancion_temp)

        reg_temp.contenido = contenido_completo.mezclar()

        # Mezclar la playlist
        self.playlist_actual = reg_temp

        # Canción actual
        self.cancion_actual = None
        self.cancion_actual = self.playlist_actual.get_contenido().get_cancion_pos(0)

        # Actualizar datos de la cancion actual
        self.actualizar_datos_cancion_actual()

    def anterior(self):
        if not self.playlist_actual:
            QMessageBox.critical(
                self,
                "Error",
                f"No se ha escogido ninguna lista de reproducción"
            )
            return
        
        if len(self.pila_reproduccion) < 1: # No hay canciones anteriores
            QMessageBox.critical(
                self,
                "Error",
                f"No se puede regresar a la canción anterior"
            )
            return

        # Actualizar la canción actual
        nueva_cancion = self.pila_reproduccion.pop() # Obtener la ultima cancion de la pila

        if not nueva_cancion:
            print("No se pudo obtener la cancion anterior")
            return

        self.cancion_actual = nueva_cancion
        # Actualizar datos de la cancion actual
        self.actualizar_datos_cancion_actual()
        self.actualizar_ecualizador()

    def siguiente(self):
        if not self.playlist_actual:
            QMessageBox.critical(
                self,
                "Error",
                f"No se ha escogido ninguna lista de reproducción"
            )
            return

        # Actualizar la canción actual
        nueva_cancion = self.playlist_actual.get_contenido().get_cancion_random()
        contador_iter = 0

        while nueva_cancion == self.cancion_actual:
            nueva_cancion = self.playlist_actual.get_contenido().get_cancion_random()
            contador_iter += 1

            if contador_iter > 1000:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"No se pudo obtener la siguiente canción"
                )
                return

        if not nueva_cancion:
            print("No se pudo obtener la cancion anterior")
            return

        # Agregar la cancion anterior a la pila
        self.pila_reproduccion.append(self.cancion_actual)

        # Actualizar la cancion actual
        self.cancion_actual = nueva_cancion
        # Actualizar datos de la cancion actual
        self.actualizar_datos_cancion_actual()
        self.actualizar_ecualizador()

        