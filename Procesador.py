from Cache import *
from Memoria import *
from math import exp
import random

class Procesador:
    def __init__(self, id):
        self.id = id
        self.cache = Cache(4)
        self.instrucciones = []
        self.instruccion_actual = []
        self.flag_read_miss = False
        self.flag_write_miss = False
        self.flag_inst = False
        self.flag_WB = False
        self.flag_IE = False
        
    
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
        resultado = self.poisson(5, 0, 2)
        
        if(resultado == 0):
            instruccion= self.generar_read()
            self.instrucciones.append(instruccion)
            #self.moesi(instruccion)
        
        elif(resultado == 1):
            instruccion = self.generar_write()
            self.instrucciones.append(instruccion)
            #self.moesi(instruccion)
        
        elif(resultado == 2):
            instruccion = self.generar_calc()
            self.instrucciones.append(instruccion)
            #self.moesi(instruccion)
        
        print("Instrucciones del procesador " + str(self.id) + " " + str(self.instrucciones))
        return instruccion
    

    #Genera Instruccion Read
    def generar_read(self):
        flag_inst = True
        direccion = self.poisson(10, 0, 7)
        instruccion = ["read", direccion]
        self.instruccion_actual = instruccion
        return instruccion
    
    #Genera Instruccion Write
    def generar_write(self):
        direccion = self.poisson(10, 0, 7)
        dato = hex(self.poisson(100, 0, 65535))
        instruccion = ["write", direccion, dato]
        self.instruccion_actual = instruccion
        return instruccion

    
    #Genera Instruccion CALC
    def generar_calc(self):
        flag_inst = True
        self.instruccion_actual = ["calc"]
        return self.instruccion_actual
    
    def validar_resultado_write(self, resultado):
        if (resultado == "done"):
            self.flag_inst = False
            self.instruccion_actual = []
        elif (resultado == "WB"):
            print("se debe escribir en memoria")
        elif isinstance(resultado, list):
            print("Se debe hacer WB e invalidacion por escritura")

    def validar_resultado_write(self, resultado):
        print("Resultado")
    
    #Invoca el MOESI
    def moesi(self, instruccion):
        if not isinstance(instruccion, list):
            return
        elif (instruccion[0] == "read"):
            resultado = self.cache.read_instruccion(instruccion)
            self.validar_resultado_read(resultado)
        elif (instruccion[0] == "write"):
            resultado = self.cache.write_instruccion(instruccion)
            self.validar_resultado_write(resultado)
