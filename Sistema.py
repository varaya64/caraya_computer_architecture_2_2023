from Procesador import*
from math import exp
import threading
import time

class Sistema:
    def __init__(self):
        self.P0 = Procesador(0)
        self.P1 = Procesador(1)
        self.P2 = Procesador(2)
        self.P3 = Procesador(3)
        self.MemoriaP = Memoria()
        self.instrucciones_procesadores = [self.P0.instruccion_actual, self.P1.instruccion_actual, self.P2.instruccion_actual, self.P3.instruccion_actual]
        self.instrucciones_GUI = []

    
    
    def generateInstru(self, procesador):
        procesador.generar_instruccion()

    def ejecutarHilos(self):
        # Crear cuatro hilos separados, cada uno ejecutando el método de una instancia diferente de la clase Procesador en paralelo
        threads = []
        for procesador in [self.P0, self.P1, self.P2, self.P3]:
            t = threading.Thread(target=self.generateInstru, args=(procesador,))
            threads.append(t)
            t.start()
            #time.sleep(1)
        # Esperar a que todos los hilos terminen antes de continuar
        for t in threads:
            t.join()