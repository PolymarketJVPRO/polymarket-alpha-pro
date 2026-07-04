import io
import pandas as pd
import streamlit as st
import plotly.express as px

from app.config import APP_NAME, DEFAULT_LIMIT, MIN_VOLUME, MIN_LIQUIDITY
from app.services.polymarket import fetch_markets
from app.scoring.engine import apply_scoring

st.set_page_config(page_title=APP_NAME, page_icon="📈", layout="wide")

st.title("📈 Polymarket Alpha Pro")
st.caption("Scanner de mercados + Opportunity Score + decisión BUY YES / BUY NO / NO TRADE")

with st.sidebar:
    st.header("Filtros")
    limit = st.slider("Mercados a descargar", 50, 500, DEFAULT_LIMIT, 50)
    min_volume = st.number_input("Volumen mínimo", min_value=0, value=MIN_VOLUME, step=1000)
    min_liquidity = st.number_input("Liquidez mínima", min_value=0, value=MIN_LIQUIDITY, step=500)
    text_filter = st.text_input("Buscar texto", "")
    st.divider()
    st.write("Regla v1")
    st.write("Score ≥ 85: BUY YES / WATCH CLOSELY")
    st.write("Score 70–84: WATCHLIST")
    st.write("Score < 70: NO TRADE")

@st.cache_data(ttl=300)
def load_data(limit):
    df = fetch_markets(limit)
    df = apply_scoring(df)
    return df

try:
    df = load_data(limit)
except Exception as e:
    st.error(f"No pude descargar mercados de Polymarket: {e}")
    st.stop()

filtered = df[(df["volume"] >= min_volume) & (df["liquidity"] >= min_liquidity)].copy()
if text_filter:
    filtered = filtered[filtered["title"].str.contains(text_filter, case=False, na=False)]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Mercados", len(filtered))
col2.metric("Mejor score", f"{filtered['score'].max():.1f}" if len(filtered) else "N/A")
col3.metric("Volumen total", f"${filtered['volume'].sum():,.0f}")
col4.metric("Liquidez total", f"${filtered['liquidity'].sum():,.0f}")

st.subheader("🔥 Top oportunidades")
show_cols = ["decision", "score", "yes_pct", "volume", "liquidity", "category", "title", "url"]
st.dataframe(
    filtered[show_cols].head(50),
    use_container_width=True,
    column_config={
        "url": st.column_config.LinkColumn("Abrir"),
        "yes_pct": st.column_config.NumberColumn("YES %", format="%.1f%%"),
        "volume": st.column_config.NumberColumn("Volumen", format="$%.0f"),
        "liquidity": st.column_config.NumberColumn("Liquidez", format="$%.0f"),
    },
    hide_index=True,
)

if len(filtered):
    st.subheader("📊 Score vs Volumen")
    fig = px.scatter(
        filtered.head(100),
        x="volume",
        y="score",
        size="liquidity",
        hover_name="title",
        hover_data=["yes_pct", "category", "decision"],
        log_x=True,
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🧠 Lectura rápida")
if len(filtered):
    best = filtered.iloc[0]
    st.markdown(
        f"""
**Mejor mercado detectado:** {best['title']}  
**Decisión:** {best['decision']}  
**Score:** {best['score']}/100  
**YES actual:** {best['yes_pct']:.1f}%  
**Volumen:** ${best['volume']:,.0f} | **Liquidez:** ${best['liquidity']:,.0f}
"""
    )
    if best['score'] < 70:
        st.warning("Lectura v1: NO TRADE. Hay volumen/liquidez, pero no suficiente edge confirmado.")
    elif best['score'] < 85:
        st.info("Lectura v1: WATCHLIST. Vigilar, no comprar automáticamente.")
    else:
        st.success("Lectura v1: posible BUY YES / WATCH CLOSELY. Confirmar noticias, edge y riesgo antes de entrar.")
else:
    st.info("No hay mercados que cumplan los filtros.")

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Descargar CSV", csv, "polymarket_alpha_results.csv", "text/csv")

st.caption("Aviso: herramienta educativa. No es asesoría financiera ni garantiza resultados.")
