import time


class Mundo:  # Clase que maneja el juego

    def __init__(self, center=(0, 0), coordinates=(), interfaz=None,
                 tiempo=0, limite=-1, print_during=False, debugging=False):
        # Self-Explanatory
        self.debugging = debugging
        self.interfaz = interfaz
        self.center = center
        self.coordinates = coordinates
        self.cells = {}
        self.toBorn = []
        self.toKill = []
        self.limite = limite
        self.tiempo = tiempo
        self.print_during = print_during
        self.builder(self.coordinates)

    def run(self):  # LOOP DEL JUEGO
        salir = 0
        celulas = len(self.cells)
        while salir != self.limite:
            if self.print_during is True and self.interfaz is not None:
                self.interfaz.run(self.cells)
            self.refresher()
            if self.tiempo > 0:
                time.sleep(self.tiempo)
            self.toBorn = []
            salir += 1
        if self.debugging is True:
            print(str(salir) + "    " + str(celulas))
        if self.debugging is True:
            print(self.cells)
        if self.interfaz is not None:
            self.interfaz.run(self.cells)

    def builder(self, lista):  # Crea instancias de celulas en las coordenadas dadas
        for x in lista:
            if x not in self.cells.items():
                objeto = Celula(x, self)
                self.cells[x] = objeto

    def refresher(self):  # Manda a las células refrescar su situación
        for x in self.cells.values():
            x.refresh()
        self.builder(self.toBorn)
        self.toBorn = []
        self.kill()

    def kill(self):
        for x in self.toKill:
            object = self.cells[x]
            del object
            del self.cells[x]
        self.toKill = []


class Celula:  # Clase célula viva

    def __init__(self, coordinates, mundo):
        self.coordinates = coordinates
        self.mundo = mundo
        self.variacion = ((-1, 1), (0, 1), (1,1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))

    def adjacent_life(self, square):
        counter = 0
        for x in self.variacion:
            if (square[0] + x[0], square[1] + x[1]) in self.mundo.cells.keys():
                counter += 1
        return counter

    def survivality(self):
        if self.adjacent_life(self.coordinates) > 3 or self.adjacent_life(self.coordinates) < 2:
            self.mundo.toKill.append(self.coordinates)

    def refresh(self):
        self.survivality()
        for x in self.variacion:
            coordenadas = (x[0]+self.coordinates[0], x[1] + self.coordinates[1])
            if self.adjacent_life(coordenadas) == 3:
                self.mundo.toBorn.append(coordenadas)


def main():
    coordenadas = [(0, 0), (1, 0), (-1, 0)]
    mundo = Mundo(coordinates=coordenadas, limite=2000)
    mundo.run()

if __name__ == "__main__":
    main()
