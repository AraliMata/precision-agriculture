# from tkinter import Tcl
import numpy as np
import matplotlib.pyplot as plt
from MiHilo import *

# la h0 nos dice que no inicia en tiempo 0
# sacar el tiempo en el que va. t1
# ya con ese tiempo y con el tiempo al poner 0 en H = mt + n. nos da el t2
# t2-t1. tiempo en el que estará en 0. T0cc

# cc = self.params['m'] * self.t + self.n. cambiando la t cada vez.

def graficar(x, y):
  # x = np.array(x)
  # y = np.array(y)
  plt.plot(x, y)

def graficarB(x,y,w,b):
  plt.bar(x, height=y, width=w,align='edge',bottom=b,color='#ECDEFF')
  # plt.bar(x, height=y, width=w,align='edge',color='black')
  

params = {
  'pendienteCurvaConsumo': -0.5,
  'pendienteCurvaRiego': 0.8,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 2
}

params2 = {
  'pendienteCurvaConsumo': -0.4,
  'pendienteCurvaRiego': 0.8,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

params3 = {
  'pendienteCurvaConsumo': -0.3,
  'pendienteCurvaRiego': 0.8,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

params4 = {
  'pendienteCurvaConsumo': -0.3,
  'pendienteCurvaRiego': 0.8,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

params5 = {
  'pendienteCurvaConsumo': -0.3,
  'pendienteCurvaRiego': 0.8,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

periodoMedicion = 100
nHilos = 2
parametros = [params, params2, params3, params4, params5]
hilos = []

for i in range(nHilos):
  hilos.append(MiHilo(daemon=False,args=(periodoMedicion,), kwargs=parametros[i]))
  
for idxHilo in range(nHilos):
  hilos[idxHilo].start()

for idxHilo in range(nHilos):
  hilos[idxHilo].join()


for idxHilo in range(nHilos):
  graficar(hilos[idxHilo].x, hilos[idxHilo].y)
  graficarB(hilos[idxHilo].xb, hilos[idxHilo].yb,hilos[idxHilo].w,hilos[idxHilo].bottom)


dt = 0.5

allTime = np.arange(0,periodoMedicion*dt,dt)
uiLine = np.full(periodoMedicion,0.5)
usLine = np.full(periodoMedicion,3.5)

plt.plot(allTime, uiLine)
plt.plot(allTime, usLine)

path = 'Graficas/'
name = 'Bar'

plt.savefig(path + name)
