from Sistema import *
import threading

"""
Clase del Bloque de Memoria
"""
class BloqueMem:
    def __init__(self, id, data, dir):
        self.id = id
        self.data = data
        self.dir = dir


"""
Clase de Memoria
"""
class Memoria:
    def __init__(self, bus, sistema):
        self.bloques = [BloqueMem(i, 0, i) for i in range(8)]
        self.bus = bus
        self.sistema = sistema
        self.id = 999
        self.instruccion_actual = F"M{self.id} init"

    def escucha_bus(self):
        if len(self.bus.instrucciones) > 0 and self.bus.ack.count(self.id) == 0:
            instruccion_bus = self.bus.instrucciones[0]
            self.instruccion_actual = instruccion_bus
            #print(F"M{self.id} instruccion bus: {instruccion_bus}")
            id_respuesta = instruccion_bus[1]
            direccion = instruccion_bus[2]
            dato = instruccion_bus[3]
            if (instruccion_bus[0] == "WB") or (instruccion_bus[0] == "IE-WB"):
                self.write_back(dato, direccion)
                self.bus.ack.append(self.id)
            elif (instruccion_bus[0] == "IE"):
                self.bus.ack.append(self.id)
                
            elif instruccion_bus[0] == "RC":
                if len(self.bus.ack) == 4 and self.bus.cache_returned == False:
                    for bloque in self.bloques:
                        if direccion == bloque.dir:
                            instruccion = ["DRM", id_respuesta, bloque.dir, bloque.data]
                            self.bus.instrucciones.append(instruccion)
                            self.bus.ack.append(self.id)
                            #print(F"DR Done: {instruccion}")
                elif len(self.bus.ack) == 4 and self.bus.cache_returned == True:
                    self.bus.ack.append(self.id)
            elif instruccion_bus[0] == "DR" or instruccion_bus[0] == "DRM":
                self.bus.ack.append(self.id)
            
        
    def write_back(self, dato, direccion):
        for bloque in self.bloques:
            if ( bloque.dir == direccion):
                bloque.data = dato
                break

            
                
    def run(self):
        print(F"M{self.id} inicio en thread {threading.get_ident()}")
        while True:
            while len(self.sistema.procesadores_comenzaron) != 4:
                pass
            #time.sleep(1)
            while not len(self.sistema.procesadores_terminaron) == 4:
                self.escucha_bus()
                #time.sleep(1)
            if self.sistema.ejecucion_continua == False:
                break
        print(F"M{self.id} finished ******************")
        return True
                