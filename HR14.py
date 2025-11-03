# HR14_exploratorio.py
# Dashboard Exploratorio de Recursos Humanos
# Ejecuta con: streamlit run HR14_exploratorio.py
# Autor: ChatGPT (2025)

import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="HR — Dashboard Exploratorio", layout="wide")

st.title("📊 Dashboard Exploratorio de Recursos Humanos")
st.markdown("Explora tu dataset de empleados con filtros, métricas y gráficos interactivos.")

# =========================
# CARGA DE DATOS
# =========================
st.sidebar.header("📁 Carga de Datos")

uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Archivo cargado correctamente.")
else:
    st.info("Usando dataset de ejemplo (HRDataset_v14).")
    df = pd.DataFrame({
        "EmployeeName": [f"Empleado {i}" for i in range(1, 21)],
        "Department": ["IT", "Ventas", "HR", "Finanzas"] * 5,
        "Position": ["Analista", "Gerente", "Asistente", "Director", "Analista"][:20],
        "Salary": [40000, 55000, 30000, 80000, 45000] * 4,
        "EmpSatisfaction": [3, 4, 2, 5, 3] * 4,
        "EngagementSurvey": [4.1, 3.8, 2.9, 4.7, 3.5] * 4,
        "Absences": [2, 4, 0, 1, 3] * 4,
    })

# =========================
# FILTROS
# =========================
st.sidebar.header("🎯 Filtros")

cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

filters = {}
for col in cat_cols:
    options = df[col].unique().tolist()
    selected = st.sidebar.multiselect(f"Filtrar por {col}", options)
    if selected:
        filters[col] = selected

df_filtered = df.copy()
for col, selected in filters.items():
    df_filtered = df_filtered[df_filtered[col].isin(selected)]

# =========================
# MÉTRICAS RESUMEN
# =========================
st.subheader("📈 Métricas Generales")

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Empleados", len(df_filtered))
if "Salary" in df_filtered.columns:
    col2.metric("💰 Salario Promedio", f"${df_filtered['Salary'].mean():,.0f}")
if "EmpSatisfaction" in df_filtered.columns:
    col3.metric("😊 Satisfacción Media", f"{df_filtered['EmpSatisfaction'].mean():.2f}")
if "Absences" in df_filtered.columns:
    col4.metric("🚫 Ausencias Promedio", f"{df_filtered['Absences'].mean():.2f}")

st.divider()

# =========================
# VISUALIZACIONES
# =========================
st.subheader("📊 Visualizaciones Interactivas")

num_cols = df_filtered.select_dtypes(include=["int64", "float64"]).columns.tolist()

if len(num_cols) >= 1:
    chart_type = st.selectbox("Selecciona el tipo de gráfico", ["Histograma", "Boxplot", "Dispersión"])
    col_x = st.selectbox("Eje X", num_cols)
    col_y = None

    if chart_type == "Dispersión":
        col_y = st.selectbox("Eje Y", [c for c in num_cols if c != col_x])

    color_col = st.selectbox("Color por", [None] + cat_cols)

    if chart_type == "Histograma":
        fig = px.histogram(df_filtered, x=col_x, color=color_col, nbins=20, barmode="overlay")
    elif chart_type == "Boxplot":
        fig = px.box(df_filtered, x=color_col, y=col_x, points="all")
    else:
        fig = px.scatter(df_filtered, x=col_x, y=col_y, color=color_col, size_max=12)

    fig.update_layout(template="plotly_white", height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No se encontraron columnas numéricas para graficar.")

# =========================
# DESCARGA DE DATOS
# =========================
st.divider()
st.subheader("📥 Exportar Datos Filtrados")

csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Descargar CSV Filtrado",
    data=csv,
    file_name="HR_filtrado.csv",
    mime="text/csv",
)

st.caption("Creado con ❤️ por ChatGPT — 2025")
