# from tkinter import Tcl
import numpy as np
import matplotlib.pyplot as plt
from Agente import *

# la h0 nos dice que no inicia en tiempo 0
# sacar el tiempo en el que va. t1
# ya con ese tiempo y con el tiempo al poner 0 en H = mt + n. nos da el t2
# t2-t1. tiempo en el que estará en 0. T0cc

# cc = self.params['m'] * self.t + self.n. cambiando la t cada vez.

def graficar(x, y, ax):
  # x = np.array(x)
  # y = np.array(y)

  ax.plot(x, y)

def graficarB(x,y,w,b):
  plt.bar(x, height=y, width=w,align='edge',bottom=b,color='#ECDEFF')
  # plt.bar(x, height=y, width=w,align='edge',color='black')
  

params = {
  'pendienteCurvaConsumo': -1,
  'pendienteCurvaRiego': 0.98,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 2
}

params2 = {
  'pendienteCurvaConsumo': -1.1,
  'pendienteCurvaRiego': 0.95,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

params3 = {
  'pendienteCurvaConsumo': -1.2,
  'pendienteCurvaRiego': 0.9,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3
}

params4 = {
  'pendienteCurvaConsumo': -1.25,
  'pendienteCurvaRiego': 0.9,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 4
}

params5 = {
  'pendienteCurvaConsumo': -1.15,
  'pendienteCurvaRiego': 0.9,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}
params6 = {
  'pendienteCurvaConsumo': -1,
  'pendienteCurvaRiego': 0.98,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 2
}

params7 = {
  'pendienteCurvaConsumo': -1.1,
  'pendienteCurvaRiego': 0.95,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

params8 = {
  'pendienteCurvaConsumo': -1.2,
  'pendienteCurvaRiego': 0.9,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3
}

params9 = {
  'pendienteCurvaConsumo': -1.25,
  'pendienteCurvaRiego': 0.9,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 4
}

params10 = {
  'pendienteCurvaConsumo': -1.15,
  'pendienteCurvaRiego': 0.9,
  'umbralSuperior':3.5,
  'umbralInferior':0.5,
  'dt':0.5,
  'humedadInicial': 3.5
}

periodoMedicion = 200
nHilos = 7
parametros = [params, params2, params3, params4, params5,params6, params7, params8, params9, params10]
hilos = []

for i in range(nHilos):
  hilos.append(Agente(daemon=False,args=(periodoMedicion,), kwargs=parametros[i]))
  
for idxHilo in range(nHilos):
  hilos[idxHilo].start()

for idxHilo in range(nHilos):
  hilos[idxHilo].join()


fig = plt.figure(figsize=(20, 2))
ax = fig.add_subplot(111)

for idxHilo in range(nHilos):
  graficar(hilos[idxHilo].x, hilos[idxHilo].y, ax)
#   graficarB(hilos[idxHilo].xb, hilos[idxHilo].yb,hilos[idxHilo].w,hilos[idxHilo].bottom)


dt = 0.5

allTime = np.arange(0,periodoMedicion*dt,dt)
uiLine = np.full(periodoMedicion,0.5)
usLine = np.full(periodoMedicion,3.5)



ax.plot(allTime, uiLine)
ax.plot(allTime, usLine)

path = 'Graficas/'
name = 'Bar 7 hilos'

plt.savefig(path + name)
