from graphviz import Digraph
from tkinter import filedialog
import random

# Objetos
class Artista:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_albumes = ListaAlbumes()

    def __str__(self):
        salida = f"Artista: {self.nombre}\n"
        salida += "Albumes:\n"
        salida += str(self.lista_albumes)
        return salida

class Album:
    def __init__(self, nombre, imagen):
        self.nombre = nombre
        self.imagen = imagen
        self.lista_canciones = ListaCanciones()
    
    def __str__(self):
        salida = f"Album: {self.nombre}, Imagen: {self.imagen}\n"
        salida += f"Canciones:\n"
        salida += str(self.lista_canciones)
        return salida

class Cancion:
    def __init__(self, nombre, ruta, imagen, artista, album):
        self.nombre = nombre
        self.ruta = ruta
        self.imagen = imagen
        self.album = album
        self.artista = artista
        self.reproducciones = 0 # Numero de veces que se ha reproducido la cancion

    def aumentar_reproducciones(self):

        print(f"Aumentando reproducciones de {self.nombre}...")

        self.reproducciones += 1
    
    def resetear_reproducciones(self):
        self.reproducciones = 0
    
    def __str__(self):
        return f"Cancion: {self.nombre}, Album: {self.album}, Artista: {self.artista}, Reproducciones: {self.reproducciones}\n\tRuta: {self.ruta}\n\tImagen: {self.imagen}"

class Registro_Playlist: 
    def __init__(self, nombre):
        self.nombre = nombre
        self.reproducciones = 0 # Numero de veces que se ha reproducido la playlist
        self.contenido = Playlist() # Lista doblemente enlazada circular

    def aumentar_reproducciones(self):
        self.reproducciones += 1
    
    def resetear_reproducciones(self):
        self.reproducciones = 0

    def set_contenido(self, contenido): # Recibe un objeto de tipo cancion
        self.contenido = contenido.copy()
    
    def get_contenido(self):
        return self.contenido

    def __str__(self):
        return f"Playlist: {self.nombre}, Reproducciones: {self.reproducciones}\n{self.contenido}"

# Listas

class Nodo:
    def __init__(self, datos):
        self.datos = datos
        self.siguiente = None
        self.anterior = None
    
    def __str__(self):
        return f"Nodo: {self.datos}"

# Lista doblemente enlazada

class ListaDobleEnlazada:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def agregar_nodo_al_final(self, nodo):
        if self.inicio is None:
            self.inicio = nodo
            self.fin = nodo
        else:
            nodo.anterior = self.fin
            self.fin.siguiente = nodo
            self.fin = nodo
    
    def agregar_nodo_al_inicio(self, nodo):
        if self.inicio is None:
            self.inicio = nodo
            self.fin = nodo
        else:
            nodo.siguiente = self.inicio
            self.inicio.anterior = nodo
            self.inicio = nodo

    def expandir(self, ListaDobleEnlazada):
        for nodo in ListaDobleEnlazada:
            self.agregar_nodo_al_final(nodo)
    
    def get_nodo(self, posicion):
        contador = 0
        actual = self.inicio
        while actual:
            if contador == posicion:
                return actual
            contador += 1
            actual = actual.siguiente
        return None

    def __sizeof__(self) -> int:
        size = 0
        actual = self.inicio
        while actual:
            size += 1
            actual = actual.siguiente
        return size

    def __str__(self) -> str:
        actual = self.inicio
        str_resultado = ""

        while actual:
            str_resultado = str_resultado + str(actual) + "\n"
            actual = actual.siguiente

        return str_resultado

    def __iter__(self):
        actual = self.inicio
        while actual:
            yield actual
            actual = actual.siguiente

    def __len__(self):
        return self.__sizeof__()

