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
        t1 = self.variables["t1"]
        t2 = self.variables["t2"]
        obj_func = (x1 + x2) + (t1 + t2)
        self.model.setObjective(obj_func)

    def add_constraints(self) -> None:
        x1 = self.variables["x1"]
        x2 = self.variables["x2"]
        c1 = self.params["C1"]
        c2 = self.params["C2"]
        d1 = self.params["D1"]
        d2 = self.params["D2"]
        t1 = self.variables["t1"]
        t2 = self.variables["t2"]
        G = self.params["G"]
        E = self.params["E"]
        V = self.params["V"]
        I = self.params["I"]
        n_max = self.params["N_max"]
        kratio = self.params["kids_ratio"]

        director = self.params["director"]
        accountant = self.params["accountant"]
        secretary = self.params["secretary"]
        kitchen = self.params["kitchen"]
        pastor = self.params["pastor"]
        crew = director + accountant + secretary + kitchen + pastor

        R1 = (c1 * x1 + c2 * x2) + (d1 * t1) + (d2 * t2) + 4741.56 + G + V + crew <= (I + E) * (x1 + x2)
        R2 = x1 + x2 <= n_max
        R3 = x1 >= 1
        R4 = x2 >= 1
        R5 = x1 <= (kratio) * (x1 + x2)
        R9 = x1 <= (50 * t1)
        R10 = x2 <= (100 * t2)
        R11 = t1 >= 0
        R12 = t2 >= 0
        R13 = (x1 * 1.5 * 2 * 10) + (t1 * 2 * 10) + (t1 * 2 * 2) <= 0.8 * (t1 * 1920)
        R14 = (t2 * 2 * 44) + (t2 * 2 * 2) + (x2 * 1.5) + (2 * t2 * 44) <= 0.8 * (t2 * 1920)

        for const in [R1, R2, R3, R4, R5, R9, R10, R11, R12, R13, R14]:
            self.model.addConstraint(constraint=const)

    def solve(self) -> None:
        self.model.solve()
