class BloqueCache:
    def __init__(self, id, state, dir, data):
        self.id = id
        self.state = state
        self.dir = dir
        self.data = data

    def obtener_estado(self):
        return self.state

class Cache:
    def __init__(self, numBloques):
        self.states = ["I", "S", "E", "M", "O"]
        self.bloques = [BloqueCache(i, "I", "000", "000") for i in range(numBloques)]

    
    def read_instruccion(self, instruccion):
        r_bloque = self.encontrar_bloque()
        if r_bloque is not None:
            print("ando leyendo")
            print(r_bloque.id)

    def write_instruccion(self, instruccion):
        w_bloque = self.encontrar_bloque()
        if w_bloque is not None:
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            print(w_bloque.data)

    def encontrar_bloque(self):
        for state in self.states:
            bloque = self.encontrar_bloque_aux(state)
            return bloque

    def encontrar_bloque_aux(self, state):
        for bloque in self.bloques:
            if (state == bloque.state):
                return bloque
        return None