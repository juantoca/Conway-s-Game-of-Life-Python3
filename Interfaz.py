import shutil
import NucleoExp as Nucleo


class Interfaz:

    def __init__(self, center=(0, 0)):
        self.center = center
        self.terminal_size = shutil.get_terminal_size()
        self.top_left_corner = self.get_corner()

    def inicio(self):
        archivos = Archivos()
        print("Bienvenido al Juego de la Vida")
        print("Idea original de John Conway")
        respuesta = ""
        while respuesta not in ("1", "2"):
            respuesta = input("\n\nElija el modo:\n1-Gráfico\n2-Solo cálculo\n[1/2]-->")
        if respuesta == "1":
            tiempo = None
            while tiempo is None:
                respuesta1 = input("Elija el tiempo entre ciclos\n-->")
                try:
                    tiempo = float(respuesta1)
                except ValueError:
                    pass
            limite = self.limite()
            mundo = Nucleo.Mundo(coordinates=archivos.load(), interfaz=self, tiempo=tiempo,
                                 limite=limite, print_during=True)
            mundo.run()
        elif respuesta == "2":
            limite = self.limite()
            mundo = Nucleo.Mundo(coordinates=archivos.load(), limite=limite, debugging=True)
            mundo.run()

    def limite(self):
        limite = None
        while limite is None:
            respuesta2 = input("Elija el limite de ciclos(números negativos = ciclos infinitos)"
                               "(No acepta decimales)\n-->")
            try:
                limite = int(respuesta2)
            except ValueError:
                pass
        return limite

    def get_corner(self):  # Consigue la esquina superior izquierda respecto al centro
                            # y las dimensiones de la terminal
        corner = (int(-self.terminal_size.columns / 2 - self.center[0]),
                  int(self.terminal_size.lines / 2 - self.center[1]))
        return corner

    def prepare_map(self, cells):  # Prepara el mapa para pasarse por pantalla
        mapa = ""
        counter = list(self.top_left_corner)
        salir = False
        while salir is False:
            if tuple(counter) in cells.keys():
                mapa += "#"
            else:
                mapa += " "
            if counter[0] == self.top_left_corner[0] + self.terminal_size.columns:
                mapa += "\n"
                counter[1] -= 1
                counter[0] = self.top_left_corner[0]
            if tuple(counter) == (self.top_left_corner[0], self.top_left_corner[1] - self.terminal_size.lines):
                salir = True
            counter[0] += 1
        return mapa

    def run(self, cells):  # Pasa por pantalla el mapa
        print(self.prepare_map(cells))


class Archivos:

    def __init__(self, rutainput="./mapa.txt", rutaoutput="./output.txt"):
        self.rutainput = rutainput
        self.rutaoutput = rutaoutput

    def load(self):
        cells = []
        with open(self.rutainput, "r") as arch:
            archivo = arch.read()
            lineas = archivo.split("\n")
            counter = 0
            for x in lineas:
                if x[0] == "!":
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


def main():
    archivos = Archivos()
    archivos.load()
    cells = archivos.load()
    interfaz = Interfaz()
    # interfaz.inicio()
    mundo = Nucleo.Mundo(coordinates=cells, interfaz=interfaz, limite=2000, print_during=False, debugging=True)
    mundo.run()

main()
