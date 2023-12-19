from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QIcon, QPixmap, QMovie
from PyQt6.QtCore import Qt, pyqtSignal
import os

import TDA as tda
    
class VentanaReproductorNormal(QWidget):
    def __init__(self, biblioteca, listas_reproduccion):
        super().__init__()

        self.biblioteca = biblioteca
        self.listas_reproduccion = listas_reproduccion

        self.playlist_actual = None
        self.cancion_repruduciendo = None
        self.reproduciendo_musica = False
        
        color_fondo = "#BB9CC0"
        color_botones = "#67729D"
        color_texto = "#FFFFFF"
        color_hover = "#59648E"

        # Configurar la ventana del reproductor
        self.setWindowTitle('IPC MUSIC')

        # No permitir cambiar el tamaño de la ventana
        self.setFixedSize(800, 350)

        # Label 
        self.label_lista = QLabel('Lista en reproducción: ', self)
        self.label_lista.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_lista.setStyleSheet(f"font-size: 15px; color: {color_texto}; font-weight: bold;")

        # Agregar un icono a la ventana
        icono = QIcon("images/musica.ico")
        self.setWindowIcon(icono)

        # Configurar el color de fondo
        self.setStyleSheet(f"background-color: {color_fondo};")

        # Crear la interfaz del reproductor

        # Botones para manejar reproduccion
        self.escoger_btn = QPushButton(QIcon('images/cursor.png'),'Escoger lista', self)
        self.regresar_btn = QPushButton(QIcon('images/regresar.png'), None, self)
        for boton in [self.escoger_btn, self.regresar_btn]: # Modificar botones
            boton.setStyleSheet(f"background-color: {color_botones}; font-size: {15}px; border-radius: {5}px;")
            boton.enterEvent = lambda event, boton=boton, color_hover=color_hover: self.cambiar_estilo(boton, color_hover, 15, 5, True)
            boton.leaveEvent = lambda event, boton=boton, color_botones=color_botones: self.cambiar_estilo(boton, color_botones, 15, 5, False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            
        self.escoger_btn.setFixedSize(400, 35)
        self.regresar_btn.setFixedSize(35, 35)

        # Botones para la musica

        self.anterior_btn = QPushButton(QIcon('images/atras.png'), None, self)
        self.play_btn = QPushButton(QIcon('images/pause_play.png'), None,self)
        self.siguiente_btn = QPushButton(QIcon('images/siguiente.png'), None,self)
        self.aleatorio_btn = QPushButton(QIcon('images/aleatorio.png'), None,self)
        for boton in [self.anterior_btn, self.play_btn, self.siguiente_btn, self.aleatorio_btn]: # Modificar botones
            boton.setFixedSize(50, 50)
            boton.setStyleSheet(f"background-color: white; font-size: {15}px; border-radius: {10}px;")
            boton.enterEvent = lambda event, boton=boton, color_hover="#DADCE4": self.cambiar_estilo(boton, color_hover, 15, 10, True)
            boton.leaveEvent = lambda event, boton=boton, color_botones="white": self.cambiar_estilo(boton, color_botones, 15, 10, False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Tooltip para los botones
        self.anterior_btn.setToolTip("Anterior canción")
        self.play_btn.setToolTip("Reproducir/Pausar canción")
        self.siguiente_btn.setToolTip("Siguiente canción")
        self.aleatorio_btn.setToolTip("Mezclar lista de reproducción")

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

        # Funcion del ecualizador
        self.actualizar_ecualizador() # Al inicio sera pausado

        # Conectar funciones a los botones
        self.escoger_btn.clicked.connect(self.escoger)
        self.regresar_btn.clicked.connect(self.regresar)

        self.anterior_btn.clicked.connect(self.anterior)
        self.play_btn.clicked.connect(self.play)
        self.siguiente_btn.clicked.connect(self.siguiente)
        self.aleatorio_btn.clicked.connect(self.aleatorio)

        # Layout principal
        layout_principal = QHBoxLayout()

        # Layout para los botones de la ventana
        layout_botones_ventana = QHBoxLayout()
        layout_botones_ventana.addWidget(self.escoger_btn)
        layout_botones_ventana.addWidget(self.regresar_btn)
        layout_botones_ventana.setContentsMargins(10, 10, 10, 10)
        layout_botones_ventana.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout para los botones del reproductor
        layout_botones_reproductor = QHBoxLayout()
        layout_botones_reproductor.addWidget(self.anterior_btn)
        layout_botones_reproductor.addWidget(self.play_btn)
        layout_botones_reproductor.addWidget(self.aleatorio_btn)
        layout_botones_reproductor.addWidget(self.siguiente_btn)
        layout_botones_reproductor.setContentsMargins(10, 15, 10, 15)

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
        layout_derecha.addWidget(self.label_lista)
        layout_derecha.addLayout(layout_botones_reproductor)
        layout_derecha.addLayout(layout_etiquetas)

        # Layout principal
        layout_principal.addLayout(layout_izquierda)
        layout_principal.addLayout(layout_derecha)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Establecer el diseño horizontal en la ventana del reproductor
        self.setLayout(layout_principal)

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
       
    def actualizar_label_lista(self, nombre_lista):
        self.label_lista.setText(f'Lista en reproducción: {nombre_lista}')

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

    def escoger(self):
        ventana_secundaria = VentanaEleccionLista(self.listas_reproduccion)
        ventana_secundaria.escoger_signal.connect(self.procesar_dato)
        ventana_secundaria.exec()
    
    def procesar_dato(self, nombre_seleccionado):
        
        if nombre_seleccionado == 'Todas':
            # Crear una copia de la lista
            self.playlist_actual = None
            
            reg_temp = tda.Registro_Playlist('Todas')
            reg_temp.reproducciones = 0

            contenido_completo = tda.Playlist()

            for ct in self.biblioteca.get_all_canciones():
                cancion_temp = tda.Cancion(ct.datos.nombre, ct.datos.ruta, ct.datos.imagen, ct.datos.artista, ct.datos.album)
                contenido_completo.agregar_cancion(cancion_temp)

            reg_temp.contenido = contenido_completo

            self.playlist_actual = reg_temp

            QMessageBox.information(
                self,
                "Escoger lista",
                f"Se ha escogido todas las canciones"
            )

            # Actualizar la etiqueta de la lista
            self.actualizar_label_lista(nombre_seleccionado)

            # Canción actual
            self.cancion_actual = None
            self.cancion_actual = self.playlist_actual.get_contenido().get_cancion_pos(0)

            # Actualizar datos de la cancion actual
            self.actualizar_datos_cancion_actual()

            return

        for reg_playlist in self.listas_reproduccion:
            if reg_playlist.nombre == nombre_seleccionado:
                
                # Crear una copia de la lista
                self.playlist_actual = None
                
                reg_temp = tda.Registro_Playlist(reg_playlist.nombre)
                reg_temp.reproducciones = reg_playlist.reproducciones
                reg_temp.contenido = reg_playlist.contenido.copy()

                self.playlist_actual = reg_temp

                print("Se creo una copia de la lista:")
                print(self.playlist_actual)

                QMessageBox.information(
                    self,
                    "Escoger lista",
                    f"Se ha escogido la lista: {nombre_seleccionado}"
                )

                # Actualizar la etiqueta de la lista
                self.actualizar_label_lista(nombre_seleccionado)

                # Canción actual
                self.cancion_actual = None
                self.cancion_actual = self.playlist_actual.get_contenido().get_cancion_pos(0)

                # Actualizar la portada
                self.actualizar_datos_cancion_actual()

                # Actualizar la lista de reproduccion
                for lista in self.listas_reproduccion:
                    if lista.nombre == nombre_seleccionado:
                        lista.aumentar_reproducciones()

                return

        # Si no se encontró la lista
        self.playlist_actual = None
        QMessageBox.critical(
            self,
            "Error",
            f"No se encontró la lista: {nombre_seleccionado}"
        )

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

    def anterior(self):
        if not self.playlist_actual:
            QMessageBox.critical(
                self,
                "Error",
                f"No se ha escogido ninguna lista de reproducción"
            )
            return
        
        # Actualizar la canción actual
        nueva_cancion = self.playlist_actual.get_contenido().get_anterior_cancion(self.cancion_actual.nombre)

        if not nueva_cancion:
            print("No se pudo obtener la cancion anterior")
            return

        self.cancion_actual = nueva_cancion
        self.reproduccion_cancion()
        # Actualizar datos de la cancion actual
        self.actualizar_datos_cancion_actual()


    def siguiente(self):
        if not self.playlist_actual:
            QMessageBox.critical(
                self,
                "Error",
                f"No se ha escogido ninguna lista de reproducción"
            )
            return

        # Actualizar la canción actual
        nueva_cancion = self.playlist_actual.get_contenido().get_siguiente_cancion(self.cancion_actual.nombre)

        if not nueva_cancion:
            print("No se pudo obtener la cancion anterior")
            return

        self.cancion_actual = nueva_cancion
        self.reproduccion_cancion()
        # Actualizar datos de la cancion actual
        self.actualizar_datos_cancion_actual()

    def aleatorio(self):
        # Mezclar la lista de reproduccion
        if self.playlist_actual:

            self.actualizar_ecualizador()

            nueva_lista = self.playlist_actual.get_contenido().mezclar()
            if not nueva_lista:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"No se pudo mezclar la lista de reproducción"
                )
                return
            
            reg_temp = tda.Registro_Playlist(self.playlist_actual.nombre)
            reg_temp.reproducciones = self.playlist_actual.reproducciones
            reg_temp.contenido = nueva_lista

            self.playlist_actual = reg_temp

            # Canción actual
            self.cancion_actual = None
            self.cancion_actual = self.playlist_actual.get_contenido().get_cancion_pos(0)

            # Actualizar la portada
            self.reproduciendo_musica = False # Parar la reproduccion
            self.actualizar_datos_cancion_actual()
            self.actualizar_ecualizador()

            QMessageBox.information(
                self,
                "Aleatorio",
                f"Se ha mezclado la lista de reproducción"
            )

            return

        # Si no se encontró la lista
        QMessageBox.critical(
            self,
            "Error",
            f"No se ha escogido ninguna lista de reproducción"
        )

       

class VentanaEleccionLista(QDialog):
    escoger_signal = pyqtSignal(str)

    def __init__(self, listas_reproduccion):
        super().__init__()

        color_fondo = "#BB9CC0"

        self.setWindowTitle('Escoger lista')
        
        # Agregar un icono a la ventana
        icono = QIcon("images/musica.ico")
        self.setWindowIcon(icono)

        # No permitir cambiar el tamaño de la ventana
        self.setFixedSize(300, 200)

        # Configurar el color de fondo
        self.setStyleSheet(f"background-color: {color_fondo};")

        # Crear la tabla
        self.tabla_listas = QTableWidget(self)
        self.tabla_listas.setColumnCount(2)
        self.tabla_listas.setHorizontalHeaderLabels(["Nombre", "Escoger"])
        self.tabla_listas.setColumnWidth(0, 150)  # Ancho de la columna 'Nombre'
        self.tabla_listas.horizontalHeader().setStretchLastSection(True)

        self.listas_reproduccion = listas_reproduccion

        # Agregar datos a la tabla
        self.actualizar_tabla()

        # Conectar la señal de clic del botón
        self.tabla_listas.cellClicked.connect(self.celda_clicada)

        # Diseño de la ventana secundaria
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabla_listas)
        self.setLayout(layout)

    def actualizar_tabla(self):
        
        #Vaciar la tabla
        self.tabla_listas.setRowCount(0)

        # Agregar primer dato de opcion de todos
        self.tabla_listas.insertRow(0)
        self.tabla_listas.setItem(0, 0, QTableWidgetItem("Todas las canciones"))
        btn_escoger = QPushButton('Escoger', self)
        btn_escoger.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_escoger.setStyleSheet(f"background-color: #67729D; font-size: {12}px")
        btn_escoger.clicked.connect(lambda _, texto='Todas': self.escoger_signal.emit(texto))
        self.tabla_listas.setCellWidget(0, 1, btn_escoger)

        # Agregar datos de las listas de reproduccion
        for playlist in self.listas_reproduccion:

            # Obtener el numero de filas de la tabla
            num_filas = self.tabla_listas.rowCount()

            # Insertar una nueva fila en la tabla
            self.tabla_listas.insertRow(num_filas)

            item_texto = QTableWidgetItem(playlist.nombre)
            btn_escoger = QPushButton( 'Escoger', self)
            btn_escoger.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_escoger.setStyleSheet(f"background-color: #67729D; font-size: {12}px")
            btn_escoger.clicked.connect(lambda _, texto=playlist.nombre: self.escoger_signal.emit(texto))

            self.tabla_listas.setItem(num_filas, 0, item_texto)
            self.tabla_listas.setCellWidget(num_filas, 1, btn_escoger)

    def celda_clicada(self, row, col):
        if col == 1:
            item_texto = self.tabla_listas.item(row, 0)
            if item_texto is not None:
                texto = item_texto.text()
                print(f"Texto seleccionado: {texto}")
                self.close()