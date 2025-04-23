import random

# Clase base para los agentes
class Agente:
    def __init__(self, nombre, posicion):
        self.nombre = nombre
        self.pos = posicion

# Agente Rojo - intenta llegar a la meta (camino más corto)
class AgenteRojo(Agente):
    def __init__(self, posicion, meta, size):
        super().__init__('Rojo', posicion)
        self.meta = meta
        self.size = size

    def mover(self, pos_amarillo):
        fila, col = self.pos
        objetivo_fila, objetivo_col = self.meta

        # Posibles movimientos (arriba, abajo, izquierda, derecha)
        movimientos = [
            (fila - 1, col),
            (fila + 1, col),
            (fila, col - 1),
            (fila, col + 1)
        ]

        # Filtrar movimientos dentro del tablero y que no estén ocupados por el amarillo
        opciones = [m for m in movimientos
                    if 0 <= m[0] < self.size and 0 <= m[1] < self.size and m != pos_amarillo]

        # Elegir el/los movimientos que más acerquen a la meta (distancia Manhattan)
        if opciones:
            # Calcular la distancia para cada movimiento
            opciones.sort(key=lambda x: abs(x[0] - objetivo_fila) + abs(x[1] - objetivo_col))
            min_dist = abs(opciones[0][0] - objetivo_fila) + abs(opciones[0][1] - objetivo_col)

            # Filtrar solo los movimientos con la distancia mínima
            mejores_opciones = [m for m in opciones if abs(m[0] - objetivo_fila) + abs(m[1] - objetivo_col) == min_dist]

            # Elegir aleatoriamente una de las mejores opciones
            self.pos = random.choice(mejores_opciones)

        return self.pos

# Agente Amarillo - se mueve verticalmente para bloquear al rojo
class AgenteAmarillo(Agente):
    def __init__(self, posicion, size):
        super().__init__('Amarillo', posicion)
        self.col_fija = posicion[1]  # Solo se mueve en esta columna
        self.size = size

    def mover(self, pos_rojo, meta):
        fila_rojo, col_rojo = pos_rojo
        fila_actual = self.pos[0]

        # Si el rojo está cerca de la meta, seguir bloqueando
        if abs(fila_rojo - meta[0]) <= 1:  # Cuando el rojo está a un paso de la meta
            if fila_rojo < fila_actual and fila_actual > 0:
                fila_actual -= 1
            elif fila_rojo > fila_actual and fila_actual < self.size - 1:
                fila_actual += 1
            else:
                # Amarillo debe moverse para no quedarse quieto
                if fila_actual > 0 and fila_actual < self.size - 1:
                    fila_actual += random.choice([-1, 1])
                elif fila_actual == 0:
                    fila_actual += 1
                else:
                    fila_actual -= 1
        else:
            # Si el rojo no está tan cerca de la meta, bloquear normalmente
            if col_rojo == self.col_fija:
                if fila_rojo < fila_actual and fila_actual > 0:
                    fila_actual -= 1
                elif fila_rojo > fila_actual and fila_actual < self.size - 1:
                    fila_actual += 1
                else:
                    # Ya está alineado, igual debe moverse (evitar quedarse quieto)
                    if fila_actual > 0 and fila_actual < self.size - 1:
                        fila_actual += random.choice([-1, 1])
                    elif fila_actual == 0:
                        fila_actual += 1
                    else:
                        fila_actual -= 1
            else:
                # Si el rojo no está en su columna, igual moverse verticalmente
                if fila_actual > 0 and fila_actual < self.size - 1:
                    fila_actual += random.choice([-1, 1])
                elif fila_actual == 0:
                    fila_actual += 1
                else:
                    fila_actual -= 1

        self.pos = (fila_actual, self.col_fija)
        return self.pos

# Representación del entorno
class Tablero:
    def __init__(self, size, orden_turnos='rojo'):
        self.size = size
        self.meta = (0, size - 1)  # Meta siempre es arriba a la derecha
        self.rojo = AgenteRojo((size - 1, 0), self.meta, size)  # Rojo inicia abajo a la izquierda
        self.amarillo = AgenteAmarillo((0, size - 1), size)  # Amarillo inicia arriba a la derecha
        self.turno = 0
        self.orden_turnos = orden_turnos  # Define el orden fijo de turnos: 'rojo' o 'amarillo'

    def mostrar(self):
        print(f"\nTurno {self.turno}:")
        for i in range(self.size):
            fila = []
            for j in range(self.size):
                if (i, j) == self.rojo.pos:
                    fila.append('R')
                elif (i, j) == self.amarillo.pos:
                    fila.append('A')
                elif (i, j) == self.meta:
                    fila.append('M')
                else:
                    fila.append('.')
            print(' '.join(fila))

    def jugar(self, max_turnos=20):
        while self.rojo.pos != self.meta and self.turno < max_turnos:
            self.turno += 1

            # Orden fijo: Primero rojo o amarillo, luego el otro
            if self.orden_turnos == 'rojo':
                # Rojo mueve primero
                self.rojo.mover(self.amarillo.pos)
                self.amarillo.mover(self.rojo.pos, self.meta)
            else:
                # Amarillo mueve primero
                self.amarillo.mover(self.rojo.pos, self.meta)
                self.rojo.mover(self.amarillo.pos)

            self.mostrar()

        if self.rojo.pos == self.meta:
            print("\n🎯 El agente ROJO llegó a la meta!")
        else:
            print("\n🛑 Se alcanzó el límite de turnos. El ROJO no pudo escapar.")

# --- EJECUCIÓN ---

if __name__ == "__main__":
    tamano_tablero = 3  # Cambiá esto por 3, 4 o 5 según lo que quieras
    orden_turnos = input("¿Quién empieza, 'rojo' o 'amarillo'? ").strip().lower()
    juego = Tablero(tamano_tablero, orden_turnos)
    juego.mostrar()
    juego.jugar()
