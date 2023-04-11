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
        self.bus = Bus()
        self.P0 = Procesador(0, self.bus, self)
        self.P1 = Procesador(1, self.bus, self)
        self.P2 = Procesador(2, self.bus, self)
        self.P3 = Procesador(3, self.bus, self)
        self.MemoriaP = Memoria(self.bus, self)
        self.ejecucion_continua = True
        self.pausa = False
        self.reanudar = False
        self.siguiente_paso = False
        

    def ejecutarHilos(self):
        # Crear cuatro hilos separados, cada uno ejecutando el método de una instancia diferente de la clase Procesador en paralelo
        
        threads = []
        for procesador in [self.P0, self.bus, self.MemoriaP, self.P1, self.P2, self.P3]:
            t = threading.Thread(target=procesador.run)
            threads.append(t)
            t.start()
        # Esperar a que todos los hilos terminen antes de continuar
        for t in threads:
            t.join()
            
    def run(self):
        
        self.ejecucion_continua = True # va a ser igual a variable de la interfaz grafica
        print("Ejecutando hilos...")
        self.ejecutarHilos()
        
        while self.sistema.siguiente_paso == False:
            self.sistema.siguiente_paso = input() # cambiar por variable de la interfaz grafica
            pass
        self.sistema.siguiente_paso = True


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
            #print(F"__{len(self.instrucciones)}__")
            #print(self.ack)
            if len(self.instrucciones) > 0:
                tipo = self.instrucciones[0][0]
                inst_id = self.instrucciones[0][1]
                if tipo == "WB":
                    if self.ack.count(999) >= 1:
                        self.clear_bus()
                elif tipo == "DR":
                    if self.ack.count(inst_id) > 0:
                        self.clear_bus()
                elif tipo == "IE":
                    if (self.ack.count(0) + self.ack.count(1) + self.ack.count(2) + self.ack.count(3)) >= 4:
                        self.clear_bus()
                elif tipo  == "RC":
                    if len(self.ack) ==  5:
                        self.clear_bus()
                        
            #time.sleep(0.5)
            #clear()
                
    def clear_bus(self):
        #print(F"Bus cleared instruction: {self.instrucciones[0]} | ACK: {self.ack}")
        self.instrucciones.pop(0)
        self.ack = []
        self.cache_returned = False
        
