

class Mundo:  # Clase que maneja el juego

    def __init__(self, center=(0, 0), coordinates=(), interfaz=None,
                 tiempo=0, limite=-1, print_during=False, debugging=False):
        # Self-Explanatory
        self.variacion = ((-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))
        self.debugging = debugging
        self.interfaz = interfaz
        self.center = center
        self.toBorn = []
        self.toKill = []
        self.limite = limite
        self.tiempo = tiempo
        self.print_during = print_during
        self.builder(self.coordinates)