class ListaArtistas(ListaDobleEnlazada):
        
    def agregar(self, nombre):
        # Verificar si el artista ya existe
        if self.existe(nombre):
            print(f"El artista {nombre} ya existe")
            return
        
        artista = Artista(nombre)
        nodo = Nodo(artista)
        
        self.agregar_nodo_al_final(nodo)
    
    def get_artista(self, nombre_artista):
        for artista_actual in self:
            if artista_actual.datos.nombre == nombre_artista:
                return artista_actual.datos
        
        print(f"El artista {nombre_artista} no existe")
        return None

    def existe(self, nombre):
        for artista_actual in self:
            if artista_actual.datos.nombre == nombre:
                return True
        
        return False

    def get_cancion(self, nombre_artista, nombre_album, nombre_cancion):
        # Buscar el artista
        for artista_actual in self:
            if artista_actual.datos.nombre == nombre_artista:
                # Buscar el album
                for album_actual in artista_actual.datos.lista_albumes:
                    if album_actual.datos.nombre == nombre_album:
                        # Buscar la cancion
                        for cancion_actual in album_actual.datos.lista_canciones:
                            if cancion_actual.datos.nombre == nombre_cancion:
                                return cancion_actual.datos # Objeto cancion
        
        print(f"La cancion {nombre_cancion} del album {nombre_album} del artista {nombre_artista} no existe")
        return None

    def get_all_canciones(self):
        canciones = ListaCanciones()

        for artista_actual in self:
            for album_actual in artista_actual.datos.lista_albumes:
                for cancion_actual in album_actual.datos.lista_canciones:

                    if canciones.existe(cancion_actual.datos.nombre):
                        continue
                    
                    cancion_temp = Cancion(cancion_actual.datos.nombre, cancion_actual.datos.ruta, cancion_actual.datos.imagen, cancion_actual.datos.artista, cancion_actual.datos.album)
                    cancion_temp.reproducciones = cancion_actual.datos.reproducciones

                    canciones.agregar_nodo_al_final(Nodo(cancion_temp))

        return canciones

    def get_album(self, nombre_artista, nombre_album):
        # Buscar el artista
        for artista_actual in self:
            if artista_actual.datos.nombre == nombre_artista:
                # Buscar el album
                for album_actual in artista_actual.datos.lista_albumes:
                    if album_actual.datos.nombre == nombre_album:
                        return album_actual.datos # Objeto album
                    
        print(f"El album {nombre_album} del artista {nombre_artista} no existe")
        return None

    def get_albumes(self, nombre_artista):
        # Buscar el artista
        for artista_actual in self:
            if artista_actual.datos.nombre == nombre_artista:
                return artista_actual.datos.lista_albumes
        
        print("El artista no existe")

    def graficar(self):  
        try:
            print("graficando biblioteca...")
            archivo = filedialog.asksaveasfilename(
                initialdir="/",
                title="Guardar grafico",
                filetypes=(("archivo png", "*.png"), ("todos los archivos", "*.*"))
            )

            if archivo:

                # Crear el grafo
                graph = Digraph('G', format='png', engine='dot', comment='Biblioteca')

                # Configurar atributos del grafo
                graph.attr(rankdir='LR', ranksep='1.0')
                graph.attr('node', shape='box', style='rounded', fontname='Courier', fontsize='10')

                # Agregar nodos y enlaces
                contador_a = 0
                for artista_actual in self:
                    # Crear nodo de artista
                    graph.node(f'nodo_a_{contador_a}', f'Artista:\n{artista_actual.datos.nombre}', color='#836096')

                    # Agregar nodos de albumes
                    lista_albumes = artista_actual.datos.lista_albumes

                    # Enlazar artista con albumes
                    if len(lista_albumes) > 0:
                        lista_albumes.graficar(graph, contador_a)
                        graph.edge(f'nodo_a_{contador_a}', f'nodo_b_{contador_a}_0')

                    # Enlazar artistas
                    if artista_actual.siguiente:
                        graph.edge(f'nodo_a_{contador_a}', f'nodo_a_{contador_a+1}')

                    contador_a += 1
                # Renderizar y mostrar el gráfico
                graph.render(archivo, view=True, cleanup=True)

        except Exception as e:
            print(f"No se pudo graficar la lista. Error: {e}")
    
class ListaAlbumes(ListaDobleEnlazada):
    
    def agregar(self, nombre, imagen):
        # Verificar si el album ya existe
        if self.existe(nombre):
            print(f"El album {nombre} ya existe")
            return
        
        album = Album(nombre, imagen)
        nodo = Nodo(album)

        self.agregar_nodo_al_final(nodo)
    
    def existe(self, nombre):
        for album_actual in self:
            if album_actual.datos.nombre == nombre:
                return True
        
        return False
    
    def get_canciones(self, nombre_album):
        # Buscar el album
        for album_actual in self:
            if album_actual.datos.nombre == nombre_album:
                return album_actual.datos.lista_canciones
        
        print("El album no existe")

    def graficar(self, graph, contador_a):
        contador_b = 0
        for album_actual in self:
            graph.node(f'nodo_b_{contador_a}_{contador_b}', f'Album:\n{album_actual.datos.nombre}', color='#6585a5')

            # Agregar nodos de canciones
            lista_canciones = album_actual.datos.lista_canciones

            # Enlazar artista con albumes
            if len(lista_canciones) > 0:
                lista_canciones.graficar(graph, contador_a, contador_b)
                graph.edge(f'nodo_b_{contador_a}_{contador_b}', f'nodo_c_{contador_a}_{contador_b}_0')

            # Enlazar artistas
            if album_actual.siguiente:
                graph.edge(f'nodo_b_{contador_a}_{contador_b}', f'nodo_b_{contador_a}_{contador_b+1}')

            contador_b += 1

