document.addEventListener('DOMContentLoaded', () => {
    const algSelect = document.getElementById('algorithm');
    const labelStart = document.getElementById('label-start');
    const labelGoal = document.getElementById('label-goal');
    const inputStart = document.getElementById('input-start');
    const inputGoal = document.getElementById('input-goal');
    const solveBtn = document.getElementById('solve-btn');
    const resultsContent = document.getElementById('results-content');
    const loader = document.getElementById('loader');
    const errorMsg = document.getElementById('error-msg');
    const pathVisualizer = document.getElementById('path-visualizer');
    const statSteps = document.querySelector('#stat-steps .value');
    const statCost = document.getElementById('stat-cost');
    const statCostContainer = document.getElementById('stat-cost-container');

    const config = {
        dfs: {
            labelStart: 'Estado Inicial (Puzzle)',
            labelGoal: 'Estado Objetivo (Puzzle)',
            placeholder: 'Ej: 4,2,3,1',
            type: 'text'
        },
        ucs: {
            labelStart: 'Ciudad Origen',
            labelGoal: 'Ciudad Destino',
            placeholder: '',
            type: 'select'
        },
        heuristica: {
            labelStart: 'Estado Inicial (Puzzle)',
            labelGoal: 'Estado Objetivo (Puzzle)',
            placeholder: 'Ej: 4,2,3,1',
            type: 'text'
        }
    };

    let cities = [];

    async function fetchCities() {
        try {
            const resp = await fetch('/api/cities');
            cities = await resp.json();
        } catch (e) {
            console.error("Error cargando ciudades", e);
        }
    }

    function createInput(id, type, placeholder) {
        if (type === 'select') {
            const select = document.createElement('select');
            select.id = id;
            cities.forEach(city => {
                const opt = document.createElement('option');
                opt.value = city;
                opt.textContent = city.charAt(0).toUpperCase() + city.slice(1);
                select.appendChild(opt);
            });
            return select;
        } else {
            const input = document.createElement('input');
            input.id = id;
            input.type = 'text';
            input.placeholder = placeholder;
            return input;
        }
    }

    function updateInputs() {
        const alg = algSelect.value;
        const currentConfig = config[alg];

        const inputsContainer = document.getElementById('inputs-container');
        inputsContainer.innerHTML = '';

        const group1 = document.createElement('div');
        group1.className = 'input-group';
        const lbl1 = document.createElement('label');
        lbl1.textContent = currentConfig.labelStart;
        group1.appendChild(lbl1);
        const in1 = createInput('input-start', currentConfig.type, currentConfig.placeholder);
        group1.appendChild(in1);

        const group2 = document.createElement('div');
        group2.className = 'input-group';
        const lbl2 = document.createElement('label');
        lbl2.textContent = currentConfig.labelGoal;
        group2.appendChild(lbl2);
        const in2 = createInput('input-goal', currentConfig.type, currentConfig.placeholder);
        group2.appendChild(in2);

        inputsContainer.appendChild(group1);
        inputsContainer.appendChild(group2);

        resultsContent.classList.add('hidden');
        errorMsg.classList.add('hidden');
    }

    algSelect.addEventListener('change', updateInputs);

    // Inicializar
    fetchCities().then(() => updateInputs());

    solveBtn.addEventListener('click', async () => {
        const inputStart = document.getElementById('input-start');
        const inputGoal = document.getElementById('input-goal');

        const payload = {
            algorithm: algSelect.value,
            start: inputStart.value.trim(),
            goal: inputGoal.value.trim()
        };

        if (!payload.start || !payload.goal) {
            showError('Por favor ingresa ambos valores');
            return;
        }

        // UI State
        loader.classList.remove('hidden');
        resultsContent.classList.add('hidden');
        errorMsg.classList.add('hidden');
        pathVisualizer.innerHTML = '';

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error en el servidor');
            }

            renderResults(data);
        } catch (err) {
            showError(err.message);
        } finally {
            loader.classList.add('hidden');
        }
    });

    function renderResults(data) {
        resultsContent.classList.remove('hidden');
        statSteps.textContent = data.path.length;

        if (data.cost !== undefined) {
            statCostContainer.classList.remove('hidden');
            statCost.textContent = `${data.cost} km`;
        } else {
            statCostContainer.classList.add('hidden');
        }

        data.path.forEach((step, index) => {
            const node = document.createElement('div');
            node.className = 'step-node';
            node.textContent = Array.isArray(step) ? step.join(', ') : step;
            pathVisualizer.appendChild(node);

            if (index < data.path.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'arrow';
                arrow.textContent = '→';
                pathVisualizer.appendChild(arrow);
            }
        });
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.classList.remove('hidden');
    }
});
