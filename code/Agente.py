import re
import threading
import time
import numpy

tiempoRestanteCapacidadCampoMinima = {}
recursoOcupado = ""
recursosSolicitados = {}

class Agente(threading.Thread):
    # contador = 100
    params = {
        'pendienteCurvaConsumo': -0.5,
        'pendienteCurvaRiego': 0.8,
        'umbralSuperior':3.5,
        'umbralInferior':0.5,
        'dt':0.5,
        'humedadInicial': 2
    }

    tActual = 0
   
    def __init__(self, args=(), group=None, target=None, name=None, daemon=None, **kwargs):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.params = kwargs['kwargs']
        self.periodoMedicion = args[0]
        self.desplazamientoCurvaConsumo = self.params['humedadInicial'] - self.params['pendienteCurvaConsumo'] * self.tActual
        # self.t = (self.params['humedadInicial'] - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        tiempoRestanteCapacidadCampoMinima[self.name] = self.tiempoCapacidadCampoMinima-self.tActual
        recursosSolicitados[self.name] = 0
        self.primeraVez = True
        self.x = []
        self.y = []
        self.xb = []
        self.yb = []
        self.w = []
        self.bottom = []
        self.capacidadCampo = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
        self.capacidadCampoFutura = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
        self.ur = self.params['umbralSuperior'] -self.params['umbralInferior'] / 2

    def run(self):
        global recursoOcupado
        global recursosSolicitados
        global tiempoRestanteCapacidadCampoMinima
        

        while self.periodoMedicion >= 0:

            if recursoOcupado != self.name:
                self.consumir()

                self.actualizarRecursosSolicitados()

                if self.regarse():
                    print('me voy a regar ', self.name)
                    # self.desplazamientoCurvaRiego = - self.tActual
                    recursoOcupado = self.name
                    recursosSolicitados[self.name] = 0
                    self.desplazamientoCurvaRiego = self.capacidadCampo - self.params['pendienteCurvaRiego'] * self.tActual

            else:
                self.regar()
                
                if self.parar():
                    self.desplazamientoCurvaConsumo = - self.tActual
                    print('me voy a dejar de regar ', self.name)
                    recursoOcupado = ""

            self.simulacion()


    def actualizarRecursosSolicitados(self):
        if self.capacidadCampo <= self.params['umbralInferior']:
            recursosSolicitados[self.name] += 1


    def consumir(self):
        # self.capacidadCampo = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
        self.capacidadCampo =self.consumoLogaritmico(self.params['pendienteCurvaConsumo'], self.tActual, self.desplazamientoCurvaConsumo)
        # self.capacidadCampoFutura = self.params['pendienteCurvaConsumo'] * (self.tActual + self.params['dt']) + self.desplazamientoCurvaConsumo
        self.capacidadCampoFutura =  self.consumoLogaritmico(self.params['pendienteCurvaConsumo'], self.tActual + self.params['dt'], self.desplazamientoCurvaConsumo)
        self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']


    def regarse(self):
        print('max ',max(recursosSolicitados.values()), 'recursoOcupado ', recursoOcupado)
        return recursosSolicitados[self.name] != 0 and recursosSolicitados[self.name] == max(recursosSolicitados.values()) and recursoOcupado == ""
    

    def regar(self):
        # self.desplazamientoCurvaConsumo = self.capacidadCampo - self.params['pendienteCurvaConsumo'] * self.tActual
        # self.desplazamientoCurvaConsumo = - self.tActual
        self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        self.capacidadCampoFutura = self.params['pendienteCurvaRiego'] * (self.tActual+ self.params['dt']) + self.desplazamientoCurvaRiego
        # self.capacidadCampoFutura = self.f(self.params['pendienteCurvaRiego'], self.tActual + self.params['dt'], self.desplazamientoCurvaRiego)
        # self.capacidadCampo = self.f(self.params['pendienteCurvaRiego'], self.tActual, self.desplazamientoCurvaRiego)
        self.capacidadCampo = self.params['pendienteCurvaRiego'] * self.tActual + self.desplazamientoCurvaRiego

    def parar(self):
        return (max(recursosSolicitados.values()) > 0 and self.capacidadCampo >= self.ur) or self.capacidadCampo >= self.params['umbralSuperior']


    def simulacion(self):
        self.x.append(self.tActual)
        self.y.append(self.capacidadCampo)
        self.periodoMedicion -= 1
        print('T ', self.tActual, ' name ', self.name, ' capacidadCampo ',self.capacidadCampo, ' solicitado ', recursosSolicitados.values())
        self.tActual += self.params['dt']
       
        time.sleep(0.001)

    def consumoLogaritmico(self, m, t, desplazamiento):
        return m * numpy.log(t + desplazamiento) + self.params['umbralSuperior']