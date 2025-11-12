import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard de Optimización de Inventario",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS para un look más profesional ---
st.markdown("""
<style>
    .reportview-container {
        background: #f5f5ff;
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
    .stMetric {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: #262424;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        color: black; /* Color de texto negro para las métricas */
    }
    .stMetric > div[data-testid="stMetricValue"] {
        color: black; /* Color negro para el valor de las métricas */
    }
    .stMetric > div[data-testid="stMetricLabel"] {
        color: black; /* Color negro para el título de las métricas */
    }
    .stDataFrame {
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1E3A8A; /* Azul oscuro */
    }
</style>
""", unsafe_allow_html=True)

# --- Título y Descripción del Dashboard ---
st.title("Dashboard de Análisis de Rentabilidad y Optimización de Inventarios")
st.markdown("""
Este dashboard interactivo presenta un análisis detallado de las estrategias de gestión de inventario para una empresa retail. 
A través de diferentes visualizaciones, se evalúan las recomendaciones de compra, se comparan escenarios de costos y se exploran los datos maestros 
para facilitar la toma de decisiones estratégicas.
""")

# --- Carga de Datos ---
@st.cache_data
def load_data():
    """Carga todos los archivos CSV necesarios desde el directorio de resultados."""
    data_path = 'Resultados_Optimizacion_sQ'
    if not os.path.exists(data_path):
        st.error(f"El directorio '{data_path}' no fue encontrado. Asegúrate de que los resultados se hayan exportado correctamente.")
        return None, None, None, None

    try:
        recomendaciones = pd.read_csv(os.path.join(data_path, 'Recomendaciones_Compra_Final.csv'))
        maestro = pd.read_csv(os.path.join(data_path, 'Datos_Maestros_Consolidados.csv'))
        combinados = pd.read_csv(os.path.join(data_path, 'Resultados_Combinados_Escenarios.csv'))
        
        # Cargar resultados por escenario
        resultados_escenarios = {}
        for i in range(1, 6):
            file = f'Resultados_Escenario_{i}.csv'
            resultados_escenarios[f'Escenario {i}'] = pd.read_csv(os.path.join(data_path, file))

        return recomendaciones, maestro, combinados, resultados_escenarios
    except FileNotFoundError as e:
        st.error(f"Error al cargar el archivo: {e}. Verifica que todos los CSV estén en la carpeta 'Resultados_Optimizacion_sQ'.")
        return None, None, None, None

recomendaciones, maestro, combinados, resultados_escenarios = load_data()

if recomendaciones is None:
    st.stop()

# --- Sidebar ---
st.sidebar.title("Panel de Navegación")
page = st.sidebar.radio("Selecciona una sección:", ["Resumen Ejecutivo", "Análisis de Escenarios", "Detalle de Recomendaciones", "Explorador de Datos"])

# --- Unir recomendaciones con datos maestros para obtener costo y categoría ---
recomendaciones_full = pd.merge(recomendaciones, maestro[['sku', 'costo_unitario', 'categoria']], on='sku', how='left')
recomendaciones_full['costo_total_pedido'] = recomendaciones_full['cantidad_a_pedir'] * recomendaciones_full['costo_unitario']


