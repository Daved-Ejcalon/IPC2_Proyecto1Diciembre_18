from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QTableWidget, QFileDialog, QLineEdit, QMessageBox, QLabel, QToolTip
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

import TDA as tda
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
    
class VentanaLista(QWidget):
    def __init__(self, biblioteca, listas_reproduccion):
        super().__init__()

        self.biblioteca = biblioteca
        self.listas_reproduccion = listas_reproduccion

        color_fondo = "#BB9CC0"
        color_botones = "#67729D"
        color_texto = "#FFFFFF"
        color_hover = "#59648E"

        # Configurar la ventana del reproductor
        self.setWindowTitle('IPC MUSIC')
        self.setGeometry(200, 200, 600, 500)

        # No permitir cambiar el tamaño de la ventana
        self.setFixedSize(600, 500)

        # Agregar un icono a la ventana
        icono = QIcon("images/musica.ico")
        self.setWindowIcon(icono)

        # Configurar el color de fondo
        self.setStyleSheet(f"background-color: {color_fondo};")

        # Label 
        self.label_1 = QLabel('CREAR LISTA DE REPRODUCCIÓN', self)
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estilo del label
        self.label_1.setStyleSheet(f"font-size: 25px; color: {color_texto}; font-weight: bold;")

        # Label 
        self.label_2 = QLabel('LISTAS DE REPRODUCCIÓN', self)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estilo del label
        self.label_2.setStyleSheet(f"font-size: 25px; color: {color_texto}; font-weight: bold;")

        # Botones
        self.crear_btn = QPushButton(QIcon('images/nota.png'),'Crear lista', self)
        self.guardar_btn = QPushButton(QIcon('images/music-folder.png'),'Guardar listas', self)
        self.cargar_btn = QPushButton(QIcon('images/archivo-de-musica.png'),'Cargar listas', self)

        for boton in [self.crear_btn, self.guardar_btn, self.cargar_btn]: # Modificar botones
            boton.setFixedSize(275, 35)
            boton.setStyleSheet(f"background-color: {color_botones}; font-size: {15}px; border-radius: {5}px;")

        self.crear_btn.setFixedSize(540, 35)

        self.regresar_btn = QPushButton(QIcon('images/regresar.png'), None, self)
        self.regresar_btn.setFixedSize(35, 35)
        self.regresar_btn.setStyleSheet(f"background-color: {color_botones}; font-size: {15}px; border-radius: {5}px;")
        
        for boton in [self.crear_btn, self.regresar_btn, self.guardar_btn, self.cargar_btn]: # Modificar botones
            boton.enterEvent = lambda event, boton=boton, color_hover=color_hover: self.cambiar_estilo(boton, color_hover, 15, 5, True)
            boton.leaveEvent = lambda event, boton=boton, color_botones=color_botones: self.cambiar_estilo(boton, color_botones, 15, 5, False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Input para el nombre de la lista
        self.input_usuario = QLineEdit(self)
        self.input_usuario.setPlaceholderText('Nombre de la lista')

        # Estilo del input
        self.input_usuario.setStyleSheet(f"background-color: white; font-size: {15}px; border-radius: {5}px;")

        # Crear la tabla canciones disponibles para crear la lista
        self.tabla_canciones = QTableWidget(self)
        self.tabla_canciones.setColumnCount(4)
        self.tabla_canciones.setHorizontalHeaderLabels(['Artista', 'Album', 'Cancion', 'Agregar'])
        self.tabla_canciones.setColumnWidth(0, 130)  # Ancho de la columna 'Artista'
        self.tabla_canciones.setColumnWidth(1, 175)  # Ancho de la columna 'Album'
        self.tabla_canciones.setColumnWidth(2, 175)  # Ancho de la columna 'Cancion'

        # Ultima columna debe rellenar el espacio restante
        self.tabla_canciones.setColumnWidth(3, 50)  # Ancho de la columna 'Agregar'
        
        # No permitir que el usuario edite los datos de la tabla
        self.tabla_canciones.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Ultima fila debe rellenar el espacio restante
        self.tabla_canciones.horizontalHeader().setStretchLastSection(True)

        # Llenar la tabla con datos
        self.llenar_tabla()

        # Crear la tabla canciones disponibles para crear la lista
        self.tabla_listas = QTableWidget(self)
        self.tabla_listas.setColumnCount(3)
        self.tabla_listas.setHorizontalHeaderLabels(['Nombre', 'Canciones', 'Reproducciones'])
        self.tabla_listas.setColumnWidth(0, 175)  # Ancho de la columna 'Nombre'
        self.tabla_listas.setColumnWidth(1, 250)  # Ancho de la columna 'Canciones'

        # No permitir que el usuario edite los datos de la tabla
        self.tabla_listas.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Ultima fila debe rellenar el espacio restante
        self.tabla_listas.horizontalHeader().setStretchLastSection(True)

        # Llenar la tabla con datos
        self.llenar_tabla_listas()

        # Conectar funciones a los botones
        self.crear_btn.clicked.connect(self.crear_playlist)
        self.regresar_btn.clicked.connect(self.regresar)
        self.guardar_btn.clicked.connect(self.guardar_playlist)
        self.cargar_btn.clicked.connect(self.cargar_playlist)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Layout para los botones
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.crear_btn)
        layout_botones.addWidget(self.regresar_btn)
        layout_botones.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # LKayour para botones 2
        layout_botones_2 = QHBoxLayout()
        layout_botones_2.addWidget(self.guardar_btn)
        layout_botones_2.addWidget(self.cargar_btn)

        layout_principal.addWidget(self.label_1)
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.input_usuario)
        layout_principal.addWidget(self.tabla_canciones)
        layout_principal.addWidget(self.label_2)
        layout_principal.addLayout(layout_botones_2)
        layout_principal.addWidget(self.tabla_listas)

        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Establecer el diseño horizontal en la ventana del reproductor
        self.setLayout(layout_principal)

    # Definir las funciones para cada botón
    def llenar_tabla(self):

        # Limpiar la tabla
        self.tabla_canciones.setRowCount(0)

        for dato in self.biblioteca:
            for album in dato.datos.lista_albumes:
                for cancion in album.datos.lista_canciones:
                    # Obtener el numero de filas de la tabla
                    num_filas = self.tabla_canciones.rowCount()

                    # Insertar una nueva fila en la tabla
                    self.tabla_canciones.insertRow(num_filas)

                    # Insertar datos en la tabla
                    self.tabla_canciones.setItem(num_filas, 0, QTableWidgetItem(dato.datos.nombre))
                    self.tabla_canciones.setItem(num_filas, 1, QTableWidgetItem(album.datos.nombre))
                    self.tabla_canciones.setItem(num_filas, 2, QTableWidgetItem(cancion.datos.nombre))

                    # Agregar un checkbox en la celda correspondiente a "Guardar"
                    checkbox = QTableWidgetItem()
                    checkbox.setCheckState(Qt.CheckState.Unchecked)  # Desmarcar por defecto
                    self.tabla_canciones.setItem(num_filas, 3, checkbox)

        self.tabla_canciones.horizontalHeader().setStretchLastSection(True)

    def llenar_tabla_listas(self):

        # Limpiar la tabla
        self.tabla_listas.setRowCount(0)

        for lista_t in self.listas_reproduccion:

            # Obtener el numero de filas de la tabla
            num_filas = self.tabla_listas.rowCount()

            # Insertar una nueva fila en la tabla
            self.tabla_listas.insertRow(num_filas)

            # Insertar datos en la tabla
            self.tabla_listas.setItem(num_filas, 0, QTableWidgetItem(lista_t.nombre))
            self.tabla_listas.setItem(num_filas, 2, QTableWidgetItem(str(lista_t.reproducciones)))

            # Concatenar los nombres de las canciones
            canciones = ''
            for cancion in lista_t.contenido:
                canciones += f'{cancion.datos.nombre}, '

            # Insertar datos en la tabla
            self.tabla_listas.setItem(num_filas, 1, QTableWidgetItem(canciones[:-2]))

            # Agregar tooltip a la columna de canciones
            self.tabla_listas.item(num_filas, 1).setToolTip(canciones[:-2])
            
    def cambiar_estilo(self, boton, color, font_size, border_radius, hover=True):

        if hover:
            boton.setStyleSheet(f"background-color: {color}; font-size: {font_size+2}px; border-radius: {border_radius}px; border: 2px solid white;")
        else:
            boton.setStyleSheet(f"background-color: {color}; font-size: {font_size}px; border-radius: {border_radius}px; border: 0px;")

    def guardar_playlist(self):
        
        if len(self.listas_reproduccion) <= 0:
            QMessageBox.critical(
                self,
                "Error",
                "No se han creado listas de reproducción",
                QMessageBox.StandardButton.Ok
            )
            return
        
        xml_listas = ET.Element('ListasReproduccion')
        
        for playlist_temp in self.listas_reproduccion:
            self.crear_elemento_lista(xml_listas, playlist_temp.nombre, playlist_temp.contenido)

        tree = ET.ElementTree(xml_listas)

        #Preguntar al usuario donde guardar el archivo
        ruta = QFileDialog.getSaveFileName(self, 'Guardar archivo', '.', 'XML (*.xml)')

        with open(ruta[0], 'wb', encoding='utf-8') as file:
            xml_string = ET.tostring(xml_listas, encoding='utf-8')
            dom = minidom.parseString(xml_string)
            pretty_xml_string = dom.toprettyxml(indent='  ')
            file.write(pretty_xml_string.encode('utf-8'))

    def crear_elemento_lista(self, xml_listas, nombre_lista, lista_canciones):
        lista = ET.SubElement(xml_listas, 'Lista', {'nombre': nombre_lista})
        for cancion in lista_canciones:
            self.crear_elemento_cancion(lista, cancion)

    def crear_elemento_cancion(self, xml_lista, cancion):
        cancion_element = ET.SubElement(xml_lista, 'cancion', {'nombre': cancion.datos.nombre})
        ET.SubElement(cancion_element, 'artista').text = str(cancion.datos.artista)
        ET.SubElement(cancion_element, 'album').text = str(cancion.datos.album)
        ET.SubElement(cancion_element, 'vecesReproducida').text = str(cancion.datos.reproducciones)
        ET.SubElement(cancion_element, 'imagen').text = str(cancion.datos.imagen)
        ET.SubElement(cancion_element, 'ruta').text = str(cancion.datos.ruta)

    def cargar_playlist(self):
        try:
            #Preguntar al usuario donde guardar el archivo

            ruta = QFileDialog.getOpenFileName(self, 'Cargar listas', '.', 'XML (*.xml)')

            tree = ET.parse(ruta[0])
            root = tree.getroot()

            for lista_element in root.findall('Lista'):
                nombre_lista = lista_element.get('nombre')
                lista_playlist_temp = tda.Playlist()
                
                for cancion_element in lista_element.findall('cancion'):
                    nombre_cancion = cancion_element.get('nombre')
                    artista = cancion_element.find('artista').text
                    album = cancion_element.find('album').text
                    veces_reproducida = int(cancion_element.find('vecesReproducida').text)
                    imagen = cancion_element.find('imagen').text
                    ruta = cancion_element.find('ruta').text

                    cancion_temp = tda.Cancion(nombre_cancion, ruta, imagen, artista, album)
                    cancion_temp.reproducciones = veces_reproducida

                    # Verificar si existe el artista, sino crearlo
                    if not self.biblioteca.existe(artista):
                        self.biblioteca.agregar(artista)

                    #Verificar si existe el album, sino crearlo

                    if not self.biblioteca.get_albumes(artista).existe(album):
                        self.biblioteca.get_albumes(artista).agregar(album, imagen)
                    
                    # Verificar si la cancion existe en la biblioteca
                    if not self.biblioteca.get_cancion(artista, album, nombre_cancion):
                        self.biblioteca.get_album(artista, album).lista_canciones.agregar_cancion(cancion_temp)

                    # Verificar que el nombre de la lista no exista
                    for lista in self.listas_reproduccion:
                        if lista.nombre == nombre_lista:
                            print(f"Ya existe una lista con ese nombre: {nombre_lista}")
                            continue
                    
                    lista_playlist_temp.agregar_cancion(cancion_temp)
                
                # Verificar que se hayan seleccionado canciones
                if len(lista_playlist_temp) == 0:
                    print("Lista vacia")
                    continue

                # Registro de la lista de reproduccion
                playlist_temp = tda.Registro_Playlist(nombre_lista)
                playlist_temp.set_contenido(lista_playlist_temp)

                # Agregar la lista de reproduccion a la lista de listas de reproduccion
                self.listas_reproduccion.append(playlist_temp)

            self.llenar_tabla_listas()

        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return None
        except Exception as e:
            print(f"Error al cargar el archivo XML: {e}")
            return None

    def crear_playlist(self):
        nombre_lista = self.input_usuario.text()
        print(f'Nombre de la lista a crear: {nombre_lista}')

        # Verificar que el usuario haya ingresado un nombre
        if nombre_lista == '':
            QMessageBox.critical(
                self,
                "Error",
                "No se ha ingresado un nombre para la lista",
                QMessageBox.StandardButton.Ok
            )
            return
        
        # Verificar que el nombre de la lista no exista

        for lista in self.listas_reproduccion:
            if lista.nombre == nombre_lista:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Ya existe una lista con ese nombre",
                    QMessageBox.StandardButton.Ok
                )
                return

        lista_playlist_temp = tda.Playlist()

        # Obtener las canciones seleccionadas
        for fila in range(self.tabla_canciones.rowCount()):
            # Obtener el checkbox de la fila actual
            checkbox = self.tabla_canciones.item(fila, 3)

            # Verificar si el checkbox está marcado
            if checkbox.checkState() == Qt.CheckState.Checked:
                # Obtener los datos de la fila actual
                artista_actual = self.tabla_canciones.item(fila, 0).text()
                album_actual = self.tabla_canciones.item(fila, 1).text()
                cancion_actual = self.tabla_canciones.item(fila, 2).text()

                # Agregar la cancion a la lista de canciones seleccionadas
                cancion_temp = self.biblioteca.get_cancion(artista_actual, album_actual, cancion_actual)

                if cancion_temp != None:
                    lista_playlist_temp.agregar_cancion(cancion_temp)
                    print(f"Cancion agregada: {cancion_actual}")

        # Verificar que se hayan seleccionado canciones
        if len(lista_playlist_temp) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "No se han seleccionado canciones",
                QMessageBox.StandardButton.Ok
            )
            return

        # Registro de la lista de reproduccion
        playlist_temp = tda.Registro_Playlist(nombre_lista)
        playlist_temp.set_contenido(lista_playlist_temp)

        # Agregar la lista de reproduccion a la lista de listas de reproduccion
        self.listas_reproduccion.append(playlist_temp)

        # Actualizar la tabla
        self.llenar_tabla_listas()

        # Limpiar el input
        self.input_usuario.clear()

        # Desmarcar todas las canciones
        for fila in range(self.tabla_canciones.rowCount()):
            # Obtener el checkbox de la fila actual
            checkbox = self.tabla_canciones.item(fila, 3)

            # Desmarcar el checkbox
            checkbox.setCheckState(Qt.CheckState.Unchecked)

        # Mostrar mensaje de éxito
        QMessageBox.information(
            self,
            "Éxito",
            f"Se ha creado la lista de reproducción {nombre_lista} con éxito",
            QMessageBox.StandardButton.Ok
        )

    

    


    def regresar(self):
        # Cerrar la ventana actual
        self.close()