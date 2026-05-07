class Nodo:
    def __init__(self, datos, hijos=None):
        self.datos = datos
        self.hijos = None
        self.padre = None
        self.costo = None
    
    def set_hijos(self, hijos):
        self.hijos = hijos 
        if self.hijos != None:
            for h in self.hijos:
                h.padre = self
    
    def get_hijos(self):
        return self.hijos

    def get_padre(self):
        return self.padre
    
    def set_padre(self, padre):
        self.padre = padre

    def set_datos(self, datos):
        self.datos = datos

    def get_datos(self):
        return self.datos
    
    def set_costo(self, costo):
        self.costo = costo

    def get_costo(self):
        return self.costo
    
    def igual(self, nodo):
        return self.get_datos() == nodo.get_datos()
        
    def en_lista(self, lista_nodos):
        for n in lista_nodos:
            if self.igual(n):
               return True
        return False
    
    def __str__(self):
        return str(self.get_datos())


# --- Algoritmo DFS (Búsqueda en Profundidad) ---
def buscar_solucion_dfs(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop()
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos() 
            # Operador izquierdo 
            hijo_1 = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izq = Nodo(hijo_1)
            # operador central
            hijo_2 = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_cen = Nodo(hijo_2)
            # Operador derecho
            hijo_3 = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_der = Nodo(hijo_3)

            hijos = []
            for h in [hijo_izq, hijo_cen, hijo_der]:
                if not h.en_lista(nodos_visitados) and not h.en_lista(nodos_frontera):
                    nodos_frontera.append(h)
                    hijos.append(h)
            
            nodo.set_hijos(hijos)
    return None


# --- Algoritmo UCS (Búsqueda de Costo Uniforme) ---
CONEXIONES_ST = {
    'jiloyork':{'cdmx':125, 'queretaro':513},
    'morelos':{'queretaro':524},
    'cdmx':{'jiloyork':125, 'queretaro':423, 'hidalgo':491},
    'hidalgo':{'cdmx':491, 'queretaro':356, 'mexicali':309, 'monterrey':346},
    'queretaro':{'slp':203, 'morelos':514, 'jiloyork':513, 'cdmx':423, 'monterrey':603, 'sonora':437, 'hidalgo':356,'mexicali':313, 'ags':599},
    'slp':{'ags':390, 'queretaro':203},
    'ags':{'slp':390, 'queretaro':599},
    'sonora':{'queretaro':437, 'mexicali':394},
    'mexicali':{'monterrey':296, 'hidalgo':309, 'queretaro':313},
    'monterrey':{'mexicali':296, 'queretaro':603, 'hidalgo':346}
}

def buscar_solucion_ucs(estado_inicial, solucion, conexiones=CONEXIONES_ST):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []

    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)
    
    while not solucionado and len(nodos_frontera) != 0:
        nodos_frontera = sorted(nodos_frontera, key=lambda x: x.get_costo())
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo 
        else:
            dato_nodo = nodo.get_datos()
            if dato_nodo not in conexiones:
                continue
                
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                costo = conexiones[dato_nodo][un_hijo]
                hijo.set_costo(nodo.get_costo() + costo)
                lista_hijos.append(hijo)

                if not hijo.en_lista(nodos_visitados):
                    if hijo.en_lista(nodos_frontera):
                        for n in nodos_frontera:
                            if n.igual(hijo) and n.get_costo() > hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                    else:
                        nodos_frontera.append(hijo)
            nodo.set_hijos(lista_hijos)
    return None


# --- Algoritmo Heurístico (Hill Climbing) ---
def mejora(nodo_padre, nodo_hijo):
    calidad_padre = 0
    calidad_hijo = 0
    dato_padre = nodo_padre.get_datos()
    dato_hijo = nodo_hijo.get_datos()

    for n in range(1, len(dato_padre)):
        if (dato_padre[n] > dato_padre[n-1]):
            calidad_padre += 1
        if (dato_hijo[n] > dato_hijo[n-1]):
            calidad_hijo += 1

    return calidad_hijo >= calidad_padre

def buscar_solucion_heuristica(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        dato_nodo = nodo_inicial.get_datos()
        
        # Generar hijos
        h1 = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        h2 = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        h3 = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        
        hijos = [Nodo(h1), Nodo(h2), Nodo(h3)]
        nodo_inicial.set_hijos(hijos)

        for nodo_hijo in nodo_inicial.get_hijos():
            if not nodo_hijo.get_datos() in visitados and mejora(nodo_inicial, nodo_hijo):
                sol = buscar_solucion_heuristica(nodo_hijo, solucion, visitados)
                if sol != None:
                    return sol
        return None
