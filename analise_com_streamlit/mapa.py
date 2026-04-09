import streamlit as st
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer
from sidebar import render_sidebar

if "dados_processados" not in st.session_state:
    st.warning("Acesse a página 'Main Page' para carregar os dados primeiro.")
    st.stop()

dataset = render_sidebar(st.session_state.dados_processados)

st.title("Mapa Geográfico — Renda Per Capita")

# Converter WGS84 (lat/lon) para Web Mercator (projeção usada pelos tiles)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
x, y = transformer.transform(dataset['LON'].values, dataset['LAT'].values)

fig, ax = plt.subplots(figsize=(12, 10))
sc = ax.scatter(
    x, y,
    c=dataset['renda_per_capita'],
    cmap='RdYlGn',
    s=2,
    alpha=0.7,
    vmin=dataset['renda_per_capita'].quantile(0.05),
    vmax=dataset['renda_per_capita'].quantile(0.95)
)
plt.colorbar(sc, ax=ax, label='Renda Per Capita (R$)')
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
ax.set_title('Renda Per Capita por Localização Geográfica', fontsize=14)
plt.tight_layout()
st.pyplot(fig)




