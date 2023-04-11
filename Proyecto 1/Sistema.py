from Procesador import*
from Memoria import *
from math import exp
import threading
import time

"""
Clase del sistema
"""
class Sistema:
    def __init__(self):
        self.bus = Bus(self)
        self.P0 = Procesador(0, self.bus, self)
        self.P1 = Procesador(1, self.bus, self)
        self.P2 = Procesador(2, self.bus, self)
        self.P3 = Procesador(3, self.bus, self)
        self.MemoriaP = Memoria(self.bus, self)
        self.procesadores_comenzaron = []
        self.procesadores_terminaron = []
        self.ejecucion_continua = False
        self.pausa = False
        self.reanudar = False
        self.siguiente_paso = False
        

    def ejecutarHilos(self):
        # Crear cuatro hilos separados, cada uno ejecutando el método de una instancia diferente de la clase Procesador en paralelo
        
        threads = []
        for procesador in [self.bus, self.P0, self.P1, self.P2, self.P3, self.MemoriaP]:
            t = threading.Thread(target=procesador.run)
            threads.append(t)
            t.start()
            
        # Esperar a que todos los hilos terminen antes de continuar
        for t in threads:
            t.join()
            
        print("Termino ejecutar hilos...")
        return True
            
    def run(self):
        while True:
            print("Ejecutando hilos...")
            self.procesadores_terminaron = []
            self.procesadores_comenzaron = []
            time.sleep(1)
            self.ejecutarHilos()
            time.sleep(1)
            if self.ejecucion_continua == False:
                return True
        


"""
Clase del Bus de datos
"""

class Bus:
    def __init__(self, sistema):
        self.instrucciones = []
        self.ack = []
        self.cache_returned = False
        self.sistema = sistema
        
    def run(self):
        while True:
            #print(F"Bus inicio en thread {threading.get_ident()}")
            #time.sleep(0.5)
            while not len(self.sistema.procesadores_terminaron) == 4:
                if len(self.instrucciones) > 0:
                    if len(self.ack) == 5:
                        self.clear_bus()
                #time.sleep(0.5)
            if self.sistema.ejecucion_continua == False:
                break
            break
        print("Bus finished ******************")
        return True 
                
    def clear_bus(self):
        #print(F"Bus: {self.instrucciones}")
        #print(F"Bus cleared instruction: {self.instrucciones[0]} | ACK: {self.ack}")
        self.instrucciones.pop(0)
        self.ack = []
        self.cache_returned = False
        
        