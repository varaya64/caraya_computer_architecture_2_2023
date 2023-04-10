"""
Clase del Bloque de Cache
"""
class BloqueCache:
    def __init__(self, id, state, dir, data):
        self.id = id
        self.state = state
        self.dir = dir
        self.data = data

    def obtener_estado(self):
        return self.state

"""
Clase de Cache
"""
class Cache:
    def __init__(self, numBloques):
        self.states = ["I", "S", "E", "M", "O"]
        self.bloques = [BloqueCache(i, "I", "000", "000") for i in range(numBloques)]

    #Metodo para hacer un read 
    def read_instruccion(self, instruccion):
        procesador_id = instruccion[3]
        for bloque in self.bloques:
            if bloque.dir == instruccion[1] and bloque.state != "I":
                print(bloque.data)
                return ["done"]
            else:
                resultado = ["RC", procesador_id, instruccion[1],0]
                return resultado
    
    #Metodo para hacer un read
    def write_instruccion(self, instruccion):
        
        #Encuentro bloque disponible segun jerarquia
        w_bloque = self.encontrar_bloque() 
        print(F"Bloque.state: {w_bloque.state}")
        #Write para el caso 1
        if (w_bloque.state == "I" or w_bloque.state == "E" or w_bloque.state == "S"):
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            procesador_id = instruccion[3]
            return ["done"]
            #print("Done")
       
        #Write para el caso 2
        elif (w_bloque.state == "M"):
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            procesador_id = instruccion[3]
            return ["WB", procesador_id, w_bloque.dir, w_bloque.data]
       
        #Write para el caso 3
        elif (w_bloque.state == "O"):
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            procesador_id = instruccion[3]
            return ["IE", procesador_id, w_bloque.dir, w_bloque.data]

    #Metodo para encontrar un bloque de cache disponible
    def encontrar_bloque(self):
        for state in self.states:
            bloque = self.encontrar_bloque_aux(state)
            if bloque != None:
                return bloque
                
        
    
    #Metodo para encontrar bloque de cache disponible auxiliar
    def encontrar_bloque_aux(self, state):
        for bloque in self.bloques:
            if (state == bloque.state):
                return bloque
        return None
            
    def actualizar_bloque(self, direccion):
        for bloque in self.bloques:
            if bloque.dir == direccion and bloque != "I":
                if bloque.state == "E":
                    bloque.state = "S"
                elif bloque.state == "M":
                    bloque.state = "O"
                return bloque.data
        return None
            
    def invalidar_bloque(self, dir):
        for bloque in self.bloques:
            if bloque.dir == dir:
                bloque.state = "I"
            else:
                return