class ListaCanciones(ListaDobleEnlazada):

    def agregar(self, nombre, ruta, imagen, artista, album):

        # Verificar si la cancion ya existe
        if self.existe(nombre):
            print(f"La cancion {nombre} ya existe")
            return
        
        cancion = Cancion(nombre, ruta, imagen, artista, album)
        nodo = Nodo(cancion)

        self.agregar_nodo_al_final(nodo)
    
    def agregar_cancion(self, cancion): # Recibe un objeto de tipo cancion

        # Verificar si la cancion ya existe
        if self.existe(cancion.nombre):
            print(f"La cancion {cancion.nombre} ya existe")
            return
        
        nodo = Nodo(cancion)
        self.agregar_nodo_al_final(nodo)
        print(f"Cancion {cancion.nombre} agregada a la lista de canciones")


    def existe(self, nombre):
        for cancion_actual in self:
            if cancion_actual.datos.nombre == nombre:
                return True
        
        return False

    def get_top_canciones(self, cantidad):
        # Crear una lista temporal para almacenar las canciones ordenadas
        canciones_ordenadas = sorted(self, key=lambda x: x.datos.reproducciones, reverse=True)

        # Devolver las primeras "cantidad" canciones
        return canciones_ordenadas[:cantidad]

    def graficar(self, graph, contador_a, contador_b): # Recibe el grafo, el contador del artista y el contador del album
        contador_c = 0
        for cancion_actual in self:
            graph.node(f'nodo_c_{contador_a}_{contador_b}_{contador_c}', f'Cancion:\n{cancion_actual.datos.nombre}', color='#F4E869')

            # Enlazar artistas
            if cancion_actual.siguiente:
                graph.edge(f'nodo_c_{contador_a}_{contador_b}_{contador_c}', f'nodo_c_{contador_a}_{contador_b}_{contador_c+1}')

            contador_c += 1
    

# Lista doblemene enlazada circular
class ListaDobleEnlazadaCircular:
    def __init__(self):
        self.inicio = None

    def agregar_nodo_al_final(self, nodo):
        if self.inicio is None:
            self.inicio = nodo
            nodo.anterior = nodo
            nodo.siguiente = nodo
        else:
            ultimo = self.inicio.anterior
            ultimo.siguiente = nodo
            nodo.anterior = ultimo
            nodo.siguiente = self.inicio
            self.inicio.anterior = nodo

    def agregar_nodo_al_inicio(self, nodo):
        self.agregar_nodo_al_final(nodo)
        self.inicio = nodo

    def expandir(self, lista_doble_enlazada):
        for nodo in lista_doble_enlazada:
            self.agregar_nodo_al_final(nodo)

    def get_nodo(self, posicion):
        if self.inicio is None:
            return None

        actual = self.inicio
        for _ in range(posicion):
            actual = actual.siguiente

        return actual

    def get_random(self):
        if self.inicio is None:
            return None

        posicion = random.randint(0, len(self) - 1)

        print("Posicion aleatoria: ", posicion)
        print("retornando nodo: ", self.get_nodo(posicion))

        return self.get_nodo(posicion)

    def __sizeof__(self) -> int:
        if self.inicio is None:
            return 0

        size = 0
        actual = self.inicio
        while True:
            size += 1
            actual = actual.siguiente
            if actual == self.inicio:
                break
        return size

    def __str__(self) -> str:
        if self.inicio is None:
            return "Lista vacía"

        actual = self.inicio
        str_resultado = ""
        while True:
            str_resultado += str(actual) + "\n"
            actual = actual.siguiente
            if actual == self.inicio:
                break
        return str_resultado

    def __iter__(self):
        if self.inicio is None:
            return

        actual = self.inicio
        while True:
            yield actual
            actual = actual.siguiente
            if actual == self.inicio:
                break

    def __len__(self):
        return self.__sizeof__()

