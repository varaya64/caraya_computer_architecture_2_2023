from math import exp
import threading
import time
import random

import os
import sys
clear = lambda: os.system('cls')
from Sistema import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QRunnable, Qt, QThreadPool, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("test.ui", self)
        self.sistema = Sistema()
        self.boton_comenzar.clicked.connect(self.runTasks)
        self.boton_pausa.clicked.connect(self.pausar)
        self.boton_pausa.clicked.connect(self.reanudar)
        self.boton_siguiente.clicked.connect(self.siguiente_paso)
        self.sendInstru.clicked.connect(self.enviar_instruccion)
    
        self.dir_000.setText("000")
        self.dir_001.setText("001")
        self.dir_010.setText("010")
        self.dir_011.setText("011")
        self.dir_100.setText("100")
        self.dir_101.setText("101")
        self.dir_110.setText("110")
        self.dir_111.setText("111")
        
        self.instruccion1.setText("hola")
        self.actualizar_pantalla()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_pantalla)
        self.timer.start(100)  # Actualizar el texto cada 100 ms

    def runTasks(self):
        pool = QThreadPool.globalInstance()
        runnable = Runnable(self.sistema)
        pool.start(runnable)
    
    def enviar_instruccion(self):
        procesador = int(self.pInput.text())
        direccion = int(self.dirInput.text())
        dato = self.dataInput.text()
        operacion = self.opInput.text()
        
        comando = F"self.sistema.P{procesador}.instruccion_manual = ['{operacion}',{direccion},'{dato}',{procesador}]"
        
        print(comando)
        exec(comando)

    
    def siguiente_paso(self):
        self.sistema.ejecucion_continua = False
        self.runTasks()
    
    def pausar(self):
        self.sistema.ejecucion_continua = False
    
    def reanudar(self):
        self.sistema.ejecucion_continua = True
        
        
    def actualizar_pantalla(self):
        self.instruccion1.setText(str(self.sistema.P0.instruccion_actual))
        self.instruccion2.setText(str(self.sistema.P1.instruccion_actual))
        self.instruccion3.setText(str(self.sistema.P2.instruccion_actual))
        self.instruccion4.setText(str(self.sistema.P3.instruccion_actual))
        self.instruccionMem.setText(str(self.sistema.MemoriaP.instruccion_actual))
        
        self.anterior_P0.setText(str(self.sistema.P0.instruccion_anterior))
        self.anterior_P1.setText(str(self.sistema.P1.instruccion_anterior))
        self.anterior_P2.setText(str(self.sistema.P2.instruccion_anterior))
        self.anterior_P3.setText(str(self.sistema.P3.instruccion_anterior))
        
        #Actualiza datos de memoria
        self.dato_000.setText(str(self.sistema.MemoriaP.bloques[0].data))
        self.dato_001.setText(str(self.sistema.MemoriaP.bloques[1].data))
        self.dato_010.setText(str(self.sistema.MemoriaP.bloques[2].data))
        self.dato_011.setText(str(self.sistema.MemoriaP.bloques[3].data))
        self.dato_100.setText(str(self.sistema.MemoriaP.bloques[4].data))
        self.dato_101.setText(str(self.sistema.MemoriaP.bloques[5].data))
        self.dato_110.setText(str(self.sistema.MemoriaP.bloques[6].data))
        self.dato_111.setText(str(self.sistema.MemoriaP.bloques[7].data))
        
        #Actualiza estados del Bloque 0
        self.estado_B0_P1.setText(str(self.sistema.P0.cache.bloques[0].state))
        self.estado_B0_P2.setText(str(self.sistema.P1.cache.bloques[0].state))
        self.estado_B0_P3.setText(str(self.sistema.P2.cache.bloques[0].state))
        self.estado_B0_P4.setText(str(self.sistema.P3.cache.bloques[0].state))
        
        #Actualiza estados del Bloque 1
        self.estado_B1_P1.setText(str(self.sistema.P0.cache.bloques[1].state))
        self.estado_B1_P2.setText(str(self.sistema.P1.cache.bloques[1].state))
        self.estado_B1_P3.setText(str(self.sistema.P2.cache.bloques[1].state))
        self.estado_B1_P4.setText(str(self.sistema.P3.cache.bloques[1].state))
        
        #Actualiza estados del Bloque 2
        self.estado_B2_P1.setText(str(self.sistema.P0.cache.bloques[2].state))
        self.estado_B2_P2.setText(str(self.sistema.P1.cache.bloques[2].state))
        self.estado_B2_P3.setText(str(self.sistema.P2.cache.bloques[2].state))
        self.estado_B2_P4.setText(str(self.sistema.P3.cache.bloques[2].state))
        
        #Actualiza estados del Bloque 3
        self.estado_B3_P1.setText(str(self.sistema.P0.cache.bloques[3].state))
        self.estado_B3_P2.setText(str(self.sistema.P1.cache.bloques[3].state))
        self.estado_B3_P3.setText(str(self.sistema.P2.cache.bloques[3].state))
        self.estado_B3_P4.setText(str(self.sistema.P3.cache.bloques[3].state))
        
        #Actualiza direcciones del Bloque 0
        self.dir_B0_P1.setText(str(self.sistema.P0.cache.bloques[0].dir))
        self.dir_B0_P2.setText(str(self.sistema.P1.cache.bloques[0].dir))
        self.dir_B0_P3.setText(str(self.sistema.P2.cache.bloques[0].dir))
        self.dir_B0_P4.setText(str(self.sistema.P3.cache.bloques[0].dir))
        
        #Actualiza direcciones del Bloque 1
        self.dir_B1_P1.setText(str(self.sistema.P0.cache.bloques[1].dir))
        self.dir_B1_P2.setText(str(self.sistema.P1.cache.bloques[1].dir))
        self.dir_B1_P3.setText(str(self.sistema.P2.cache.bloques[1].dir))
        self.dir_B1_P4.setText(str(self.sistema.P3.cache.bloques[1].dir))
        
        #Actualiza direcciones del Bloque 2
        self.dir_B2_P1.setText(str(self.sistema.P0.cache.bloques[2].dir))
        self.dir_B2_P2.setText(str(self.sistema.P1.cache.bloques[2].dir))
        self.dir_B2_P3.setText(str(self.sistema.P2.cache.bloques[2].dir))
        self.dir_B2_P4.setText(str(self.sistema.P3.cache.bloques[2].dir))
        
        #Actualiza direcciones del Bloque 3
        self.dir_B3_P1.setText(str(self.sistema.P0.cache.bloques[3].dir))
        self.dir_B3_P2.setText(str(self.sistema.P1.cache.bloques[3].dir))
        self.dir_B3_P3.setText(str(self.sistema.P2.cache.bloques[3].dir))
        self.dir_B3_P4.setText(str(self.sistema.P3.cache.bloques[3].dir))
        
        #Actualiza datos del Bloque 0
        self.dato_B0_P1.setText(str(self.sistema.P0.cache.bloques[0].data))
        self.dato_B0_P2.setText(str(self.sistema.P1.cache.bloques[0].data))
        self.dato_B0_P3.setText(str(self.sistema.P2.cache.bloques[0].data))
        self.dato_B0_P4.setText(str(self.sistema.P3.cache.bloques[0].data))
        
        #Actualiza datos del Bloque 1
        self.dato_B1_P1.setText(str(self.sistema.P0.cache.bloques[1].data))
        self.dato_B1_P2.setText(str(self.sistema.P1.cache.bloques[1].data))
        self.dato_B1_P3.setText(str(self.sistema.P2.cache.bloques[1].data))
        self.dato_B1_P4.setText(str(self.sistema.P3.cache.bloques[1].data))
        
        #Actualiza datos del Bloque 2
        self.dato_B2_P1.setText(str(self.sistema.P0.cache.bloques[2].data))
        self.dato_B2_P2.setText(str(self.sistema.P1.cache.bloques[2].data))
        self.dato_B2_P3.setText(str(self.sistema.P2.cache.bloques[2].data))
        self.dato_B2_P4.setText(str(self.sistema.P3.cache.bloques[2].data))
        
        #Actualiza datos del Bloque 3
        self.dato_B3_P1.setText(str(self.sistema.P0.cache.bloques[3].data))
        self.dato_B3_P2.setText(str(self.sistema.P1.cache.bloques[3].data))
        self.dato_B3_P3.setText(str(self.sistema.P2.cache.bloques[3].data))
        self.dato_B3_P4.setText(str(self.sistema.P3.cache.bloques[3].data))
        
        #Actualiza datos del Bloque 3
        self.miss_P0.setText(str(self.sistema.P0.miss))
        self.miss_P1.setText(str(self.sistema.P1.miss))
        self.miss_P2.setText(str(self.sistema.P2.miss))
        self.miss_P3.setText(str(self.sistema.P3.miss))


class Runnable(QRunnable):
    def __init__(self, sistema):
        super().__init__()
        self.sistema = sistema

    def run(self):
        self.sistema.run()

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    