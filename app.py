from flask import Flask, render_template, request, jsonify
from logic import Nodo, buscar_solucion_dfs, buscar_solucion_ucs, buscar_solucion_heuristica, CONEXIONES_ST

app = Flask(__name__)

def parse_state(state_str):
    """Convierte una cadena como '4,2,3,1' en una lista de enteros."""
    try:
        return [int(x.strip()) for x in state_str.split(',')]
    except ValueError:
        return None

def get_path(nodo):
    """Obtiene la ruta desde el nodo solución hasta el inicial."""
    path = []
    curr = nodo
    while curr is not None:
        path.append(curr.get_datos())
        curr = curr.get_padre()
    path.reverse()
    return path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    alg = data.get('algorithm')
    start = data.get('start')
    goal = data.get('goal')

    if not alg or not start or not goal:
        return jsonify({'error': 'Faltan parámetros'}), 400

    result = None
    if alg == 'dfs':
        start_list = parse_state(start)
        goal_list = parse_state(goal)
        if start_list is None or goal_list is None:
            return jsonify({'error': 'Formato de estado inválido (use num,num,num,num)'}), 400
        result_node = buscar_solucion_dfs(start_list, goal_list)
        if result_node:
            result = {'path': get_path(result_node)}

    elif alg == 'ucs':
        # start y goal son nombres de ciudades
        result_node = buscar_solucion_ucs(start.lower(), goal.lower())
        if result_node:
            result = {
                'path': get_path(result_node),
                'cost': result_node.get_costo()
            }

    elif alg == 'heuristica':
        start_list = parse_state(start)
        goal_list = parse_state(goal)
        if start_list is None or goal_list is None:
            return jsonify({'error': 'Formato de estado inválido'}), 400
        
        nodo_inicial = Nodo(start_list)
        result_node = buscar_solucion_heuristica(nodo_inicial, goal_list, [])
        if result_node:
            result = {'path': get_path(result_node)}

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'No se encontró solución'}), 404

@app.route('/api/cities')
def get_cities():
    """Devuelve la lista de ciudades disponibles para UCS."""
    return jsonify(list(CONEXIONES_ST.keys()))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