class Playlist(ListaDobleEnlazadaCircular):

    def existe(self, nombre):
        for cancion_actual in self:
            if cancion_actual.datos.nombre == nombre:
                return True
        
        return False

    def agregar_cancion(self, cancion): # Recibe un objeto de tipo cancion
        nodo = Nodo(cancion)
        self.agregar_nodo_al_final(nodo)
    
    def get_cancion(self, nombre_cancion):
        for cancion_actual in self:
            if cancion_actual.datos.nombre == nombre_cancion:
                return cancion_actual.datos
            
        print(f"La cancion {nombre_cancion} no existe")
        return None
    
    def get_siguiente_cancion(self, nombre_cancion):
        for cancion_actual in self:
            if cancion_actual.datos.nombre == nombre_cancion:
                siguiente_cancion = cancion_actual.siguiente.datos
                if cancion_actual.siguiente == self.inicio:
                    # Si estamos en el último nodo, regresar al inicio
                    siguiente_cancion = self.inicio.datos
                return siguiente_cancion

        print(f"La canción {nombre_cancion} no existe")
        return None

    def get_anterior_cancion(self, nombre_cancion):
        for cancion_actual in self:
            if cancion_actual.datos.nombre == nombre_cancion:
                anterior_cancion = cancion_actual.anterior.datos
                if cancion_actual.anterior == self.inicio:
                    # Si estamos en el primer nodo, ir al final
                    anterior_cancion = self.inicio.anterior.datos
                return anterior_cancion

        print(f"La canción {nombre_cancion} no existe")
        return None

    def get_cancion_random(self): # Retorna un objeto de tipo cancion

        if self.inicio is None:
            return None
        
        if self.inicio == self.inicio.siguiente:
            return self.inicio.datos
        
        cancion = self.get_random()

        if cancion == None:
            print("No hay canciones en la playlist")
            return None

        return cancion.datos
    
    def get_cancion_pos(self, posicion):
        
        if posicion < 0 or posicion >= len(self):
            print("La posicion no existe")
            return None
        
        cancion = self.get_nodo(posicion)

        if cancion == None:
            print("La cancion no existe")
            return None

        return self.get_nodo(posicion).datos

    def copy(self): # Retorna una copia de la playlist
        playlist = Playlist()
        
        for nodo_temp in self:
            cancion = nodo_temp.datos
            cancion_copy = Cancion(cancion.nombre, cancion.ruta, cancion.imagen, cancion.artista, cancion.album)
            playlist.agregar_cancion(cancion_copy)

        return playlist

    def eliminar_cancion(self, nombre_cancion):
        print(f"Eliminando cancion {nombre_cancion}...")

        nodo_actual = self.inicio

        while nodo_actual:
            if nodo_actual.datos.nombre == nombre_cancion:
                if nodo_actual.siguiente == nodo_actual:  # Único nodo en la lista
                    self.inicio = None
                else:
                    nodo_actual.anterior.siguiente = nodo_actual.siguiente
                    nodo_actual.siguiente.anterior = nodo_actual.anterior
                    if nodo_actual == self.inicio:  # Si se elimina el primer nodo
                        self.inicio = nodo_actual.siguiente
                return True

            nodo_actual = nodo_actual.siguiente
            if nodo_actual == self.inicio:  # Se ha recorrido toda la lista
                break

        print(f"La cancion {nombre_cancion} no existe")
        return False

    def mezclar(self):

        #Mezclar la playlist actual
        playlist = self.copy()

        #Crear una nueva playlist
        nueva_playlist = Playlist()

        #Mientras la playlist tenga canciones
        while len(playlist) != 0:

            #Obtener una cancion aleatoria, sin repetir
            cancion = None
            cancion = playlist.get_cancion_random() # Cancion

            if cancion == None:
                print("No hay canciones en la playlist")
                return None

            #Agregar la cancion a la nueva playlist
            nueva_playlist.agregar_cancion(cancion)
            
            #Eliminar la cancion de la playlist
            if not playlist.eliminar_cancion(cancion.nombre):
                print("No se pudo eliminar la cancion de la playlist")
                return None
        
        #Retornar la nueva playlist
        return nueva_playlist

        
