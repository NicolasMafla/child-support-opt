import streamlit as st
import pulp
import pandas as pd
from typing import Dict, Any
from src.modelling.optimizer import BudgetLpOptimizer

# Configuración de la página
st.set_page_config(
    page_title="Optimizador de Presupuesto",
    page_icon="💰",
    layout="wide"
)

# Versión del modelo
MODEL_VERSION = "v1.0.0"

# Título y descripción
st.title("Optimizador de Presupuesto")
st.caption(f"Modelo de optimización lineal {MODEL_VERSION}")

st.markdown("""
Esta aplicación te permite optimizar la distribución de recursos usando programación lineal.
Ajusta los parámetros y observa cómo cambian los resultados óptimos.
""")


# Función para ejecutar el optimizador
def run_optimizer(params):
    pulp.LpSolverDefault.msg = False

    model = pulp.LpProblem(name="compassion", sense=pulp.LpMinimize)

    variables = {
        "x1": pulp.LpVariable(name="x1", lowBound=0, cat="Integer"),
        "x2": pulp.LpVariable(name="x2", lowBound=0, cat="Integer"),
        "t1": pulp.LpVariable(name="t1", lowBound=0, cat="Integer"),
        "t2": pulp.LpVariable(name="t2", lowBound=0, cat="Integer")
    }

    optimizer = BudgetLpOptimizer(model=model, variables=variables, params=params)
    optimizer.set_objective()
    optimizer.add_constraints()
    optimizer.solve()

    results = {
        "status": pulp.LpStatus[model.status],
        "n1": pulp.value(variables['x1']),
        "n2": pulp.value(variables['x2']),
        "t1": pulp.value(variables['t1']),
        "t2": pulp.value(variables['t2']),
    }

    if results["status"] == "Optimal":
        results["total_kids"] = results["n1"] + results["n2"]
        results["expenses"] = ((params["C1"] * results["n1"] + params["C2"] * results["n2"]) +
                               (params["D1"] * results["t1"]) + (params["D2"] * results["t2"]) +
                               params["G"] + params["V"] +
                               params["director"] + params["accountant"] +
                               params["secretary"] + params["kitchen"] + params["pastor"])
        results["budget"] = params["I"] * results["total_kids"]

    return results


# Interfaz de usuario para parámetros
st.sidebar.header("Parámetros del Modelo")

with st.sidebar.expander("Parámetros de Costo", expanded=True):
    c1 = st.number_input("C1 (Costo por niño tipo 1)", value=41.88401, step=1.0, format="%.5f")
    c2 = st.number_input("C2 (Costo por niño tipo 2)", value=165.59988, step=1.0, format="%.5f")
    d1 = st.number_input("D1 (Costo por maestro tipo 1)", value=7925.16, step=100.0, format="%.2f")
    d2 = st.number_input("D2 (Costo por maestro tipo 2)", value=7925.16, step=100.0, format="%.2f")

with st.sidebar.expander("Parámetros de Ingresos", expanded=True):
    i = st.number_input("I (Ingreso mensual por niño)", value=20.5 * 12, step=1.0, format="%.5f")
    e = st.number_input("E (Extra)", value=7.04717, step=0.1, format="%.5f")

with st.sidebar.expander("Restricciones", expanded=True):
    n_max = st.number_input("N_max (Capacidad máxima)", value=1000.0, step=10.0, format="%.1f")
    kids_ratio = st.slider("Proporción de niños tipo 1", min_value=0.0, max_value=1.0, value=0.19, step=0.01,
                           format="%.2f")

with st.sidebar.expander("Gastos Fijos", expanded=True):
    g = st.number_input("G (Gastos generales)", value=4570.15, step=100.0, format="%.2f")
    v = st.number_input("V (Gastos variables)", value=1140.76, step=100.0, format="%.2f")
    director = st.number_input("Director", value=7925.16, step=100.0, format="%.2f")
    accountant = st.number_input("Contador", value=float(235 * 12), step=100.0, format="%.2f")
    secretary = st.number_input("Secretaria", value=2820.0, step=100.0, format="%.2f")
    kitchen = st.number_input("Cocina", value=0.0, step=100.0, format="%.2f")
    pastor = st.number_input("Pastor", value=0.0, step=100.0, format="%.2f")

# Información sobre el modelo en el sidebar
with st.sidebar.expander("Documentación del Modelo", expanded=False):
    st.markdown("""
    ### Descripción del Modelo

    Este modelo de optimización lineal busca maximizar el número total de niños (x1 + x2) y profesores (t1 + t2) 
    sujeto a restricciones de presupuesto, capacidad, y operativas.

    #### Variables de Decisión:
    - **x1**: Cantidad de niños tipo 1
    - **x2**: Cantidad de niños tipo 2
    - **t1**: Cantidad de maestros tipo 1
    - **t2**: Cantidad de maestros tipo 2

    #### Restricciones Principales:
    - **Presupuestaria**: Los gastos totales deben ser menores o iguales al presupuesto
    - **Capacidad**: El número total de niños no puede exceder la capacidad máxima
    - **Proporción de niños**: El número de niños tipo 1 debe mantener cierta proporción del total
    - **Relación niños-maestros**: Cada maestro puede atender a un número máximo de niños
    """)

