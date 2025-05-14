import streamlit as st
import pulp
import pandas as pd
from src.modelling.optimizer import BudgetLpOptimizer
from PIL import Image
import os

# Configuración de la página
st.set_page_config(
    page_title="Optimizador de Presupuesto",
    # page_icon="💰",
    layout="wide"
)

# Versión del modelo
MODEL_VERSION = "v1.0.0"


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
                               params["G"] + params["med_remb"] + params["V"] +
                               params["director"] + params["accountant"] +
                               params["secretary"] + params["additional"] + params["doctor"])
        results["budget"] = (params["I"] + params["E"]) * results["total_kids"]

    return results


def sidebar_contents():
    """Contenido del sidebar"""
    # Logo al inicio del sidebar
    try:
        # Ruta al logo (ajusta la ruta según donde tengas el archivo)
        logo_path = "logo.png"

        # Verificar si existe el archivo
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            # Mostrar logo en el sidebar
            st.sidebar.image(logo, use_container_width=True)
        else:
            st.sidebar.warning("Logo no encontrado en la ruta especificada")
    except Exception as e:
        st.sidebar.error(f"Error al cargar el logo: {e}")

    # Parámetros del modelo
    st.sidebar.header("Parámetros del Modelo")

    # Sección de parámetros de costo
    with st.sidebar.expander("Parámetros de Costo", expanded=True):
        c1 = st.number_input("Costo participante basado en el hogar", value=25.00, step=10.0, format="%.2f")
        c2 = st.number_input("Costo participante basado en el centro", value=99.00, step=10.0, format="%.2f")
        d1 = st.number_input("Costo tutor para atención en el hogar", value=7735.32, step=10.0, format="%.2f")
        d2 = st.number_input("Costo tutor para atención en el centro", value=7735.32, step=10.0, format="%.2f")

    # Sección de parámetros de ingreso
    with st.sidebar.expander("Parámetros de Ingresos", expanded=True):
        i = st.number_input("Tarifa Child Support Anual", value=20.5 * 12, step=10.0, format="%.2f")
        e = st.number_input("Movilización de recursos locales", value=0.00, step=10.0, format="%.2f")

    # Sección de restricciones
    with st.sidebar.expander("Restricciones", expanded=True):
        n_max = st.number_input("Capacidad máxima de participantes", value=1000, step=10)
        kids_ratio = st.slider(
            "Proporción participantes en el hogar", min_value=0.0, max_value=1.0, value=0.12, step=0.01,
            format="%.2f"
        )

    # Sección de gastos fijos
    with st.sidebar.expander("Gastos", expanded=True):
        g = st.number_input("Gastos recurrentes", value=3012.26, step=100.0, format="%.2f")
        med_remb = st.number_input("Gastos reembolso médico", value=500.00, step=100.0, format="%.2f")
        v = st.number_input("Gastos por movilización transporte", value=1000.00, step=100.0, format="%.2f")
        doctor = st.number_input("Costo tutor de salud", value=4741.56, step=100.0, format="%.2f")
        director = st.number_input("Costo director/a", value=7735.32, step=100.0, format="%.2f")
        accountant = st.number_input("Costo contador/a", value=float(200 * 12), step=100.0, format="%.2f")
        secretary = st.number_input("Costo secretario/a", value=4741.56, step=100.0, format="%.2f")
        additional = st.number_input("Costo otra posición", value=0.00, step=100.0, format="%.2f")

    # Documentación del modelo como sección normal (no colapsable)
    st.sidebar.header("Documentación del Modelo")
    st.sidebar.markdown("""
    Este modelo de optimización lineal busca maximizar el número total de niños (x1 + x2) y profesores (t1 + t2) 
    sujeto a restricciones de presupuesto, capacidad, y operativas.

    **Variables de Decisión:**
    - **x1**: Cantidad de participantes basado en el hogar
    - **x2**: Cantidad de participantes basado en el centro
    - **t1**: Cantidad de tutores con atención en el hogar
    - **t2**: Cantidad de tutores con atención en el centro

    **Restricciones Principales:**
    - **Presupuestaria**: Los gastos totales deben ser menores o iguales al presupuesto.
    - **Capacidad**: El número total de participantes no puede exceder la capacidad máxima.
    - **Proporción de participantes**: El número de participantes basado en el hogar debe mantener cierta proporción del total
    - **Relación participantes-tutor**: Cada tutor puede atender a un número máximo de participantes
    """)

    # Recopilación de parámetros
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
        "med_remb": med_remb,
        "V": v,
        "doctor": doctor,
        "director": director,
        "accountant": accountant,
        "secretary": secretary,
        "additional": additional
    }

    return params


def display_metrics(results):
    """Muestra las métricas principales separadas en dos filas"""

    # Primera fila: Participantes
    st.subheader("Participantes")

    # Crear layout de 2 columnas para los participantes
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Basados en el hogar",
            value=int(results["n1"]),
            border=True
        )

    with col2:
        st.metric(
            label="Basados en el centro",
            value=int(results["n2"]),
            border=True
        )

    # Segunda fila: Tutores
    st.subheader("Tutores")

    # Crear layout de 3 columnas para los tutores
    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric(
            label="Tutores atención hogar y centro",
            value=int(results["t1"]),
            border=True
        )

    with col4:
        st.metric(
            label="Tutores atención en centro",
            value=int(results["t2"]),
            border=True
        )

    with col5:
        st.metric(
            label="Tutor de salud",
            value=1,
            border=True
        )


