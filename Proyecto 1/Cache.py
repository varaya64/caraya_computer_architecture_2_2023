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
        self.bloques = [BloqueCache(i, "I", 0, "000") for i in range(numBloques)]

    #Metodo para hacer un read 
    def read_instruccion(self, instruccion):
        procesador_id = instruccion[3]
        for bloque in self.bloques:
            if bloque.dir == instruccion[1] and bloque.state != "I":
                #print(bloque.data)
                return ["done"]
            else:
                resultado = ["RC", procesador_id, instruccion[1], 0]
                return resultado
    
    #Metodo para hacer un read
    def write_instruccion(self, instruccion):
        #instruccion: [tipo,direccion,dato,id]
        #Encuentro bloque disponible segun jerarquia
        w_bloque = self.encontrar_bloque() 
        #Write para el caso 1
        
        
        for bloque in self.bloques:
            if bloque.dir == instruccion[1]:
                w_bloque = bloque
                break
                
    
        if w_bloque.state == "I" or w_bloque.state == "E" or w_bloque.state == "S":
            procesador_id = instruccion[3]
            #nueva_instrucion = ["IE", procesador_id, instruccion[1], w_bloque.data]
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            return ["done"]
            
        #Write para el caso 2
        elif (w_bloque.state == "M"):
            procesador_id = instruccion[3]
            nueva_instrucion = ["IE-WB", procesador_id, w_bloque.dir, w_bloque.data]
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            return nueva_instrucion
       
        #Write para el caso 3
        elif (w_bloque.state == "O"):
            procesador_id = instruccion[3]
            nueva_instrucion = ["IE-WB", procesador_id, w_bloque.dir, w_bloque.data]
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            w_bloque.state = "M"
            return nueva_instrucion



    def write_read_instruccion(self, instruccion):
        #instruccion: [tipo,direccion,dato,id]
        #Encuentro bloque disponible segun jerarquia
        w_bloque = self.encontrar_bloque() 
        #Write para el caso 1
        
    
        if w_bloque.state == "I" or w_bloque.state == "E" or w_bloque.state == "S":
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            if instruccion[0] == "read-w":
                w_bloque.state = "S"
            elif instruccion[0] == "read-wm":
                w_bloque.state = "E"
            return ["done"]
          
       
        #Write para el caso 2
        elif (w_bloque.state == "M"):
            procesador_id = instruccion[3]
            nueva_instrucion = ["WB", procesador_id, w_bloque.dir, w_bloque.data]
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            if instruccion[0] == "read-w":
                w_bloque.state = "S"
            elif instruccion[0] == "read-wm":
                w_bloque.state = "E"
            return nueva_instrucion
       
        #Write para el caso 3
        elif (w_bloque.state == "O"):
            procesador_id = instruccion[3]
            nueva_instrucion = ["IE-WB", procesador_id, w_bloque.dir, w_bloque.data]
            w_bloque.dir = instruccion[1]
            w_bloque.data = instruccion[2]
            if instruccion[0] == "read-w":
                w_bloque.state = "S"
            elif instruccion[0] == "read-wm":
                w_bloque.state = "E"
            return nueva_instrucion


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
            if bloque.dir == direccion and bloque.state != "I":
                if bloque.state == "E":
                    bloque.state = "S"
                elif bloque.state == "M":
                    bloque.state = "O"
                return bloque.data
        return None
            
    def invalidar_bloque(self, dir):
        for bloque in self.bloques:
            if bloque.dir == dir:
                if bloque.state == "O" or bloque.state == "M":
                    bloque.state = "I"
                    return bloque.data
                else:
                    bloque.state = "I"
        return None