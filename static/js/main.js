document.addEventListener('DOMContentLoaded', () => {
    const solveBtn = document.getElementById('solve-btn');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');
    const errorContainer = document.getElementById('error-container');

    // Inputs
    const startStateInput = document.getElementById('start-state');
    const goalStateInput = document.getElementById('goal-state');

    // Checkboxes
    const checks = {
        dfs: document.getElementById('check-dfs'),
        bfs: document.getElementById('check-bfs'),
        heuristic: document.getElementById('check-heuristic')
    };

    // Result Columns
    const columns = {
        dfs: document.getElementById('dfs-results'),
        bfs: document.getElementById('bfs-results'),
        heuristic: document.getElementById('heuristic-results')
    };

    solveBtn.addEventListener('click', async () => {
        const start = startStateInput.value;
        const goal = goalStateInput.value;
        const selectedAlgos = Object.keys(checks).filter(key => checks[key].checked);

        if (selectedAlgos.length === 0) {
            showError("Por favor selecciona al menos un algoritmo.");
            return;
        }

        if (!start || !goal) {
            showError("Por favor ingrese ambos estados inicial y objetivo.");
            return;
        }

        resetUI(selectedAlgos);

        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ start, goal, algorithms: selectedAlgos })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Error en la búsqueda");
            }

            renderAllResults(data);
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } catch (err) {
            showError(err.message);
        } finally {
            loader.classList.add('hidden');
        }
    });

    function resetUI(selectedAlgos) {
        resultsSection.classList.add('hidden');
        errorContainer.classList.add('hidden');
        loader.classList.remove('hidden');

        Object.keys(columns).forEach(key => {
            const col = columns[key];
            col.querySelector('.stats-compact').innerHTML = '';
            col.querySelector('.path-visualizer-vertical').innerHTML = '';

            // Show/Hide column based on selection
            if (selectedAlgos.includes(key)) {
                col.classList.remove('hidden');
            } else {
                col.classList.add('hidden');
            }
        });
    }

    function renderAllResults(data) {
        resultsSection.classList.remove('hidden');

        Object.keys(data).forEach(algo => {
            const col = columns[algo];
            const result = data[algo];

            if (!result || !result.path) {
                col.querySelector('.stats-compact').innerHTML = '<p class="error-msg">Sin solución</p>';
                return;
            }

            // Render Stats
            col.querySelector('.stats-compact').innerHTML = `
                <div class="stat-mini"><span>Pasos:</span> ${result.steps}</div>
                <div class="stat-mini"><span>Tiempo:</span> ${result.time}ms</div>
            `;

            // Render Path
            const visualizer = col.querySelector('.path-visualizer-vertical');
            result.path.forEach((step, index) => {
                const node = document.createElement('div');
                node.className = 'step-node';
                node.textContent = step.join(', ');
                visualizer.appendChild(node);

                if (index < result.path.length - 1) {
                    const arrow = document.createElement('div');
                    arrow.className = 'arrow-v';
                    arrow.innerHTML = '↓';
                    visualizer.appendChild(arrow);
                }
            });
        });
    }

    function showError(msg) {
        errorContainer.textContent = msg;
        errorContainer.classList.remove('hidden');
        loader.classList.add('hidden');
    }
});