# ==============================================================================
# --- Página 1: Resumen Ejecutivo ---
# ==============================================================================
if page == "Resumen Ejecutivo":
    st.header("Resumen Ejecutivo de Recomendaciones de Compra")
    st.markdown("Esta sección presenta los indicadores clave (KPIs) basados en las recomendaciones del **Escenario 1**.")

    # --- KPIs Principales ---
    total_unidades_a_pedir = recomendaciones_full['cantidad_a_pedir'].sum()
    costo_total_inversion = recomendaciones_full['costo_total_pedido'].sum()
    skus_a_reponer = recomendaciones_full['sku'].nunique()
    tiendas_con_pedidos = recomendaciones_full['tienda'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Unidades Totales a Pedir", f"{total_unidades_a_pedir:,.0f}")
    col2.metric("Inversión Total Estimada", f"${costo_total_inversion:,.2f}")
    col3.metric("SKUs a Reponer", f"{skus_a_reponer}")
    col4.metric("Tiendas con Pedidos", f"{tiendas_con_pedidos}")

    st.markdown("---")

    # --- Gráficos de Resumen ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 SKUs por Cantidad a Pedir")
        top_skus = recomendaciones_full.groupby('sku')['cantidad_a_pedir'].sum().nlargest(10)
        fig_skus = px.bar(top_skus, x=top_skus.values, y=top_skus.index, orientation='h',
                          labels={'x': 'Cantidad a Pedir', 'y': 'SKU'},
                          title="Top 10 SKUs por Unidades",
                          text=top_skus.values, template="plotly_white")
        fig_skus.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_skus, use_container_width=True)

    with col2:
        st.subheader("Distribución de Inversión por Categoría")
        inversion_categoria = recomendaciones_full.groupby('categoria')['costo_total_pedido'].sum().sort_values(ascending=False)
        fig_cat = px.pie(inversion_categoria, values=inversion_categoria.values, names=inversion_categoria.index,
                         title="Inversión por Categoría de Producto",
                         hole=0.4)
        fig_cat.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Pedidos por Tienda")
    pedidos_tienda = recomendaciones_full.groupby('tienda')['cantidad_a_pedir'].sum().sort_values()
    fig_tienda = px.bar(pedidos_tienda, x=pedidos_tienda.index, y=pedidos_tienda.values,
                        labels={'x': 'Tienda', 'y': 'Cantidad a Pedir'},
                        title="Total de Unidades a Pedir por Tienda",
                        text=pedidos_tienda.values, template="plotly_white")
    st.plotly_chart(fig_tienda, use_container_width=True)

    # --- Análisis de Contribución ---
    st.header("Análisis de Contribución y Pareto")
    st.markdown("Identifica los productos y categorías con mayor impacto en la inversión total.")

    # Treemap de contribución por categoría y SKU
    st.subheader("Contribución a la Inversión por Categoría y SKU")
    contribucion_df = recomendaciones_full.groupby(['categoria', 'sku'])['costo_total_pedido'].sum().reset_index()
    fig_treemap = px.treemap(contribucion_df, path=['categoria', 'sku'], values='costo_total_pedido',
                             title='Distribución de la Inversión: Categorías y SKUs',
                             color='costo_total_pedido',
                             color_continuous_scale='Blues')
    st.plotly_chart(fig_treemap, use_container_width=True)

    # Gráfico de Pareto (80/20)
    st.subheader("Análisis de Pareto: SKUs vs. Inversión Total")
    pareto_df = recomendaciones_full.groupby('sku')['costo_total_pedido'].sum().sort_values(ascending=False).reset_index()
    pareto_df['pareto_%'] = pareto_df['costo_total_pedido'].cumsum() / pareto_df['costo_total_pedido'].sum() * 100
    
    # Encontrar el punto 80/20
    pareto_80 = pareto_df[pareto_df['pareto_%'] <= 80]
    num_skus_80 = len(pareto_80)
    total_skus = len(pareto_df)
    
    st.info(f"**Principio de Pareto (80/20):** Aproximadamente el 80% de la inversión se concentra en **{num_skus_80} de {total_skus} SKUs** (el {num_skus_80/total_skus:.1%} del total).")

    fig_pareto = px.bar(pareto_df.head(50), x='sku', y='costo_total_pedido',
                        title='Top 50 SKUs con Mayor Inversión',
                        labels={'sku': 'SKU', 'costo_total_pedido': 'Inversión Total'},
                        template='plotly_white')
    st.plotly_chart(fig_pareto, use_container_width=True)


