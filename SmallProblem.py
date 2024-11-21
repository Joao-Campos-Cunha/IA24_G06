# -*- coding: utf-8 -*-
"""
Notebook - Planeamento de Tarefas (CSP)
Este notebook aborda a resolução de um problema de planeamento de tarefas usando CSPs (Constraint Satisfaction Problems).
"""

# Importar a biblioteca de restrições
from constraint import Problem

# Importar matplotlib para o gráfico
import matplotlib.pyplot as plt

# Função para carregar o dataset pequeno
def load_small_dataset():
    """
    Define o dataset com 8 tarefas, as precedências e o uso de recursos.
    """
    return {
        "horizon": 20,
        "tasks": {
            1: {"duration": 2, "resources": {"R1": 1, "R2": 0}},
            2: {"duration": 3, "resources": {"R1": 0, "R2": 1}},
            3: {"duration": 4, "resources": {"R1": 0, "R2": 1}},
            4: {"duration": 1, "resources": {"R1": 0, "R2": 1}},
            5: {"duration": 2, "resources": {"R1": 1, "R2": 0}},
            6: {"duration": 3, "resources": {"R1": 0, "R2": 1}},
            7: {"duration": 4, "resources": {"R1": 0, "R2": 1}},
            8: {"duration": 1, "resources": {"R1": 0, "R2": 1}},
        },
        "precedences": {
            1: [2, 3],
            2: [4],
            3: [4],
            5: [6, 7],
            6: [8],
            7: [8],
        },
        "resources": {"R1": 1, "R2": 2},
    }

# Carrega os dados
data = load_small_dataset()

# Criar o problema
problem = Problem()

# Adiciona variáveis para cada tarefa
for task_id in data["tasks"]:
    # Cada tarefa pode começar em qualquer unidade de tempo dentro de um horizonte
    problem.addVariable(task_id, range(data["horizon"] + 1))

# Adicionar restrições de precedência
for task, successors in data["precedences"].items():
    for successor in successors:
        problem.addConstraint(
            lambda t1, t2, dur=data["tasks"][task]["duration"]: t1 + dur <= t2,
            (task, successor),
        )

# Adiciona restrições de recursos
def resource_constraint(*args):
    """
    Verifica se o uso de recursos em cada unidade de tempo está dentro dos limites permitidos.
    """
    times = {task: start for task, start in zip(data["tasks"].keys(), args)}
    for t in range(data["horizon"] + 1):
        usage = {"R1": 0, "R2": 0}
        for task, start in times.items():
            # Se a tarefa estiver ativa neste tempo
            if start <= t < start + data["tasks"][task]["duration"]:
                for resource, amount in data["tasks"][task]["resources"].items():
                    usage[resource] += amount
        # Verificar se algum recurso excede o limite
        if any(usage[res] > data["resources"][res] for res in data["resources"]):
            return False
    return True

# Adicionar a restrição de recursos ao problema
problem.addConstraint(resource_constraint, data["tasks"].keys())

# Resolver o problema
solution = problem.getSolution()

# Exibir a solução
if solution:
    print("Solução encontrada:")
    for task, start_time in sorted(solution.items()):
        print(f"Tarefa {task}: início no tempo {start_time}")

    # Criar o gráfico de Gantt
    tasks = sorted(solution.items())  # Ordenar tarefas por ID
    task_ids = [f"Tarefa {task}" for task, _ in tasks]
    start_times = [start for _, start in tasks]
    durations = [data["tasks"][task]["duration"] for task, _ in tasks]

    # Criar o gráfico de Gantt
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (start, duration) in enumerate(zip(start_times, durations)):
        ax.barh(i, duration, left=start, color='skyblue', edgecolor='black')

    # Configurar o gráfico
    ax.set_yticks(range(len(task_ids)))
    ax.set_yticklabels(task_ids)
    ax.set_xlabel("Tempo")
    ax.set_title("Cronograma de Tarefas")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()
else:
    print("Nenhuma solução encontrada.")
