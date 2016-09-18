import time
import multiprocessing
"""Processing engine for Conway's Game of Life"""


# Multithreading only makes itself useful on long numbers of cells


class Mundo:  # Clase que maneja el juego

    def __init__(self, center=(0, 0), coordinates=(), interfaz=None,
                 tiempo=0, limite=-1, print_during=False, debugging=False):
        # Self-Explanatory
        self.variacion = ((-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))
        self.debugging = debugging
        self.interfaz = interfaz
        self.center = center
        self.coordinates = coordinates
        self.cells = {}
        self.limite = limite
        self.tiempo = tiempo
        self.print_during = print_during
        self.builder(self.coordinates)

    def run(self):  # LOOP DEL JUEGO
        salir = 0
        tiempoinicial = time.time()
        pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
        while salir != self.limite:
            if self.print_during is True and self.interfaz is not None:
                self.interfaz.run(self.cells)
            self.refresher(pool)
            if self.interfaz and self.tiempo > 0:
                time.sleep(self.tiempo)
            salir += 1
        result = self.final(tiempoinicial, salir)
        return result

    def final(self, tiempo, loops):  # Final del juego
        if self.debugging is True:
            tiempo = time.time() - tiempo
        if self.interfaz is not None:
            self.interfaz.run(self.cells)
        return {"celulas": self.cells, "tiempo": tiempo, "loops": loops}

    def builder(self, lista):  # Guarda las coordenadas de las células que deben nacer en el diccionario
        for x in lista:
            if x not in self.cells:
                self.cells[x] = None

    def refresher(self, pool):  # Refresca la situación de las células
        toborn = []
        todie = []
        results = pool.map(self.refresh, self.cells.keys())
        for x in results:
            for y in x[0]:
                toborn.append(y)
            for z in x[1]:
                todie.append(z)
        self.builder(toborn)
        self.kill(todie)

    def kill(self, lista):  # Borra del diccionario las células que deben morir
        for x in lista:
            objecto = self.cells[x]
            del objecto
            del self.cells[x]

    def adjacent_life(self, square):  # Cuenta las células vivas alrededor de una casilla
        counter = 0
        for x in self.variacion:
            if (square[0] + x[0], square[1] + x[1]) in self.cells:
                counter += 1
        return counter

    def survivality(self, coordinates):  # Detecta si la célula sobrevive o muere
        tokill = []
        if self.adjacent_life(coordinates) > 3 or self.adjacent_life(coordinates) < 2:
            tokill.append(coordinates)
        return tokill

    def refresh(self, coordinates):  # Refresca la situación de una coordenada
        toborn = []
        todie = self.survivality(coordinates)
        for x in self.variacion:
            coordenadas = (x[0] + coordinates[0], x[1] + coordinates[1])
            if self.adjacent_life(coordenadas) == 3:
                toborn.append(coordenadas)
        return [toborn, todie]


def main():
    coordenadas = [(0, 0), (1, 0), (-1, 0)]
    mundo = Mundo(coordinates=coordenadas, limite=200000, debugging=True)
    mundo.run()

if __name__ == "__main__":
    main()
