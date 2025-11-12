import streamlit as st
import pandas as pd
import numpy as np
import re
from pathlib import Path

st.set_page_config(page_title="Dashboard Prescriptivo Retail", layout="wide")
BASE = Path(".")

# --------------------------- Utils ---------------------------

def slugify(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z_-]+", "_", s)

@st.cache_data
def load_resumen_escenarios():
    df = pd.read_csv(BASE / "resumen_escenarios.csv")
    # Ordenar por número si vienen como "Escenario 1..5"
    try:
        df["_n"] = df["escenario"].str.extract(r"(\d+)").astype(float)
        df = df.sort_values(["_n", "escenario"]).drop(columns=["_n"])
    except Exception:
        df = df.sort_values("escenario")
    return df

@st.cache_data
def load_ventas():
    ventas = pd.read_csv(BASE / "ventas.csv", parse_dates=["fecha"])
    ventas["periodo"] = ventas["fecha"].dt.to_period("M").astype(str)
    ventas["periodo"] = pd.to_datetime(ventas["periodo"] + "-01")
    return ventas

@st.cache_data
def load_escenario_files(escenario: str):
    slug = slugify(escenario)
    dfQ = pd.read_csv(BASE / f"plan_pedidos_optimo__{slug}.csv")
    dfI = pd.read_csv(BASE / f"inventario_proyectado__{slug}.csv")
    dfB = pd.read_csv(BASE / f"backorders_proyectados__{slug}.csv")

    # periodo puede venir como 'YYYY-MM'
    for df in (dfQ, dfI, dfB):
        if "periodo" in df.columns and df["periodo"].dtype == object:
            df["periodo"] = pd.to_datetime(df["periodo"] + "-01", errors="coerce")

    por_tienda = "tienda" in dfQ.columns
    return dfQ, dfI, dfB, por_tienda

# --------------------------- Header ---------------------------

st.title("Dashboard Prescriptivo — Reabastecimiento Multi-Periodo")

# ------------------ Sección 1: Comparación escenarios ------------------

st.subheader("Comparación de escenarios (costo vs servicio)")
resumen = load_resumen_escenarios()

colA, colB = st.columns([2, 1])
with colA:
    st.markdown("**Costo total por escenario**")
    st.bar_chart(resumen.set_index("escenario")["costo_total"])
with colB:
    st.dataframe(
        resumen[["escenario","estado","costo_total","nivel_servicio","backorders_totales"]]
        .assign(**{"nivel_servicio_%": lambda d: (d["nivel_servicio"] * 100).round(2)}),
        use_container_width=True, height=240
    )

colC, colD = st.columns(2)
with colC:
    st.markdown("**Nivel de servicio (%)**")
    st.bar_chart((resumen.set_index("escenario")["nivel_servicio"]*100).rename("Nivel de servicio (%)"))
with colD:
    st.markdown("**Backorders totales**")
    st.bar_chart(resumen.set_index("escenario")["backorders_totales"])

st.divider()

# ------------------ Sección 2: Drill-down por escenario/SKU ------------------

st.subheader("Detalle por escenario y SKU")

escenario_sel = st.selectbox("Escenario", resumen["escenario"].tolist())
dfQ, dfI, dfB, por_tienda = load_escenario_files(escenario_sel)
ventas = load_ventas()

# Claves
cols_key = ["tienda","sku","periodo"] if por_tienda else ["sku","periodo"]

# Filtros
left, right = st.columns([1,3])
with left:
    if por_tienda:
        tienda_sel = st.selectbox("Tienda", ["(todas)"] + sorted(dfQ["tienda"].unique().tolist()))
    else:
        tienda_sel = "(todas)"
    sku_sel = st.selectbox("SKU", sorted(dfQ["sku"].unique().tolist()))
    rango = st.date_input("Rango de periodos", [])

# Base filtrada
base = dfQ.copy()
if por_tienda and tienda_sel != "(todas)":
    base = base[base["tienda"] == tienda_sel]
base = base[base["sku"] == sku_sel]

if rango and len(rango) == 2:
    ini, fin = pd.to_datetime(rango[0]), pd.to_datetime(rango[1])
    base = base[(base["periodo"] >= ini) & (base["periodo"] <= fin)]

# Merge con I, B
df_plot = base.merge(dfI, on=cols_key, how="left").merge(dfB, on=cols_key, how="left")
df_plot = df_plot.rename(columns={"Q":"Pedidos", "I":"Inventario", "B":"Backorders"})

# ✅ AGREGACIÓN CORREGIDA (no duplicar 'periodo')
df_plot = (
    df_plot.groupby(cols_key, as_index=False)[["Pedidos","Inventario","Backorders"]]
           .sum()
)

# Demanda mensual agregada (evita multiplicar filas)
demanda_m = ventas.groupby(["sku","periodo"], as_index=False)["cantidad_vendida"].sum()
demanda_sel = demanda_m[demanda_m["sku"] == sku_sel].copy()
if rango and len(rango) == 2:
    demanda_sel = demanda_sel[(demanda_sel["periodo"] >= ini) & (demanda_sel["periodo"] <= fin)]

# Unir demanda y rellenar
df_plot = df_plot.merge(demanda_sel, on=["sku","periodo"], how="left")
df_plot[["cantidad_vendida","Inventario","Backorders","Pedidos"]] = (
    df_plot[["cantidad_vendida","Inventario","Backorders","Pedidos"]].fillna(0.0)
)
df_plot = df_plot.sort_values("periodo")

# ------------------ KPIs (sin sesgos por duplicados) ------------------

dem_total = float(df_plot["cantidad_vendida"].sum())
back_total = float(df_plot["Backorders"].sum())
ns_calc = None if dem_total == 0 else (1 - back_total/dem_total)
ns_calc = max(0.0, min(1.0, ns_calc)) if ns_calc is not None else None  # clamp 0..1

# Valor del modelo para cross-check (desde resumen_escenarios)
try:
    ns_modelo = float(resumen.loc[resumen["escenario"] == escenario_sel, "nivel_servicio"].iloc[0])
except Exception:
    ns_modelo = None

m1, m2, m3, m4 = right.columns(4)
m1.metric("Demanda", f"{dem_total:,.0f}")
m2.metric("Pedidos", f"{df_plot['Pedidos'].sum():,.0f}")
m3.metric("Backorders", f"{back_total:,.0f}")
m4.metric("Nivel de servicio", "-" if ns_calc is None else f"{100*ns_calc:.2f}%")

# (opcional) validación visual
if ns_modelo is not None:
    st.caption(f"Nivel de servicio del modelo para {escenario_sel}: **{100*ns_modelo:.2f}%**")

# Serie temporal
right.markdown(f"**Serie temporal — {escenario_sel} — SKU {sku_sel}**")
serie = df_plot.set_index("periodo")[["Pedidos","Inventario","Backorders"]]
st.line_chart(serie)

# Tabla
st.markdown("**Tabla de detalle**")
st.dataframe(df_plot[cols_key + ["Pedidos","Inventario","Backorders","cantidad_vendida"]], use_container_width=True)

# Descarga CSV detalle filtrado
csv_bytes = df_plot.to_csv(index=False).encode("utf-8")
st.download_button("Descargar detalle (CSV)", csv_bytes, file_name=f"detalle_{slugify(escenario_sel)}_{sku_sel}.csv")

st.caption("Nota: si trabajaste por tienda+SKU, usa el filtro de tienda. La demanda proviene de ventas.csv agregada por SKU y periodo, evitando duplicidad al unir.")
