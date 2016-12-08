import shutil
import Nucleo
import multiprocessing
import time

class Interfaz:

    def __init__(self, center=(0, 0)):
        self.archivos = Archivos()
        self.altura = shutil.get_terminal_size().lines
        self.anchura = shutil.get_terminal_size().columns
        self.mundo = Nucleo.Mundo(coordinates=self.archivos.load())
        self.printear = False
        self.limite = 0
        self.tiempo = 0
        self.center = center
        self.diagonal = self.get_diagonal()  # [0]top_left, [1]bot_rigth

    def inicio(self):
        print("Bienvenido al Juego de la Vida")
        print("Idea original de John Conway")
        respuesta = ""
        while respuesta not in ("1", "2"):
            respuesta = input("\n\nElija el modo:\n1-Gráfico\n2-Solo cálculo\n[1/2]-->")
        if respuesta == "1":
            self.printear = True
            tiempo = None
            while tiempo is None:
                respuesta1 = input("Elija el tiempo entre ciclos\n-->")
                try:
                    tiempo = float(respuesta1)
                    self.tiempo = tiempo
                except ValueError:
                    pass
            self.printear = True
        self.limit()
        self.control()

    def limit(self):
        limite = None
        while limite is None:
            respuesta2 = input("Elija el limite de ciclos(números negativos = ciclos infinitos)"
                               "(No acepta decimales)\n-->")
            try:
                limite = int(respuesta2)
            except ValueError:
                pass
        self.limite = limite

    def run(self, estado):
        if self.printear:
            self.printea(estado["cells"])

    def control(self):
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        tiempo_inicial = time.time()
        resultados = {}
        for x in range(self.limite):
            resultados = self.mundo.run(pool)
            if self.printear:
                self.printea(resultados["cells"])
            tiempo = self.tiempo - time.time() - tiempo_inicial
            if tiempo > 0:
                time.sleep(tiempo)
        print("Tiempo total: " + str(time.time() - tiempo_inicial))
        print("Número de células: " + str(len(resultados["cells"])))

    def printea(self, cells, living="#", dead=" "):
        mapa = ""
        top = self.diagonal[0]
        bot = self.diagonal[1]
        coordinates = top
        while coordinates != bot:
            if coordinates in cells:
                mapa += living
            else:
                mapa += dead
            if coordinates[0] == bot[0]:  # Saltamos a la siguiente línea
                coordinates = (top[0], coordinates[1]-1)
                mapa += "\n"
            else:  # Avanzamos un carácter
                coordinates = (coordinates[0]+1, coordinates[1])
        print(mapa)

    def get_diagonal(self):
        top = (- self.anchura/2 + self.center[0], self.altura/2 - self.center[1])
        bot = (self.anchura/2 + self.center[0], self.center[1] - self.altura/2)
        return top, bot


class Archivos:

    def load(self, arch="./mapa.txt"):
        cells = []
        with open(arch, "r") as arch:
            archivo = arch.read()
            lineas = archivo.split("\n")
            counter = 0
            for x in lineas:
                if x == "" or x[0] == "!":
                    lineas.pop(counter)
                counter += 1
            ylen = len(lineas)
            xlen = len(lineas[0])
            countery = int(ylen / 2)
            for y in lineas:
                counterx = int(-xlen / 2)
                for x in y:
                    if x == "O":
                        cells.append((counterx, countery))
                    counterx += 1
                countery -= 1
        return cells

if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.inicio()
