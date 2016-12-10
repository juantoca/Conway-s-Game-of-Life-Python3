import shutil
import Nucleo
import multiprocessing
import time


class Interfaz:

    def __init__(self, center=(0, 0)):
        self.archivos = Archivos()
        self.altura = shutil.get_terminal_size().lines - 2
        self.anchura = shutil.get_terminal_size().columns - 2
        self.carga = self.cargar()  # [0]carga, [1]descarga
        self.mundo = Nucleo.Mundo(coordinates=self.archivos.load(self.carga[0]))
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

    def cargar(self):  # Pregunta al usuario la ruta de los archivos a cargar
        load = input("Elija la ruta del archivo a cargar\n-->")
        save = input("Elija la ruta del archivo donde volcar los resultados\n-->")
        return load, save

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

    def control(self):
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        tiempo_inicial = time.time()
        resultados = {}
        contador = 0
        while contador != self.limite:
            tiempo_ciclo = time.time()
            resultados = self.mundo.run(pool)
            if self.printear:
                self.printea(resultados["cells"])
            tiempo = self.tiempo - (time.time() - tiempo_ciclo)
            if tiempo > 0:
                time.sleep(tiempo)
            contador += 1
        tiempo = time.time() - tiempo_inicial
        print("Tiempo total: " + str(tiempo))
        print("Número de células: " + str(len(resultados["cells"])))
        print("Media por ciclo: " + str(tiempo/self.limite))
        print("Ciclos por segundo: " + str(self.limite/tiempo))
        self.archivos.save(resultados["cells"], arch=self.carga[1])

    def printea(self, cells, living="#", dead=" "):
        mapa = ""
        top = self.diagonal[0]
        bot = self.diagonal[1]
        coordinates = top
        while coordinates != (top[0], bot[1]-1):
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
        top = (int(- self.anchura/2 + self.center[0]), int(self.altura/2 - self.center[1]))
        bot = (int(self.anchura/2 + self.center[0]), int(self.center[1] - self.altura/2))
        return top, bot


class Archivos:
    
    def load(self, arch="./output.txt"):
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

    def save(self, celulas, arch="./output.txt"):
        cells = self.coordenadas_positivas(celulas)
        claves = cells.keys()
        mapa = ""
        top = [0, 0]
        bot = [0, 0]
        for x in claves:
            if x[0] < top[0]:
                top[0] = x[0]
            elif x[0] > bot[0]:
                bot[0] = x[0]
            if x[1] > top[1]:
                top[1] = x[1]
            elif x[1] < bot[1]:
                bot[1] = x[1]
        coordinates = tuple(top)
        limite = tuple(bot)
        while coordinates != (0, limite[1]-1):
            if coordinates in cells:
                mapa += "O"
            else:
                mapa += "."
            if coordinates[0] == bot[0]:  # Saltamos a la siguiente línea
                coordinates = (top[0], coordinates[1]-1)
                mapa += "\n"
            else:  # Avanzamos un carácter
                coordinates = (coordinates[0]+1, coordinates[1])
        with open(arch, "w") as arch:
            arch.write(mapa)

    def coordenadas_positivas(self, cells):  # La función save necesita que todas las coordenadas sean positivas
        claves = list(cells.keys())
        diccionario = {}
        minX = 0
        minY = 0
        for x in claves:
            if x[0] < minX:
                minX = x[0]
            if x[1] < minY:
                minY = x[1]
        for x in claves:
            diccionario[(x[0]-minX, x[1]-minY)] = None
        return diccionario

if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.inicio()
