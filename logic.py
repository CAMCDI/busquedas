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
            # Operadores
            h1 = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            h2 = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            h3 = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]

            hijos = []
            for h_dato in [h1, h2, h3]:
                h = Nodo(h_dato)
                if not h.en_lista(nodos_visitados) and not h.en_lista(nodos_frontera):
                    nodos_frontera.append(h)
                    hijos.append(h)
            
            nodo.set_hijos(hijos)
    return None


# --- Algoritmo BFS (Búsqueda en Amplitud) ---
def buscar_solucion_bfs(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos() 
            # Operadores
            h1 = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            h2 = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            h3 = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]

            hijos = []
            for h_dato in [h1, h2, h3]:
                h = Nodo(h_dato)
                if not h.en_lista(nodos_visitados) and not h.en_lista(nodos_frontera):
                    nodos_frontera.append(h)
                    hijos.append(h)
            
            nodo.set_hijos(hijos)
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
