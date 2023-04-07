from Cache import *
from Memoria import *
from math import exp
import random

class Procesador:
    def __init__(self, id):
        self.id = id
        self.cache = Cache(4) 
    
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
    

    def generar_instruccion(self):
        resultado = self.poisson(5, 0, 2)
        if(resultado == 0):
            instruccion = self.generar_read()
            self.moesi(instruccion)
        elif(resultado == 1):
            instruccion = self.generar_write()
            self.moesi(instruccion)
        elif(resultado == 2):
            instruccion = self.generar_calc()
            self.moesi(instruccion)
        return instruccion
    
    def generar_read(self):
        direccion = self.poisson(10, 0, 7)
        instruccion = ["read", direccion]
        return instruccion
    
    def generar_write(self):
        direccion = self.poisson(10, 0, 7)
        dato = hex(self.poisson(100, 0, 65535))
        instruccion = ["write", direccion, dato]
        return instruccion

    def generar_calc(self):
        print("calc")
    
    def moesi(self, instruccion):
        if not isinstance(instruccion, list):
            return
        elif (instruccion[0] == "read"):
            self.cache.read_instruccion(instruccion)
        elif (instruccion[0] == "write"):
            self.cache.write_instruccion(instruccion)
