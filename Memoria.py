from Sistema import *


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
        #self.bloques = [BloqueMem(i, "none", "*/") for i in range(8)]
        self.bus = bus
        self.sistema = sistema
        self.id = 999

    def escucha_bus(self):
        print("\n")
        print(F"Bus instrucciones: {self.bus.instrucciones}")
        print(F"Bus ack: {self.bus.ack}")
        print(F"P0 inst done: {self.sistema.P0.instruction_done} | Ultima inst: {self.sistema.P0.ultima_instruccion}")
        print(F"P1 inst done: {self.sistema.P1.instruction_done} | Ultima inst: {self.sistema.P1.ultima_instruccion}")
        print(F"P2 inst done: {self.sistema.P2.instruction_done} | Ultima inst: {self.sistema.P2.ultima_instruccion}")
        print(F"P3 inst done: {self.sistema.P3.instruction_done} | Ultima inst: {self.sistema.P3.ultima_instruccion}")
        if len(self.bus.instrucciones) > 0 and self.bus.ack.count(self.id) == 0:
            instruccion_bus = self.bus.instrucciones[0]
            #print(F"M{self.id} instruccion bus: {instruccion_bus}")
            id_respuesta = instruccion_bus[1]
            direccion = instruccion_bus[2]
            dato = instruccion_bus[3]
            if (instruccion_bus[0] == "WB" or instruccion_bus[0] == "IE"):
                self.write_back(dato, direccion)
                self.bus.ack.append(self.id)
                
            elif instruccion_bus[0] == "RC":
                # print(F"M{self.id} bus ack: {self.bus.ack}")
                # print(F"M{self.id} bus len len == 4: {len(self.bus.ack) == 4}")
                # print(F"M{self.id} bus cache returned == False: {self.bus.cache_returned == False}")

                if len(self.bus.ack) == 4 and self.bus.cache_returned == False: # CAMBIAR  >= 1 por == 4 para version final 
                    for bloque in self.bloques:
                        if direccion == bloque.dir:
                            instruccion = ["DR", id_respuesta, bloque.dir, bloque.data]
                            self.bus.instrucciones.append(instruccion)
                            self.bus.ack.append(self.id)
                            #print(F"DR Done: {instruccion}")
                            break
                elif len(self.bus.ack) == 4 and self.bus.cache_returned == True:
                    self.bus.ack.append(self.id)
            else:
                self.bus.ack.append(self.id)
            
        
    def write_back(self, dato, direccion):
        for bloque in self.bloques:
            if ( bloque.dir == direccion):
                bloque.data = dato
                break
                
    def run(self):
        while True:
            if self.sistema.pause:
                pass
            else:
                self.escucha_bus()
            #time.sleep(5)
            if self.sistema.ejecucion_continua == False:
                 print(F"M{self.id} finished")
                 return True
                