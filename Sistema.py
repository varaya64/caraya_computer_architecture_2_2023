from Procesador import*
from Memoria import *
from math import exp
import threading
import time

class Sistema:
    def __init__(self):
        self.bus = Bus()
        self.P0 = Procesador(0, self.bus, self)
        self.P1 = Procesador(1, self.bus, self)
        self.P2 = Procesador(2, self.bus, self)
        self.P3 = Procesador(3, self.bus, self)
        self.MemoriaP = Memoria(self.bus, self)
        self.ejecucion_continua = True
        self.pause = False
        self.siguiente_paso = False
        
        
        
           
    def generateInstru(self, procesador):
        procesador.generar_instruccion()
        resultado = procesador.generar_instruccion()

    def ejecutarHilos(self):
        # Crear cuatro hilos separados, cada uno ejecutando el método de una instancia diferente de la clase Procesador en paralelo
        threads = []
        for procesador in [self.bus, self.MemoriaP, self.P0, self.P1, self.P2, self.P3]:
            t = threading.Thread(target=procesador.run)
            threads.append(t)
            t.start()
            time.sleep(1)
        # Esperar a que todos los hilos terminen antes de continuar
        for t in threads:
            t.join()

"""
Clase del Bus de datos
"""

class Bus:
    def __init__(self):
        self.instrucciones = []
        self.ack = []
        self.cache_returned = False
        
    def run(self):     
        while True:
            if len(self.ack) ==  5:
                print(F"Bus cleared instruction: {self.instrucciones[0]} | ACK: {self.ack}")
                self.instrucciones.pop(0)
                self.ack = []
                self.cache_returned = False
                