# ==============================================================================
# --- Página 2: Análisis de Escenarios ---
# ==============================================================================
elif page == "Análisis de Escenarios":
    st.header("Análisis Comparativo de Escenarios de Costos")
    st.markdown("Compara los resultados financieros y de inventario para cada uno de los 5 escenarios de simulación.")

    if combinados is not None:
        # --- Resumen General de Escenarios ---
        st.subheader("Resumen General de Escenarios")
        
        # Calcular métricas clave por escenario
        summary_data = []
        for nombre, df_escenario in resultados_escenarios.items():
            costo_total = (df_escenario['costo_total_anual']).sum()
            unidades_totales = df_escenario['Q_optimo'].sum()
            stock_seguridad_total = df_escenario['stock_seguridad'].sum()
            summary_data.append({
                "Escenario": nombre,
                "Costo Total Anual": costo_total,
                "Unidades por Pedido (Q)": unidades_totales,
                "Unidades en Stock de Seguridad": stock_seguridad_total
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df.set_index('Escenario'))

        # --- Gráfico Comparativo de Costos ---
        fig_costos = px.bar(summary_df, x='Escenario', y='Costo Total Anual',
                            title='Costo Total Anual por Escenario',
                            labels={'Costo Total Anual': 'Costo Total ($)', 'Escenario': 'Escenario de Simulación'},
                            text=summary_df['Costo Total Anual'].apply(lambda x: f"${x:,.0f}"),
                            template="plotly_white")
        st.plotly_chart(fig_costos, use_container_width=True)

    st.markdown("---")
    
    # --- Análisis Detallado por SKU ---
    st.subheader("Análisis Detallado por SKU")
    st.markdown("Compara cómo varían los parámetros de inventario (`Q óptimo`, `Punto de Reorden`) para un mismo producto bajo diferentes escenarios de costos.")

    # --- Selector de SKU ---
    sku_seleccionado = st.selectbox("Selecciona un SKU para analizar:", options=maestro['sku'].unique())

    if sku_seleccionado and combinados is not None:
        datos_sku = combinados[combinados['sku'] == sku_seleccionado]
        
        # --- Gráfico Comparativo ---
        st.subheader(f"Comparación de Parámetros para SKU: {sku_seleccionado}")
        
        # Filtrar por una tienda para simplificar la visualización, o agregar un selector de tienda
        tiendas_del_sku = datos_sku['tienda'].unique()
        tienda_seleccionada = st.selectbox("Selecciona una Tienda:", options=tiendas_del_sku)
        
        if tienda_seleccionada:
            datos_plot = datos_sku[datos_sku['tienda'] == tienda_seleccionada]
            
            fig = px.bar(datos_plot, x='Escenario', y=['Q_optimo', 'punto_reorden', 'stock_seguridad'],
                         barmode='group',
                         labels={'value': 'Cantidad de Unidades', 'variable': 'Parámetro'},
                         title=f"Parámetros de Inventario para {sku_seleccionado} en {tienda_seleccionada}",
                         template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

            # --- Tabla de Datos ---
            st.subheader("Datos Detallados por Escenario")
            st.dataframe(datos_plot[['Escenario', 'tienda', 'sku', 'Q_optimo', 'punto_reorden', 'stock_seguridad', 'demanda_promedio_diaria']].set_index('Escenario'))


# ==============================================================================
# --- Página 3: Detalle de Recomendaciones ---
# ==============================================================================
elif page == "Detalle de Recomendaciones":
    st.header("Detalle de Órdenes de Compra Sugeridas")
    st.markdown("Explora, filtra y busca en la lista completa de recomendaciones de compra.")

    # --- Filtros ---
    col1, col2 = st.columns(2)
    with col1:
        tiendas_seleccionadas = st.multiselect("Filtrar por Tienda:", options=recomendaciones_full['tienda'].unique(), default=recomendaciones_full['tienda'].unique())
    with col2:
        categorias_seleccionadas = st.multiselect("Filtrar por Categoría:", options=recomendaciones_full['categoria'].unique(), default=recomendaciones_full['categoria'].unique())

    # Aplicar filtros
    recomendaciones_filtradas = recomendaciones_full[
        recomendaciones_full['tienda'].isin(tiendas_seleccionadas) &
        recomendaciones_full['categoria'].isin(categorias_seleccionadas)
    ]

    st.subheader(f"Mostrando {len(recomendaciones_filtradas)} de {len(recomendaciones_full)} recomendaciones")
    
    # --- Tabla Detallada ---
    st.dataframe(recomendaciones_filtradas[[
        'tienda', 'sku', 'categoria', 'inventario_posicion', 'punto_reorden', 
        'cantidad_a_pedir', 'costo_unitario', 'costo_total_pedido'
    ]], use_container_width=True)

    # --- Opción de Descarga ---
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(recomendaciones_filtradas)
    st.download_button(
        label="Descargar recomendaciones como CSV",
        data=csv,
        file_name='recomendaciones_compra.csv',
        mime='text/csv',
    )


# ==============================================================================
# --- Página 4: Explorador de Datos ---
# ==============================================================================
elif page == "Explorador de Datos":
    st.header("Explorador de Datos Maestros")
    st.markdown("Visualiza y filtra el conjunto de datos consolidado que sirve como base para el modelo.")

    if maestro is not None:
        # --- Filtros para el DataFrame Maestro ---
        st.sidebar.header("Filtros de Datos Maestros")
        cat_filter = st.sidebar.multiselect(
            'Filtrar por Categoría:',
            options=maestro['categoria'].unique(),
            default=maestro['categoria'].unique()
        )
        
        subcat_filter = st.sidebar.multiselect(
            'Filtrar por Subcategoría:',
            options=maestro['subcategoria'].unique(),
            default=maestro['subcategoria'].unique()
        )

        tienda_filter = st.sidebar.multiselect(
'Filtrar por Tienda:',
options=maestro['tienda'].unique(),
default=maestro['tienda'].unique()
)
    # Aplicar filtros al DataFrame maestro
    maestro_filtrado = maestro[
        maestro['categoria'].isin(cat_filter) &
        maestro['subcategoria'].isin(subcat_filter) &
        maestro['tienda'].isin(tienda_filter)
    ]
    
    st.subheader(f"Mostrando {len(maestro_filtrado)} de {len(maestro)} registros")
    st.dataframe(maestro_filtrado, use_container_width=True)
else:
    st.warning("No se pudo cargar el DataFrame maestro.")

st.sidebar.info(
"Dashboard creado para visualizar los resultados del modelo de optimización de inventario (s, Q)."
)
