from Cache import *
from Memoria import *
from Sistema import *
from math import exp
import random

"""
Clase del Procesador
"""
class Procesador:
    def __init__(self, id, bus, sistema):
        self.id = id
        self.cache = Cache(4)
        self.bus = bus
        self.sistema = sistema
        self.ultima_instruccion = F"{self.id} hola esta es mi instruccion"
        self.instruction_done = True
        self.num_instrucciones = 0

    
    #Metodo de probabilidad Poisson
    def poisson(self, lmbd, a, b):
        L = exp(-lmbd)
        k = 0
        p = 1
        while p > L:
            k = k + 1
            u = random.uniform(0, 1)
            p = p * u
        resultado = k - 1
        resultado = int(a + resultado * (b - a) / lmbd)
        while resultado < a or resultado > b:
            resultado = int(a + random.uniform(0, 1) * (b - a) / lmbd)
        return resultado
    
    #Generar instrucciones de forma aleatoria
    
    def generar_instruccion(self):
        tipo_instruccion = self.poisson(5, 0, 2)
        
        # If para read
        if(tipo_instruccion == 0):
            instruccion = self.generar_read()
            
        
        #If para write
        elif(tipo_instruccion == 1):
            instruccion = self.generar_write()
            
            
        #Instruccion de tipo calc
        elif(tipo_instruccion == 2):
            instruccion = self.generar_calc()
        
        instruccion.append(self.id)
        return instruccion
    
    #Genera Instruccion Read
    def generar_read(self):
        direccion = self.poisson(10, 0, 7)
        instruccion = ["read", direccion,0]
        return instruccion
    
    #Genera Instruccion Write
    def generar_write(self):
        direccion = self.poisson(10, 0, 7)
        dato = hex(self.poisson(100, 0, 65535))
        instruccion = ["write", direccion, dato]
        return instruccion

    #Genera Instruccion CALC
    def generar_calc(self):
        return ["calc",0,0]
        
    
    def procesar_instruccion(self,instruccion):
        # print("FP{self.id} procesando {instruccion}")
        self.ultima_instruccion = instruccion
        tipo = instruccion[0]
        self.instruction_done = False
        
        if tipo == "read":
            resultado = self.cache.read_instruccion(instruccion)
            if resultado[0] == "done":
                self.instruction_done = True
                #print(F"P{self.id} Read done")
            else:
                self.bus.instrucciones.append(resultado)
            
        elif tipo == "write":
            resultado = self.cache.write_instruccion(instruccion)
            if resultado[0] == "done":
                self.instruction_done = True
                #print(F"P{self.id} Write done")
            else:
                self.bus.instrucciones.append(resultado)
                self.instruction_done = True
                
        elif tipo == "calc":
            #print(F"P{self.id} Calc done")
            self.instruction_done = True
        

    def escuchar_bus(self):
        if len(self.bus.instrucciones) > 0 and self.bus.ack.count(self.id) == 0:
            instruccion_bus = self.bus.instrucciones[0]
            instruccion_id = instruccion_bus[1]
            direccion = instruccion_bus[2]
            dato = instruccion_bus[3]
            if instruccion_id != self.id:
                if instruccion_bus[0] == "IE":
                    self.cache.invalidar_bloque(direccion)
                    self.bus.ack.append(self.id)
            
                elif instruccion_bus[0] == "RC":
                    data = self.cache.actualizar_bloque(direccion)
                    if data != None:
                        instruccion = ["DR", instruccion_id, direccion, data]
                        self.bus.instrucciones.append(instruccion)
                        self.bus.cache_returned = True
                    self.bus.ack.append(self.id)  
                
                else:
                    self.bus.ack.append(self.id) 
            
            elif instruccion_bus[0] == "DR":
                instruccion = ["write", direccion, dato, self.id]
                self.instruccion_done = True
                self.procesar_instruccion(instruccion)
                self.bus.ack.append(self.id)
            
            else:
                self.bus.ack.append(self.id)

        
    
    def run(self):
        while True:
            if self.sistema.pausa:
                pass
            else:
                instruccion = self.generar_instruccion()
                #print(F"P{self.id} procesando instruccion: {instruccion}")
                # for bloque in self.cache.bloques: print(F"P{self.id} Bloque antes->{bloque.id} {bloque.state} {bloque.dir} {bloque.data}")
                self.procesar_instruccion(instruccion)
                self.num_instrucciones += 1
                #print(F"____ P{self.id} ni: {self.num_instrucciones}")
                # for bloque in self.cache.bloques: print(F"P{self.id} Bloque despues->{bloque.id} {bloque.state} {bloque.dir} {bloque.data}")
                while not self.instruction_done:
                    self.escuchar_bus()
            if self.sistema.ejecucion_continua == False:
                #print(F"P{self.id} finished ******************")
                return True
                
            