# Recopilar parámetros
params = {
    "C1": c1,
    "C2": c2,
    "D1": d1,
    "D2": d2,
    "I": i,
    "E": e,
    "N_max": n_max,
    "kids_ratio": kids_ratio,
    "G": g,
    "V": v,
    "director": director,
    "accountant": accountant,
    "secretary": secretary,
    "kitchen": kitchen,
    "pastor": pastor,
}

# Botón para ejecutar la optimización
if st.button("Ejecutar Optimización", type="primary"):
    with st.spinner("Calculando solución óptima..."):
        results = run_optimizer(params)

    # Estado de la solución con badge
    if results["status"] == "Optimal":
        st.success(f"✅ Estado de la solución: {results['status']}")
    else:
        st.error(f"❌ Estado de la solución: {results['status']}")

    if results["status"] == "Optimal":
        # SECCIÓN 1: Métricas principales (x1, x2, t1, t2)
        st.subheader("Variables Principales")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Niños tipo 1 (x1)",
                value=int(results["n1"]),
                border=True
            )

        with col2:
            st.metric(
                label="Niños tipo 2 (x2)",
                value=int(results["n2"]),
                border=True
            )

        with col3:
            st.metric(
                label="Maestros tipo 1 (t1)",
                value=int(results["t1"]),
                border=True
            )

        with col4:
            st.metric(
                label="Maestros tipo 2 (t2)",
                value=int(results["t2"]),
                border=True
            )

        # SECCIÓN 2: Detalles de la solución (colapsable)
        with st.expander("Detalles de la Solución", expanded=False):
            # Totales
            st.subheader("Totales")
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Total de Niños",
                    value=int(results["total_kids"]),
                    border=True
                )

                st.metric(
                    label="Total de Maestros",
                    value=int(results["t1"] + results["t2"]),
                    border=True
                )

            with col2:
                # Métricas financieras
                st.metric(
                    label="Presupuesto Total",
                    value=f"${results['budget']:,.2f}",
                    border=True
                )

                margin = results['budget'] - results['expenses']
                st.metric(
                    label="Gastos Totales",
                    value=f"${results['expenses']:,.2f}",
                    border=True
                )

            # Tabla de ratios
            st.subheader("Ratios Detallados")
            ratios_data = {
                "Ratio": ["Niños tipo 1 / Total", "Niños tipo 2 / Total",
                          "Niños por maestro tipo 1", "Niños por maestro tipo 2",
                          "Maestros / Total niños"],
                "Valor": [
                    f"{results['n1'] / results['total_kids']:.2%}",
                    f"{results['n2'] / results['total_kids']:.2%}",
                    f"{results['n1'] / results['t1']:.2f}" if results["t1"] > 0 else "N/A",
                    f"{results['n2'] / results['t2']:.2f}" if results["t2"] > 0 else "N/A",
                    f"{(results['t1'] + results['t2']) / results['total_kids']:.4f}" if results[
                                                                                            "total_kids"] > 0 else "N/A"
                ]
            }
            st.dataframe(pd.DataFrame(ratios_data), use_container_width=True, hide_index=True)

            # Tabla de costos
            st.subheader("Estructura de Gastos")
            costs = {
                "Categoría": ["Niños tipo 1", "Niños tipo 2", "Maestros tipo 1", "Maestros tipo 2",
                              "Personal", "Gastos Generales", "TOTAL"],
                "Costo": [
                    params["C1"] * results["n1"],
                    params["C2"] * results["n2"],
                    params["D1"] * results["t1"],
                    params["D2"] * results["t2"],
                    params["director"] + params["accountant"] + params["secretary"] + params["kitchen"] + params[
                        "pastor"],
                    params["G"] + params["V"],
                    results["expenses"]
                ],
                "Porcentaje": [
                    f"{(params['C1'] * results['n1']) / results['expenses']:.2%}",
                    f"{(params['C2'] * results['n2']) / results['expenses']:.2%}",
                    f"{(params['D1'] * results['t1']) / results['expenses']:.2%}",
                    f"{(params['D2'] * results['t2']) / results['expenses']:.2%}",
                    f"{(params['director'] + params['accountant'] + params['secretary'] + params['kitchen'] + params['pastor']) / results['expenses']:.2%}",
                    f"{(params['G'] + params['V']) / results['expenses']:.2%}",
                    "100.00%"
                ]
            }
            cost_df = pd.DataFrame(costs)
            st.dataframe(cost_df, use_container_width=True, hide_index=True)