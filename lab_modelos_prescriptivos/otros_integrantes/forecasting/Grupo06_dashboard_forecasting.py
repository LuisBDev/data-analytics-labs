import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Importar las funciones del script de lógica
from forecast_logic import load_and_prepare_data, forecast_demand, calculate_optimal_order

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard Prescriptivo de Inventario", layout="wide")

# --- Título del Dashboard ---
st.title("📈 Dashboard Prescriptivo de Inventario")
st.markdown("Utiliza este dashboard para pronosticar la demanda y optimizar las decisiones de compra de productos.")

# --- Carga de Datos ---
# Usamos una función de cache para que los datos se carguen solo una vez.
@st.cache_data
def cached_load_data():
    # La ruta debe ser la carpeta donde se encuentran los CSV
    data_path = 'C:/Users/Carlos/OneDrive - Universidad Nacional Mayor de San Marcos/Escritorio/PROYECTO DESCRIPTIVO/Casos Ventas Retail'
    productos, ventas, inventario, costos = load_and_prepare_data(data_path)
    if productos is None:
        st.error("Error al cargar los datos. Revisa la ruta de los archivos y los logs.")
        return None, None, None, None
    # Unir nombres de productos a las ventas para facilitar la selección
    ventas = pd.merge(ventas, productos[['sku', 'categoria', 'subcategoria']], on='sku', how='left')
    ventas['product_display'] = ventas['sku'] + " - " + ventas['categoria'] + " (" + ventas['subcategoria'] + ")"
    return productos, ventas, inventario, costos

productos, ventas, inventario, costos = cached_load_data()

# Si la carga de datos falla, detener la ejecución.
if productos is None:
    st.stop()

# --- Barra Lateral de Filtros ---
st.sidebar.header("Filtros de Selección")

# Selector de Producto (SKU)
# Usamos el campo 'product_display' para que el menú sea más amigable
sku_display_list = ventas['product_display'].unique()
selected_sku_display = st.sidebar.selectbox(
    "Selecciona un Producto (SKU)",
    options=sku_display_list
)
# Extraer el SKU del string seleccionado
selected_sku = selected_sku_display.split(" - ")[0]


# Selector de Escenario de Costos
scenario_list = costos['Escenario'].unique()
selected_scenario = st.sidebar.selectbox(
    "Selecciona un Escenario de Costos",
    options=scenario_list
)

st.sidebar.markdown("---")
st.sidebar.info("Este dashboard combina un pronóstico de demanda (usando un modelo ARIMA) con un cálculo de Cantidad Económica de Pedido (EOQ) para recomendar la cantidad óptima a comprar.")


# --- Cuerpo Principal del Dashboard ---

# Obtener datos del producto seleccionado
producto_info = productos[productos['sku'] == selected_sku].iloc[0]
inventario_info = inventario[inventario['sku'] == selected_sku]

st.header(f"Análisis para: {producto_info['categoria']} - {producto_info['subcategoria']}")
st.subheader(f"SKU: {selected_sku}")

# Mostrar métricas clave
col1, col2, col3 = st.columns(3)
current_stock = inventario_info['stock_actual'].sum() if not inventario_info.empty else 0
col1.metric("Stock Actual Total", f"{current_stock} unidades")
col2.metric("Costo Unitario", f"${producto_info['costo_unitario']:.2f}")
col3.metric("Lead Time (Días)", f"{producto_info['lead_time_dias']} días")


# --- Pronóstico de Demanda ---
with st.spinner(f"Generando pronóstico de demanda para {selected_sku}..."):
    # Filtrar ventas para el SKU y agrupar por día
    ventas_sku = ventas[ventas['sku'] == selected_sku]
    ventas_diarias = ventas_sku.groupby('fecha')['cantidad_vendida'].sum().resample('D').sum()
    
    # Generar pronóstico para los próximos 90 días
    forecast = forecast_demand(ventas, selected_sku, periods=90)

# Gráfico de Demanda Histórica y Pronóstico
st.subheader("Pronóstico de Demanda vs. Ventas Históricas")
fig = go.Figure()

# Serie de ventas históricas (último año)
fig.add_trace(go.Scatter(
    x=ventas_diarias.index,
    y=ventas_diarias.values,
    mode='lines',
    name='Ventas Históricas Diarias'
))

# Serie de pronóstico
fig.add_trace(go.Scatter(
    x=forecast.index,
    y=forecast.values,
    mode='lines',
    name='Demanda Pronosticada',
    line=dict(color='red', dash='dash')
))

fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Cantidad Vendida/Pronosticada",
    legend=dict(x=0.01, y=0.98)
)
st.plotly_chart(fig, use_container_width=True)


# --- Optimización de Pedido ---
st.subheader("Recomendación de Compra (Optimización)")

# Calcular cantidad óptima para el escenario seleccionado
optimal_quantity = calculate_optimal_order(
    sku=selected_sku,
    forecasted_demand=forecast,
    productos_df=productos,
    costos_df=costos,
    scenario=selected_scenario
)

st.markdown(f"Para el **{selected_scenario}**, la recomendación es:")
st.success(f"**Cantidad Óptima de Pedido: {optimal_quantity} unidades**")


# --- Comparativa de Escenarios ---
st.subheader("Comparativa de Cantidad Óptima por Escenario de Costos")
st.markdown("La siguiente tabla muestra cómo cambiaría la cantidad de pedido recomendada bajo diferentes escenarios de costos logísticos.")

escenarios_data = []
for scenario in costos['Escenario'].unique():
    qty = calculate_optimal_order(
        sku=selected_sku,
        forecasted_demand=forecast,
        productos_df=productos,
        costos_df=costos,
        scenario=scenario
    )
    costo_info = costos[costos['Escenario'] == scenario].iloc[0]
    escenarios_data.append({
        "Escenario": scenario,
        "Cantidad Óptima Recomendada": qty,
        "Costo de Pedido": f"${costo_info['costo_pedido']:.2f}",
        "Costo Mantenimiento (% Anual)": f"{costo_info['costo_mantenimiento_anual']:.0%}"
    })

escenarios_df = pd.DataFrame(escenarios_data)
st.dataframe(escenarios_df, use_container_width=True)
