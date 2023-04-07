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
        #Encuentro bloque disponible segun jerarquia
        w_bloque = self.encontrar_bloque() 
        #Write para el caso 1
        if (w_bloque.state == "I" or w_bloque == "E" or w_bloque.state == "S"):
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            return ["Done"]
        #Write para el caso 2
        elif (w_bloque.state == "M"):
            print("Write Back")
            return ["WB", instruccion[1], instruccion[2]]
           
        #Write para el caso 3
        elif (w_bloque.state == "O"):
            print("write nack")
            print("Invalidacion por Escritura")
            return ["WB", "IE", instruccion[1], instruccion[2]]

    def encontrar_bloque(self):
        for state in self.states:
            bloque = self.encontrar_bloque_aux(state)
            return bloque

    def encontrar_bloque_aux(self, state):
        for bloque in self.bloques:
            if (state == bloque.state):
                return bloque
        