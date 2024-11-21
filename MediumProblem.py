from constraint import Problem
import matplotlib.pyplot as plt

def load_medium_dataset():
    """
    Define o dataset com 12 tarefas, suas precedências, modos de execução e uso de recursos.
    """
    return {
        "horizon": 46,
        "tasks": {
            1: {"modes": {1: {"duration": 0, "resources": {"R1": 0, "R2": 0}}}},
            2: {"modes": {1: {"duration": 3, "resources": {"R1": 6, "R2": 2}}}},
            3: {"modes": {1: {"duration": 1, "resources": {"R1": 0, "R2": 0}}}},
            4: {"modes": {1: {"duration": 8, "resources": {"R1": 4, "R2": 0}}}},
            5: {"modes": {1: {"duration": 4, "resources": {"R1": 0, "R2": 4}}}},
            6: {"modes": {1: {"duration": 4, "resources": {"R1": 0, "R2": 4}}}},
            7: {"modes": {1: {"duration": 6, "resources": {"R1": 2, "R2": 0}}}},
            8: {"modes": {1: {"duration": 4, "resources": {"R1": 4, "R2": 2}}}},
            9: {"modes": {1: {"duration": 5, "resources": {"R1": 3, "R2": 0}}}},
            10: {"modes": {1: {"duration": 7, "resources": {"R1": 2, "R2": 1}}}},
            11: {"modes": {1: {"duration": 4, "resources": {"R1": 0, "R2": 3}}}},
            12: {"modes": {1: {"duration": 0, "resources": {"R1": 0, "R2": 0}}}},
        },
        "precedences": { 
            1: [2, 3, 4],
            2: [5, 6],
            3: [10, 11],
            4: [9],
            5: [7, 8],
            6: [10, 11],
            7: [9, 10],
            8: [9],
            9: [12],
            10: [12],
            11: [12],
        },
        "resources": {"R1": 6, "R2": 4},
    }

# Carregar os dados
data_medium = load_medium_dataset()

# Criar o problema
problem_medium = Problem()

# Adicionar variáveis para cada tarefa e modo
variables = []
for task_id, task_data in data_medium["tasks"].items():
    modes = task_data["modes"].keys()
    for mode in modes:
        variable = (task_id, mode)
        variables.append(variable)
        problem_medium.addVariable(variable, range(data_medium["horizon"] + 1))

# Adicionar restrições de precedência
for task, successors in data_medium["precedences"].items():
    for successor in successors:
        for mode in data_medium["tasks"][task]["modes"]:
            for succ_mode in data_medium["tasks"][successor]["modes"]:
                duration = data_medium["tasks"][task]["modes"][mode]["duration"]
                problem_medium.addConstraint(
                    lambda t1, t2, dur=duration: t1 + dur <= t2,
                    [(task, mode), (successor, succ_mode)],
                )

# Adicionar restrições de recursos
def resource_constraint(*args):
    """
    Verifica se o uso de recursos em cada unidade de tempo está dentro dos limites permitidos.
    """
    times = {variable: start for variable, start in zip(variables, args)}
    for t in range(data_medium["horizon"] + 1):
        usage = {"R1": 0, "R2": 0}
        for (task, mode), start in times.items():
            if start <= t < start + data_medium["tasks"][task]["modes"][mode]["duration"]:
                for resource, amount in data_medium["tasks"][task]["modes"][mode]["resources"].items():
                    usage[resource] += amount
        if any(usage[res] > data_medium["resources"][res] for res in data_medium["resources"]):
            return False
    return True

problem_medium.addConstraint(resource_constraint, variables)

# Resolver o problema
solution_medium = problem_medium.getSolution()

# Exibir a solução
if solution_medium:
    print("Solução encontrada:")
    for (task, mode), start_time in sorted(solution_medium.items()):
        print(f"Tarefa {task} (Modo {mode}): início no tempo {start_time}")
else:
    print("Nenhuma solução encontrada.")

# Gerar gráfico de Gantt
def plot_gantt_chart(solution, data):
    fig, ax = plt.subplots(figsize=(12, 6))

    task_labels = []
    start_times = []
    durations = []

    for (task, mode), start_time in sorted(solution.items()):
        duration = data["tasks"][task]["modes"][mode]["duration"]
        task_labels.append(f"T{task}-M{mode}")
        start_times.append(start_time)
        durations.append(duration)

    for i, (start, duration) in enumerate(zip(start_times, durations)):
        ax.barh(i, duration, left=start, color="skyblue", edgecolor="black")

    ax.set_yticks(range(len(task_labels)))
    ax.set_yticklabels(task_labels)
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Tarefas")
    ax.set_title("Gráfico de Gantt - Problema Médio")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.show()

if solution_medium:
    plot_gantt_chart(solution_medium, data_medium)
else:
    print("Nenhuma solução encontrada; não é possível gerar o gráfico de Gantt.")
