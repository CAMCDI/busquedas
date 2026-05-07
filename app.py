from flask import Flask, render_template, request, jsonify
from logic import buscar_solucion_dfs, buscar_solucion_bfs, buscar_solucion_heuristica, Nodo
import time

app = Flask(__name__)

def get_path_data(nodo):
    if not nodo:
        return None
    path = []
    curr = nodo
    while curr:
        path.append(curr.get_datos())
        curr = curr.get_padre()
    path.reverse()
    return path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compare', methods=['POST'])
def compare_searches():
    data = request.json
    try:
        start_state = [int(x) for x in data.get('start', '').split(',')]
        goal_state = [int(x) for x in data.get('goal', '').split(',')]
        requested_algos = data.get('algorithms', ['dfs', 'bfs', 'heuristic'])
        
        if len(start_state) != 4 or len(goal_state) != 4:
            return jsonify({"error": "Los estados deben tener 4 números separados por comas."}), 400
        
        results = {}

        # 1. DFS
        if 'dfs' in requested_algos:
            start_time = time.time()
            dfs_node = buscar_solucion_dfs(start_state, goal_state)
            results['dfs'] = {
                "path": get_path_data(dfs_node),
                "time": round((time.time() - start_time) * 1000, 2),
                "steps": len(get_path_data(dfs_node)) if dfs_node else 0
            }

        # 2. BFS
        if 'bfs' in requested_algos:
            start_time = time.time()
            bfs_node = buscar_solucion_bfs(start_state, goal_state)
            results['bfs'] = {
                "path": get_path_data(bfs_node),
                "time": round((time.time() - start_time) * 1000, 2),
                "steps": len(get_path_data(bfs_node)) if bfs_node else 0
            }

        # 3. Heuristic
        if 'heuristic' in requested_algos:
            start_time = time.time()
            heur_node = buscar_solucion_heuristica(Nodo(start_state), goal_state, [])
            results['heuristic'] = {
                "path": get_path_data(heur_node),
                "time": round((time.time() - start_time) * 1000, 2),
                "steps": len(get_path_data(heur_node)) if heur_node else 0
            }

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
