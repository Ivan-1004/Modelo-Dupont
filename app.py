
import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Modelo FEL", layout="wide")
st.title("💸 Modelo de Flujo de Efectivo Libre (FEL)")

with st.sidebar:
    st.header("📥 Instrucciones de uso")
    st.markdown(
        "- Sube un **Excel (.xlsx)** con la primera columna llamada **Indicador**.\n"
        "- Los encabezados de columna deben ser los **períodos** (años/meses).\n"
        "- Deben existir estas filas: **EBIT, Depreciación, Cuentas por cobrar, Inventarios, Proveedores**."
    )

    # Descargar plantilla de ejemplo
    st.subheader("Plantilla de ejemplo")
    plantilla = pd.DataFrame({
        "Indicador": ["EBIT", "Depreciación", "Cuentas por cobrar", "Inventarios", "Proveedores"],
        "1992": [None]*5,
        "1993": [None]*5,
        "1994": [None]*5,
        "1995": [None]*5,
        "1996": [None]*5,
    })
    buf_tpl = io.BytesIO()
    with pd.ExcelWriter(buf_tpl, engine="openpyxl") as w:
        plantilla.to_excel(w, index=False, sheet_name="Base")
    buf_tpl.seek(0)
    st.download_button(
        "Descargar plantilla.xlsx",
        data=buf_tpl,
        file_name="plantilla_fel.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

archivo = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

def _find_indicator_column(columns):
    for c in columns:
        if str(c).strip().lower() in {"indicador", "indicator"}:
            return c
    return None

def _coerce_numeric(df):
    # Convierte todas las columnas excepto el índice a numérico
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

if archivo is not None:
    # Leer
    df_raw = pd.read_excel(archivo, sheet_name=0)
    ind_col = _find_indicator_column(df_raw.columns)

    if ind_col is None:
        st.error("No se encontró la columna **Indicador**. Renombra la primera columna a 'Indicador'.")
        st.stop()

    df = df_raw.copy()
    df = df.set_index(ind_col)
    df.index = df.index.astype(str).str.strip()

    # Mantener solo columnas numéricas (los periodos)
    df = df.apply(pd.to_numeric, errors="coerce")
    df = _coerce_numeric(df)

    requeridos = ["EBIT", "Depreciación", "Cuentas por cobrar", "Inventarios", "Proveedores"]
    faltantes = [r for r in requeridos if r not in df.index]
    if faltantes:
        st.error(f"Faltan los siguientes indicadores en tu archivo: {', '.join(faltantes)}")
        st.stop()

    # Series base
    EBIT = df.loc["EBIT"]
    Dep = df.loc["Depreciación"]
    CxC = df.loc["Cuentas por cobrar"]
    Inv = df.loc["Inventarios"]
    Prov = df.loc["Proveedores"]

    # Cálculos
    EBITDA = EBIT + Dep
    dCxC = CxC.diff().fillna(0)
    dInv = Inv.diff().fillna(0)
    dProv = Prov.diff().fillna(0)
    VarCT = dCxC + dInv - dProv
    FEL = EBITDA - VarCT

    # Tabla final (filas = indicadores, columnas = periodos)
    resultado = pd.DataFrame({
        "EBITDA": EBITDA,
        "Δ CxC": dCxC,
        "Δ Inventarios": dInv,
        "Δ Proveedores": dProv,
        "Variación CT": VarCT,
        "FEL (antes CapEx e impuestos)": FEL,
    }).T

    # Redondeo a 1 decimal
    resultado = resultado.round(1)

    st.subheader("📊 Resultado del Modelo FEL")
    st.dataframe(resultado.style.format("{:,.1f}"), use_container_width=True)

    # Descarga en Excel
    export_buf = io.BytesIO()
    with pd.ExcelWriter(export_buf, engine="openpyxl") as writer:
        resultado.to_excel(writer, index=True, sheet_name="FEL")
    export_buf.seek(0)
    st.download_button(
        "📥 Descargar resultados en Excel",
        data=export_buf,
        file_name="Modelo_FEL_Resultados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # Mostrar datos fuente opcionalmente
    with st.expander("Ver datos originales cargados"):
        st.dataframe(df_raw, use_container_width=True)

else:
    st.info("Carga un archivo Excel para calcular el FEL o descarga la plantilla desde la barra lateral.")
