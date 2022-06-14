import threading
import time

capacidadCampo = {}
capacidadCampoFutura = {}
tiempoRestanteCapacidadCampoMinima = {}
recursosOcupados = {}

class MiHilo(threading.Thread):
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
        capacidadCampo[self.name] = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
        capacidadCampoFutura[self.name] = self.params['pendienteCurvaConsumo'] * (self.tActual+ self.params['dt']) + self.desplazamientoCurvaConsumo
        tiempoRestanteCapacidadCampoMinima[self.name] = self.tiempoCapacidadCampoMinima-self.tActual
        recursosOcupados[self.name] = False
        self.regar = False
        self.primeraVez = True
        self.x = []
        self.y = []
        self.xb = []
        self.yb = []
        self.w = []
        self.bottom = []
      
    def run_old(self):
        global recursosOcupados
        global capacidadCampo
        global tiempoRestanteCapacidadCampoMinima

        while self.periodoMedicion >= 0:
            if self.regar and not self.__recursoOcupado():
                self.__regando()
                if capacidadCampo[self.name] >= self.params['umbralSuperior'] or self.__recursoNecesitado():
                    print('Se dejó de regar ', self.name)
                    self.regar = False
                    recursosOcupados[self.name] = False
                    # self.__consumiendo()
            else:
                self.__consumiendo()
            
            self.__evaluarNecesidadRiego()
            self.__simulacion()
        pass

    def __regando(self):
        recursosOcupados[self.name] = True
        self.desplazamientoCurvaConsumo = capacidadCampo[self.name] - self.params['pendienteCurvaConsumo'] * self.tActual
        # self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        capacidadCampo[self.name] = self.params['pendienteCurvaRiego'] * self.tActual + self.desplazamientoCurvaRiego
        print('Regando ', self.name)
        pass

    def __consumiendo(self):
        # self.regar = False
        # recursosOcupados[self.name] = False
        capacidadCampo[self.name] = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
        # self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        print('Consumiendo ', self.name)
        pass

    def __evaluarNecesidadRiego(self):
        self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        tiempoRestanteCapacidadCampoMinima[self.name] = self.tiempoCapacidadCampoMinima-self.tActual
        if (self.__necesitaRegarse() and not self.regar):
            self.regar = True
            self.desplazamientoCurvaRiego = capacidadCampo[self.name] - self.params['pendienteCurvaRiego'] * self.tActual
        pass

    def __recursoOcupado(self):
        global recursosOcupados
        recursoOcupado =  False
        for key, value in recursosOcupados.items():
            if key != self.name:
                recursoOcupado = recursoOcupado or value
        return recursoOcupado
    
    def __recursoNecesitado(self):
        recursoNecesitado = False
        for key, value in capacidadCampo.items():
            #if key != self.name and (min(list(capacidadCampo.values())) == value or value < 0.5):
            if key != self.name and  value <= 0.5:
                recursoNecesitado = True
        return recursoNecesitado

    def __necesitaRegarse(self):
        # self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        tiempoRestanteCapacidadCampoMinima[self.name] = self.tiempoCapacidadCampoMinima-self.tActual
        # return min(list(tiempoRestanteCapacidadCampoMinima.values())) == tiempoRestanteCapacidadCampoMinima[self.name] and capacidadCampo[self.name] < self.params['umbralSuperior'] - 2.5 and not self.__recursoOcupado()
        # return min(list(tiempoRestanteCapacidadCampoMinima.values())) == tiempoRestanteCapacidadCampoMinima[self.name] and capacidadCampo[self.name] < self.params['umbralSuperior'] - 2.5  or capacidadCampo[self.name] < self.params['umbralInferior']
        # return min(list(tiempoRestanteCapacidadCampoMinima.values())) == tiempoRestanteCapacidadCampoMinima[self.name] or capacidadCampo[self.name] <= self.params['umbralInferior']
        return capacidadCampo[self.name] <= self.params['umbralInferior']

    def __simulacion(self):
        self.x.append(self.tActual)
        self.y.append(capacidadCampo[self.name])
        print('T ', self.tActual, ' name ', self.name, ' capacidadCampo ',list(capacidadCampo.values()), ' ocupados ', list(recursosOcupados.values()))
        self.periodoMedicion -= 1
        self.tActual += self.params['dt']
        time.sleep(0.001)
        pass

