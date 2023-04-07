from Cache import *
from Memoria import *
from math import exp
import random

class Procesador:
    def __init__(self, id):
        self.id = id
        self.cache = Cache() 
    
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

    def selectInstr(self):
        resultado = self.poisson(5, 0, 2)
        if(resultado == 0):
            instruccion = self.read("read")
            print(instruccion)
        elif(resultado == 1):
            instruccion = self.write("write")
            print(instruccion)
        elif(resultado == 2):
            instruccion = self.calc("calc")
            print(instruccion)
        return instruccion
    
    def read(self, typeInstr):
        direccion = self.poisson(10, 0, 7)
        instruccion = [typeInstr, direccion]
        return instruccion
    
    def write(self, typeInstr):
        direccion = self.poisson(10, 0, 7)
        dato = hex(self.poisson(100, 0, 65535))
        instruccion = [typeInstr, direccion, dato]
        return instruccion

    def calc(self, typeInstr):
        instruccion = typeInstr
        return instruccion
    
    def moesi(self):
        instruccion = self.selectInstr
        if not isinstance(instruccion, list):
            return
        elif (instruccion[0] == "read"):
            print("read")
        elif (instruccion[0] == "write"):
            print("write")

