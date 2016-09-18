import shutil
import Nucleo


class Interfaz:

    def __init__(self, center=(0, 0)):
        self.center = center
        self.terminal_size = shutil.get_terminal_size()
        self.top_left_corner = self.get_corner()
        self.archivos = Archivos(self)

    def inicio(self):
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
            mundo = Nucleo.Mundo(coordinates=self.archivos.load(), interfaz=self, tiempo=tiempo,
                                 limite=limite, print_during=True)
            self.result = mundo.run()
        elif respuesta == "2":
            limite = self.limite()
            mundo = Nucleo.Mundo(coordinates=self.archivos.load(), limite=limite, debugging=True)
            self.result = mundo.run()
        self.final()

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

    def prepare_map(self, cells, living="#", death=" "):  # Prepara el mapa para pasarse por pantalla
        mapa = ""
        counter = list(self.top_left_corner)
        salir = False
        while salir is False:
            if tuple(counter) in cells.keys():
                mapa += living
            else:
                mapa += death
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

    def final(self):
        print("celulas: " + str(len(self.result["celulas"])))
        print("tiempo: " + str(self.result["tiempo"]))
        self.archivos.save()


class Archivos:

    def __init__(self, interfaz, rutainput="./mapa.txt", rutaoutput="./output.txt"):
        self.rutainput = rutainput
        self.rutaoutput = rutaoutput
        self.interfaz = interfaz

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

    def save(self):
        cells = self.interfaz.result["celulas"]
        top_right_corner = (0, 0)
        bot_left_corner = (0, 0)
        returneo = ""
        for coords in cells.keys():
            x = coords[0]
            y = coords[1]
            if x > top_right_corner[0]:
                top_right_corner = (x, top_right_corner[1])
            elif x < bot_left_corner[0]:
                bot_left_corner = (x, bot_left_corner[1])
            if y > top_right_corner[1]:
                top_right_corner = (top_right_corner[0], y)
            elif y < bot_left_corner[1]:
                bot_left_corner = (bot_left_corner[0], y)
        counterx = bot_left_corner[0]
        countery = top_right_corner[1]
        while countery >= bot_left_corner[1]:
            while counterx <= top_right_corner[0]:
                coords = (counterx, countery)
                if coords in cells:
                    returneo += "O"
                else:
                    returneo += "."
                counterx += 1
            counterx = 0
            returneo += "\n"
            countery -= 1
        with open(self.rutainput, "w") as arch:
            arch.write(returneo)


def main():
    interfaz = Interfaz()
    interfaz.inicio()

main()
