import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Transferencias - Dashboard",
    page_icon="📦",
    layout="wide"
)

# Título principal
st.title("Sistema de Transferencias entre Tiendas")
st.markdown("### Dashboard de Control Prescriptivo")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    try:
        transferencias = pd.read_csv('transferencias_optimas.csv')
        comparacion = pd.read_csv('comparacion_escenarios.csv')
        return transferencias, comparacion
    except FileNotFoundError:
        st.error("Archivos de datos no encontrados. Ejecute el notebook primero.")
        return None, None

transferencias_df, comparacion_df = load_data()

if transferencias_df is not None and comparacion_df is not None:
    
    # Selector de escenario
    st.sidebar.header("Configuración")
    escenarios = transferencias_df['Escenario'].unique().tolist()
    escenario_seleccionado = st.sidebar.selectbox(
        "Seleccione un escenario:",
        escenarios
    )
    
    # Filtrar datos por escenario
    trans_filtered = transferencias_df[transferencias_df['Escenario'] == escenario_seleccionado]
    metricas_escenario = comparacion_df[comparacion_df['Escenario'] == escenario_seleccionado].iloc[0]
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Costo Total",
            value=f"${metricas_escenario['Costo_Total']:,.2f}"
        )
    
    with col2:
        st.metric(
            label="Transferencias",
            value=int(metricas_escenario['Num_Transferencias'])
        )
    
    with col3:
        st.metric(
            label="Unidades Movidas",
            value=int(metricas_escenario['Unidades_Transferidas'])
        )
    
    with col4:
        st.metric(
            label="Costo Rotura",
            value=f"${metricas_escenario['Costo_Rotura']:,.2f}"
        )
    
    st.markdown("---")
    
    # Sección: Desglose de Costos
    st.header("Desglose de Costos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Composición de Costos")
        costos_data = {
            'Tipo': ['Transferencias', 'Rotura de Stock', 'Exceso/Obsolescencia'],
            'Costo': [
                metricas_escenario['Costo_Transferencias'],
                metricas_escenario['Costo_Rotura'],
                metricas_escenario['Costo_Exceso']
            ]
        }
        costos_df = pd.DataFrame(costos_data)
        
        fig_pie = px.pie(
            costos_df,
            values='Costo',
            names='Tipo',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Comparación entre Escenarios")
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            x=comparacion_df['Escenario'],
            y=comparacion_df['Costo_Transferencias'],
            name='Transferencias',
            marker_color='lightblue'
        ))
        
        fig_bar.add_trace(go.Bar(
            x=comparacion_df['Escenario'],
            y=comparacion_df['Costo_Rotura'],
            name='Rotura',
            marker_color='orange'
        ))
        
        fig_bar.add_trace(go.Bar(
            x=comparacion_df['Escenario'],
            y=comparacion_df['Costo_Exceso'],
            name='Exceso',
            marker_color='green'
        ))
        
        fig_bar.update_layout(
            barmode='stack',
            xaxis_title="Escenario",
            yaxis_title="Costo ($)",
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Sección: Transferencias Recomendadas
    st.header("Transferencias Recomendadas")
    
    if len(trans_filtered) > 0:
        # Tabla de transferencias
        st.subheader("Detalle de Transferencias")
        st.dataframe(
            trans_filtered.style.format({
                'Cantidad': '{:.0f}',
                'Costo_Transferencia': '${:.2f}'
            }),
            use_container_width=True
        )
        
        # Análisis por tienda
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tiendas Origen (Proveedoras)")
            origenes = trans_filtered.groupby('Tienda_Origen').agg({
                'Cantidad': 'sum',
                'Costo_Transferencia': 'sum'
            }).reset_index().sort_values('Cantidad', ascending=False)
            
            fig_orig = px.bar(
                origenes,
                x='Tienda_Origen',
                y='Cantidad',
                color='Costo_Transferencia',
                color_continuous_scale='Reds',
                labels={'Cantidad': 'Unidades Enviadas', 'Tienda_Origen': 'Tienda'}
            )
            st.plotly_chart(fig_orig, use_container_width=True)
        
        with col2:
            st.subheader("Tiendas Destino (Receptoras)")
            destinos = trans_filtered.groupby('Tienda_Destino').agg({
                'Cantidad': 'sum',
                'Costo_Transferencia': 'sum'
            }).reset_index().sort_values('Cantidad', ascending=False)
            
            fig_dest = px.bar(
                destinos,
                x='Tienda_Destino',
                y='Cantidad',
                color='Costo_Transferencia',
                color_continuous_scale='Blues',
                labels={'Cantidad': 'Unidades Recibidas', 'Tienda_Destino': 'Tienda'}
            )
            st.plotly_chart(fig_dest, use_container_width=True)
        
        # Análisis por SKU
        st.subheader("Productos Más Transferidos")
        skus = trans_filtered.groupby('SKU').agg({
            'Cantidad': 'sum',
            'Costo_Transferencia': 'sum'
        }).reset_index().sort_values('Cantidad', ascending=False).head(10)
        
        fig_sku = px.bar(
            skus,
            x='SKU',
            y='Cantidad',
            color='Costo_Transferencia',
            color_continuous_scale='Viridis',
            labels={'Cantidad': 'Unidades Transferidas'}
        )
        fig_sku.update_layout(height=400)
        st.plotly_chart(fig_sku, use_container_width=True)
        
    else:
        st.info("No se recomiendan transferencias en este escenario. Los niveles de stock actuales son adecuados.")
    
    st.markdown("---")
    
    # Sección: Comparación de todos los escenarios
    st.header("Análisis Global de Escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Costo Total por Escenario")
        fig_total = px.bar(
            comparacion_df,
            x='Escenario',
            y='Costo_Total',
            color='Costo_Total',
            color_continuous_scale='RdYlGn_r',
            labels={'Costo_Total': 'Costo Total ($)'}
        )
        st.plotly_chart(fig_total, use_container_width=True)
    
    with col2:
        st.subheader("Número de Transferencias")
        fig_num = px.bar(
            comparacion_df,
            x='Escenario',
            y='Num_Transferencias',
            color='Num_Transferencias',
            color_continuous_scale='Blues',
            labels={'Num_Transferencias': 'Cantidad'}
        )
        st.plotly_chart(fig_num, use_container_width=True)
    
    # Tabla resumen de todos los escenarios
    st.subheader("Resumen Comparativo")
    st.dataframe(
        comparacion_df.style.format({
            'Costo_Transferencias': '${:.2f}',
            'Costo_Rotura': '${:.2f}',
            'Costo_Exceso': '${:.2f}',
            'Costo_Total': '${:.2f}',
            'Num_Transferencias': '{:.0f}',
            'Unidades_Transferidas': '{:.0f}'
        }).background_gradient(subset=['Costo_Total'], cmap='RdYlGn_r'),
        use_container_width=True
    )
    
    # Información adicional
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        ### Acerca del Dashboard
        
        Este dashboard muestra los resultados del modelo prescriptivo 
        de optimización de transferencias entre tiendas.
        
        **Modelo:** Programación Lineal (PuLP)
        
        **Objetivo:** Minimizar costos totales considerando:
        - Costos de transferencia
        - Costos de rotura de stock
        - Costos de obsolescencia
        
        **Restricciones:**
        - Stock de seguridad
        - Demanda proyectada
        - Disponibilidad de inventario
        """
    )

else:
    st.warning("No se pudieron cargar los datos. Ejecute el notebook de análisis primero.")
