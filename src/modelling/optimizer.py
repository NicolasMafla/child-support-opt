import pulp
from abc import ABC, abstractmethod
from typing import Dict, Any


class LpOptimizer(ABC):
    def __init__(
            self,
            model: pulp.LpProblem,
            variables: Dict[str, pulp.LpVariable],
            params: Dict[str, Any]
    ):
        self.model = model
        self.variables = variables
        self.params = params

    @abstractmethod
    def set_objective(self) -> None:
        pass

    @abstractmethod
    def add_constraints(self) -> None:
        pass

    @abstractmethod
    def solve(self) -> None:
        pass


class BudgetLpOptimizer(LpOptimizer):
    def __init__(
            self,
            model: pulp.LpProblem,
            variables: Dict[str, pulp.LpVariable],
            params: Dict[str, Any]
    ):
        super().__init__(model=model, variables=variables, params=params)

    def set_objective(self) -> None:
        x1 = self.variables["x1"]
        x2 = self.variables["x2"]
        obj_func = x1 + x2
        self.model.setObjective(obj_func)

    def add_constraints(self) -> None:
        c1 = self.params["C1"] * self.variables["x1"] + self.params["C2"] * self.variables["x2"] <= self.params["B"] * (1 - 0.05)
        c2 = self.variables["x1"] + self.variables["x2"] <= self.params["N_max"]
        c3 = self.variables["x1"] >= 1
        c4 = self.variables["x2"] >= 1
        c5 = self.variables["x1"] >= 0.1 * (self.variables["x1"] + self.variables["x2"])

        for const in [c1, c2, c3, c4, c5]:
            self.model.addConstraint(constraint=const)

    def solve(self) -> None:
        self.model.solve()


pulp.LpSolverDefault.msg = False

params = {
    "C1" : 5787.51 / 275 + 5,  # Costo por niño tipo 1 (0 a 5 años)
    "C2" : 5787.51 / 275,  # Costo por niño tipo 2 (6 a 22 años)
    "B" : 6000,  # Presupuesto asignado
    "N_max" : 1000  # Número máximo de niños
}

model = pulp.LpProblem(name="compassion", sense=pulp.LpMaximize)

variables = {
    "x1": pulp.LpVariable(name="x1", lowBound=0, cat="Integer"),
    "x2": pulp.LpVariable(name="x2", lowBound=0, cat="Integer")
}

b = BudgetLpOptimizer(model=model, variables=variables, params=params)
b.set_objective()
b.add_constraints()
b.solve()

if pulp.LpStatus[b.model.status] == "Optimal":
    print(f"Estado de la solución: {pulp.LpStatus[model.status]}")
    print(f"n1: {pulp.value(variables['x1'])}")
    print(f"n2: {pulp.value(variables['x2'])}")
    print(f"n1 + n2: {pulp.value(variables['x1']) + pulp.value(variables['x2'])}")

    # Imprimir el valor de la restricción budget_constraint (costo total)
    total_cost = params["C1"] * pulp.value(variables["x1"]) + params["C2"] * pulp.value(variables["x2"])
    print(f"Presupuesto asignado: {params['B']} vs. costo optimizado: {total_cost}")
else:
    print(f"Estado: {pulp.LpStatus[model.status]}")