def display_details(results, params):
    """Muestra los detalles de la solución"""
    with st.expander("Detalles de la Solución", expanded=False):
        # Sección de Totales
        st.subheader("Totales")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Total de participantes",
                value=int(results["total_kids"]),
                border=True
            )
        with col2:
            st.metric(
                label="Total de tutores",
                value=int(results["t1"] + results["t2"] + 1),
                border=True
            )

        col3, col4 = st.columns(2)
        with col3:
            # Métricas financieras
            st.metric(
                label="Presupuesto anual total",
                value=f"${results['budget']:,.2f}",
                border=True
            )
        with col4:
            st.metric(
                label="Gastos totales anuales estimados",
                value=f"${results['expenses']:,.2f}",
                border=True
            )

        # Tabla de costos
        st.subheader("Distribución de gastos")
        display_costs_table(results, params)

        # Tabla de ratios
        st.subheader("Ratios")
        display_ratios_table(results)


def display_ratios_table(results):
    """Muestra la tabla de ratios"""
    ratios_data = {
        "Ratio": [
            "Proporción participantes basados en el hogar",
            "Proporción participantes basados en el centro",
            "Participantes por tutor",
            "Total participantes asignados a un tutor"
        ],
        "Valor": [
            f"{results['n1'] / results['total_kids']:.2%}",
            f"{results['n2'] / results['total_kids']:.2%}",
            f"25 a 30 participantes",
            f"{int((results['n1'] + results['n2']) / (results['t1'] + results['t2']))}"
        ]
    }
    st.dataframe(pd.DataFrame(ratios_data), use_container_width=True, hide_index=True)


def display_costs_table(results, params):
    """Muestra la tabla de estructura de costos"""
    costs = {
        "Categoría": [
            "Participantes basados en el hogar",
            "Participantes basados en el centro",
            "Tutores atención en el hogar y centro",
            "Tutores atención en el centro",
            "Tutor de salud",
            "Personal",
            "Gastos recurrentes",
            "Gastos reembolso médico",
            "Gastos movilización transporte",
            "TOTAL"
        ],
        "Costo": [
            f"${params['C1'] * results['n1']:,.2f}",
            f"${params['C2'] * results['n2']:,.2f}",
            f"${params['D1'] * results['t1']:,.2f}",
            f"${params['D2'] * results['t2']:,.2f}",
            f"${params['doctor']:,.2f}",
            f"${params['director'] + params['accountant'] + params['secretary'] + params['additional']:,.2f}",
            f"${params['G']:,.2f}",
            f"${params['med_remb']:,.2f}",
            f"${params['V']:,.2f}",
            f"${results['expenses']:,.2f}"
        ],
        "Porcentaje": [
            f"{(params['C1'] * results['n1']) / results['expenses']:.2%}",
            f"{(params['C2'] * results['n2']) / results['expenses']:.2%}",
            f"{(params['D1'] * results['t1']) / results['expenses']:.2%}",
            f"{(params['D2'] * results['t2']) / results['expenses']:.2%}",
            f"{params['doctor'] / results['expenses']:.2%}",
            f"{(params['director'] + params['accountant'] + params['secretary'] + params['additional']) / results['expenses']:.2%}",
            f"{(params['G']) / results['expenses']:.2%}",
            f"{(params['med_remb']) / results['expenses']:.2%}",
            f"{(params['V']) / results['expenses']:.2%}",
            "100.00%"
        ]
    }
    cost_df = pd.DataFrame(costs)
    st.dataframe(cost_df, use_container_width=True, hide_index=True)


def main():
    """Función principal de la aplicación"""
    # Título y descripción
    st.title("Optimizador de Presupuesto")
    st.caption(f"Modelo de optimización lineal {MODEL_VERSION}")

    st.markdown("""
    Esta aplicación te permite optimizar la distribución de recursos del programa mediante un modelo de programación lineal.
    Ajusta los parámetros y observa cómo cambian los resultados óptimos.
    """)

    # Cargar el sidebar
    params = sidebar_contents()

    # Botón para ejecutar la optimización
    if st.button("Ejecutar Optimización", type="primary"):
        with st.spinner("Calculando solución óptima..."):
            results = run_optimizer(params)

        # Estado de la solución con badge
        if results["status"] == "Optimal":
            st.success(f"✅ Estado de la solución: Óptima")

            # SECCIÓN 1: Métricas principales (x1, x2, t1, t2)
            display_metrics(results)

            # SECCIÓN 2: Detalles de la solución (colapsable)
            display_details(results, params)
        else:
            st.error(f"❌ Estado de la solución: Inviable")
            st.warning("No se pudo encontrar una solución óptima. Revise los parámetros del modelo.")


if __name__ == "__main__":
    main()