#  Codigo antiguo
    def run(self):
        global recursosOcupados
        global capacidadCampo
        global tiempoRestanteCapacidadCampoMinima
        global capacidadCampoFutura


        while self.periodoMedicion >= 0:
            # Si acaba de bajar de umbralSuperior o está muy cerca, pues ver si en realidad es necesario regar
            
            if self.regar and not self.__recursoOcupado_old():
                if (self.primeraVez):
                    self.xb.append(self.tActual-self.params['dt'])
                    xb = self.tActual-self.params['dt']
                    b = capacidadCampo[self.name]
                    self.primeraVez = False
                    self.bottom.append(capacidadCampo[self.name])
                    
                recursosOcupados[self.name] = True
                self.__calcularParamsRegar_old()
                print('Regando ', self.name, ' T ',self.tActual)
                capacidadCampoFutura[self.name] = self.params['pendienteCurvaRiego'] * (self.tActual+ self.params['dt']) + self.desplazamientoCurvaRiego
                
                if(capacidadCampoFutura[self.name] >= self.params['umbralSuperior'] or self.__recursoNecesitado_old() or self.periodoMedicion == 0):
                    print('Se dejó de regar ', self.name, ' T ',self.tActual)
                    self.regar = False
                    recursosOcupados[self.name] = False
                    self.primeraVez = True
                    self.w.append(self.tActual-xb)
                    self.yb.append(capacidadCampo[self.name] - b)

            elif (self.__necesitaRegarse_old() and not self.regar):
                #print('REGAR ', self.name)

                self.regar = True
                self.desplazamientoCurvaRiego = capacidadCampo[self.name] - self.params['pendienteCurvaRiego'] * self.tActual
                capacidadCampo[self.name] = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
                capacidadCampoFutura[self.name] = self.params['pendienteCurvaConsumo'] * (self.tActual + self.params['dt']) + self.desplazamientoCurvaConsumo

            else:
                capacidadCampo[self.name] = self.params['pendienteCurvaConsumo'] * self.tActual + self.desplazamientoCurvaConsumo
                capacidadCampoFutura[self.name] = self.params['pendienteCurvaConsumo'] * (self.tActual + self.params['dt']) + self.desplazamientoCurvaConsumo
                self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']

                # if (self.regar):
                #     self.desplazamientoCurvaRiego = capacidadCampo[self.name] - self.params['pendienteCurvaRiego'] * self.t

            tiempoRestanteCapacidadCampoMinima[self.name] = self.tiempoCapacidadCampoMinima-self.tActual
            self.x.append(self.tActual)
            self.y.append(capacidadCampo[self.name])


            self.periodoMedicion -= 1

            print('T ', self.tActual, ' name ', self.name, ' capacidadCampo ',list(capacidadCampo.values()), ' recurso ', list(recursosOcupados.values()), ' is needed ', self.__recursoNecesitado_old())

            self.tActual += self.params['dt']

            # print(recursosOcupados, 'T ', self.t, ' name ', self.name )
            #print('name', self.name, ' capacidadCampo: ',list(capacidadCampo.values()),' tiempoRestanteCapacidadCampoMinima: ',list(tiempoRestanteCapacidadCampoMinima.values()))
    
            # time.sleep(self.params['dt'])
            time.sleep(0.001)


    def __calcularParamsRegar_old(self):
        self.desplazamientoCurvaConsumo = capacidadCampo[self.name] - self.params['pendienteCurvaConsumo'] * self.tActual
        self.tiempoCapacidadCampoMinima = (0 - self.desplazamientoCurvaConsumo) / self.params['pendienteCurvaConsumo']
        
        capacidadCampo[self.name] = self.params['pendienteCurvaRiego'] * self.tActual + self.desplazamientoCurvaRiego

    def __recursoOcupado_old(self):
        global recursosOcupados
        recursoOcupado =  False
        for key, value in recursosOcupados.items():
            if key != self.name:
                recursoOcupado = recursoOcupado or value
        return recursoOcupado

    def __recursoNecesitado_old(self):
        recursoNecesitado = False
        for key, value in capacidadCampoFutura.items():
            #if key != self.name and (min(list(capacidadCampo.values())) == value or value < 0.5):
            if key != self.name and  value <= 0.5:
            # if key != self.name and  value <= 0:
                recursoNecesitado = True
        return recursoNecesitado

    def __necesitaRegarse_old(self):
        # return min(list(tiempoRestanteCapacidadCampoMinima.values())) == tiempoRestanteCapacidadCampoMinima[self.name] and capacidadCampo[self.name] < self.params['umbralSuperior'] - 2.5 and not self.__recursoOcupado()
        # return min(list(tiempoRestanteCapacidadCampoMinima.values())) == tiempoRestanteCapacidadCampoMinima[self.name] and capacidadCampo[self.name] < self.params['umbralSuperior'] - 2.5  or capacidadCampo[self.name] < self.params['umbralInferior']
        # return min(list(tiempoRestanteCapacidadCampoMinima.values())) == tiempoRestanteCapacidadCampoMinima[self.name] or capacidadCampo[self.name] < self.params['umbralInferior']
        return capacidadCampoFutura[self.name] <= self.params['umbralInferior']
     