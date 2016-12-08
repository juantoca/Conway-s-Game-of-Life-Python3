# coding:utf-8
import time
import multiprocessing

"""Motor de análisis para el Juego de la Vida de Conway

Escrito integramente por: Juan Toca bajo licencia GPL-3.0
"""


# El multithreading solo mejora el rendimiento en cálculos grandes

""""Conclusiones extraídas en el desarrollo:

        1. Tras muchos intentos, no he conseguido optimizar el programa
    a través de la implementación de un diccionario en el cuál se almacenaran las células ya analizadas(a través de
    los distintos análisis se puede llegar a analizar la misma casilla hasta 8 veces(si esta esta completamente rodeada
    ) aunque teniendo en cuenta que esta disposición tiende a ser autodestructiva, no debería afectar demasiado al
    rendimiento). Supongo que este diccionario tenía demasiadas llamadas y mantenía a los procesos inactivos demasiado
    tiempo(recordemos que una sección de memoria compartida no se puede acceder a la vez por dos procesos)

        2. No me acaba de convencer que el bucle lo lleve Nucleo en vez de Interfaz, pero es la única forma que he
    encontrado de evitar que tenga que crear los procesos en cada ciclo(ya que el objeto pool no es pickleable, no
    lo puedo mantener como atributo de la clase y evitar que se destruya en cada ciclo). EDITO: Funciona creando pool
    en interfaz y pasandolo como argumento

        3. Parece que hasta el diccionario de coordenadas futuras se colapsa ante el número de peticiones del algoritmo
    (suprimiendo el guardado en este diccionario pero haciendo los cálculos se optimiza en un 50%). Solución: Volver
    ha usar una escritura de datos de un solo hilo"""


class Mundo:  # Clase que maneja el juego

    def __init__(self, coordinates=(), rules={"toborn": (3, ), "tolive": (2, 3)}):
        # Self-Explanatory
        self.variacion = ((-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))
        self.cells = {}  # Diccionario donde se almacena la situación vieja y donde al final del análisis se vuelca
                            # los resultados del análisis
        self.builder(coordinates)
        self.rules = rules

    def builder(self, coordinates):  # RECREA el diccionario y lo llena con las coordenadas dadas
        for x in coordinates:
            self.cells[x] = None

    def run(self, pool):  # Pasa un ciclo y devuelve el estado del mapa
                    # y otra información de debugging en un diccionario
        tiempo_inicial = time.time()
        self.bucle(pool)
        tiempo_final = time.time() - tiempo_inicial
        return {"time": tiempo_final, "cells": self.cells}

    def bucle(self, pool):  # LOOP DEL JUEGO
            claves = self.cells.keys()
            coordenadas = pool.map(self.analisis, claves)
            self.cells = {}
            for y in coordenadas:
                self.builder(y)

    def analisis(self, coordinates):  # Función que refresca la situación
                                        # de una región del mapa en función  de unas coordenadas
        coordenadas_futuras = []
        alive = 0  # Contamos el número de células alrededor de la que queremos saber si sobrevive
        for x in self.variacion:
            adj_coordinates = (coordinates[0]+x[0], coordinates[1]+x[1])
            if adj_coordinates in self.cells:
                alive += 1
            else:  # Si no existe la célula, puede nacer una en esa posición
                    born = 0
                    for y in self.variacion:
                        neighbours = (adj_coordinates[0]+y[0], adj_coordinates[1]+y[1])
                        if neighbours in self.cells:
                            born += 1
                    if born in self.rules["toborn"]:  # Si cumple las reglas se añade al diccionario
                        coordenadas_futuras.append(adj_coordinates)
        if alive in self.rules["tolive"]:  # Si cumple la regla se añade al diccionario de construcción
            coordenadas_futuras.append(coordinates)
        return coordenadas_futuras


def main():     # MAIN
    coordenadas = [(0, 0), (1, 0), (-1, 0)]
    mundo = Mundo(coordinates=coordenadas)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    mundo.run(pool)

if __name__ == "__main__":
    main()
