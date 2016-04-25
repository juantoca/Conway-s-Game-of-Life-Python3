import time


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
        self.toBorn = []
        self.toKill = []
        self.limite = limite
        self.tiempo = tiempo
        self.print_during = print_during
        self.builder(self.coordinates)

    def run(self):  # LOOP DEL JUEGO
        salir = 0
        tiempoinicial = time.time()
        while salir != self.limite:
            if self.print_during is True and self.interfaz is not None:
                self.interfaz.run(self.cells)
            if self.debugging is True:
                tiempo = time.time()
            self.refresher()
            if self.debugging is True:
                print("Tiempo del loop " + str(salir) + ":" + str(time.time() - tiempo))
            if self.tiempo > 0:
                time.sleep(self.tiempo)
            self.toBorn = []
            salir += 1
        if self.debugging is True:
            print("Tiempo total: " + str(time.time() - tiempoinicial))
        if self.debugging is True:
            celulas = len(self.cells)
            print(str(salir) + "    " + str(celulas))
        if self.debugging is True:
            print(self.cells)
        if self.interfaz is not None:
            self.interfaz.run(self.cells)

    def builder(self, lista):  # Crea instancias de celulas en las coordenadas dadas
        for x in lista:
            if x not in self.cells.items():
                self.cells[x] = None

    def refresher(self):  # Manda a las células refrescar su situación
        for x in self.cells.keys():
            self.refresh(x)
        self.builder(self.toBorn)
        self.toBorn = []
        self.kill()

    def kill(self):
        for x in self.toKill:
            objecto = self.cells[x]
            del objecto
            del self.cells[x]
        self.toKill = []

    def adjacent_life(self, square):
        counter = 0
        for x in self.variacion:
            if (square[0] + x[0], square[1] + x[1]) in self.cells.keys():
                counter += 1
        return counter

    def survivality(self, coordinates):
        if self.adjacent_life(coordinates) > 3 or self.adjacent_life(coordinates) < 2:
            self.toKill.append(coordinates)

    def refresh(self, coordinates):
        self.survivality(coordinates)
        for x in self.variacion:
            coordenadas = (x[0] + coordinates[0], x[1] + coordinates[1])
            if self.adjacent_life(coordenadas) == 3:
                self.toBorn.append(coordenadas)


def main():
    coordenadas = [(0, 0), (1, 0), (-1, 0)]
    mundo = Mundo(coordinates=coordenadas, limite=200000, debugging=True)
    mundo.run()

if __name__ == "__main__":
    main()