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
        c1 = self.params["C1"] * self.variables["x1"] + self.params["C2"] * self.variables["x2"] == self.params["B"]
        c2 = self.variables["x1"] + self.variables["x2"] <= self.params["N_max"]
        c3 = self.variables["x1"] -1 >= 0
        c4 = self.variables["x2"] -1 >= 0

        for const in [c1, c2, c3, c4]:
            self.model.addConstraint(constraint=const)

    def solve(self) -> None:
        self.model.solve()


pulp.LpSolverDefault.msg = False

params = {
    "C1" : 10,  # Costo por niño tipo 1 (0 a 12 años)
    "C2" : 12,  # Costo por niño tipo 2 (13 a 18 años)
    "I1" : 15,  # Ingreso por niño tipo 1
    "I2" : 18,  # Ingreso por niño tipo 2
    "B" : 1000,  # Presupuesto asignado
    "N_max" : 100  # Número máximo de niños
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
    print(f"El número mínimo de niños tipo 1 necesarios es: {pulp.value(variables['x1'])}")
    print(f"El número mínimo de niños tipo 2 necesarios es: {pulp.value(variables['x2'])}")

    # Imprimir el valor de la restricción budget_constraint (costo total)
    total_cost = params["C1"] * pulp.value(variables["x1"]) + params["C2"] * pulp.value(variables["x2"])
    print(f"El costo total asignado a los niños es: {total_cost}")
else:
    print(f"Estado: {pulp.LpStatus[model.status]}")
