import streamlit as st
import pandas as pd
import plotly.express as px
conda install matplotlib
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# ----------------------------------
# Configuración de la página
# ----------------------------------
st.set_page_config(
    page_title="Sistemas de Información Geográfica para la Gestión del Agua en la ASADA Santa Rosa, Río Nuevo, Pérez Zeledón, Costa Rica",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Sistemas de Información Geográfica para la Gestión del Agua en la ASADA Santa Rosa, Río Nuevo, Pérez Zeledón, Costa Rica")
st. header("Introducción")
st.markdown("""El recurso hídrico es fundamental para la existencia de la vida en el planeta; sin embargo, este a lo largo de la historia ha sido subestimado a nivel global, conduciéndonos a la condición actual, donde muchas poblaciones viven con escasez de este, ubicándolas en situaciones de alta vulnerabilidad.

A nivel nacional, aunque somos un país privilegiado, en cuanto a disponibilidad hídrica, en algunos casos se enfrentan dificultades relacionadas a su gestión, debido a la falta de recursos tanto económicos, como tecnológicos, especialmente en zonas rurales, donde normalmente quienes administran y suministran el recurso son las ASADAS, asociaciones
administradoras de acueductos que generalmente no tienen ingresos externos, si no que se sostienen con los pagos de sus usuarios.  


Se ha demostrado el éxito de los *Sistemas de Información Geográfica* en la gestión del recurso hídrico.

Este sitio web presenta una propuesta para desarrollar un sistema SIG que apoye la gestión del agua en una ASADA, utilizando datos geoespaciales y herramientas de análisis espacial""")

st.header("Descripción del tema")
st.markdown("""Un **Sistema de Información Geográfica** permite integrar datos espaciales con información alfanumérica para analizar fenómenos relacionados con el territorio. En el caso de la gestión del agua potable, los SIG pueden utilizarse para:

- Visualizar la ubicación de nacientes
- Analizar la red de distribución de agua
- Identificar zonas con alto consumo
- Evaluar la cobertura forestal alrededor de las fuentes de agua

La implementación de un sistema SIG puede mejorar significativamente la planificación y gestión de los recursos hídricos en comunidades rurales.

---""")

st.header("Datos geoespaciales utilizados")
st.markdown("""Para desarrollar este proyecto se pueden utilizar diferentes capas de información geográfica relacionadas con el sistema de agua potable.

Entre los datos más importantes se encuentran:

- **Ubicación de nacientes**
- **Red de tuberías**
- **Tanques de almacenamiento**
- **Ubicación de medidores de consumo**

Una de las fuentes más importantes para la obtención de esta información es el [SNIT](https://www.snitcr.go.cr/), sitio desde el cual se pueden descargar una importante variedad de capas relevantes para este sistema de información geográfica, además de la obtención de datos en campo como medio principal.""")

st.header("Variables principales del análisis")
st.markdown("""Las variables más relevantes que se pueden analizar en este sistema incluyen:

1. Ubicación geográfica de las nacientes
2. Consumo de agua por sector o usuario
3. Sectores con mayor cantidad de nacientes/disponibilidad hídrica
4. Estado de protección de las nacientes
5. Ubicación de la infraestructura del acueducto

El análisis de estas variables permite comprender mejor la relación entre el uso del territorio y la disponibilidad del recurso hídrico.

---""")

st.header("Problemas o preguntas de investigación")
st.markdown("""El análisis espacial de los datos puede ayudar a responder varias preguntas importantes relacionadas con la gestión del agua potable.

Entre las principales preguntas se encuentran:

- ¿Qué sectores de la comunidad presentan mayor consumo de agua?
- ¿Qué nacientes se encuentran en zonas con menor protección?
- ¿Existen áreas donde la red de distribución presenta mayor riesgo de fugas?
- ¿Qué zonas tienen mayor cantidad de usuarios?

Responder estas preguntas puede ayudar a mejorar la gestión del acueducto y promover un uso más sostenible del recurso hídrico.

---""")

st.header("Aplicaciones de los SIG en la gestión del agua")
st.markdown("""Los SIG ofrecen múltiples beneficios para la gestión del agua potable en comunidades rurales. Algunas de las aplicaciones más importantes incluyen:

- Monitoreo de la infraestructura del acueducto
- Identificación de fugas en la red de distribución
- Planificación de mantenimiento
- Protección de zonas de recarga hídrica
- Análisis del consumo de agua

El uso de estas herramientas permite una gestión más eficiente y sostenible del recurso.""")

# ----------------------------------
# Carga de datos
# ----------------------------------
@st.cache_data
def cargar_datos():
    return pd.read_csv("tarea.csv")

datos = cargar_datos()

# ----------------------------------
# Filtro lateral
# ----------------------------------
categorias = sorted(datos["Tipo de componente"].unique())

seleccion = st.sidebar.selectbox(
    "Tipo de componente",
    options=["(Todas)"] + list(categorias)
)

if seleccion == "(Todas)":
    datos_filtrados = datos
else:
    datos_filtrados = datos[
        datos["Tipo de componente"] == seleccion
    ]

# ----------------------------------
# Tabla de datos
# ----------------------------------
st.header("📋 Datos")

st.dataframe(
    datos_filtrados,
    use_container_width=True,
    hide_index=True
)

st.header ("Cantidad de usuarios por sector")
st.markdown("""La tabla muestra la cantidad de usuarios registrados en cada sector del sistema de acueducto.
Esto permite identificar cuáles sectores tienen mayor concentración de usuarios y mayor demanda potencial de agua.""")


# ----------------------------------
import pandas as pd

df = pd.read_csv("tarea.csv")

usuarios_sector = (
    df[df["Tipo de componente"] == "Usuario"]
    .groupby("Sector")
    .size()
    .reset_index(name="Cantidad de usuarios")
)

usuarios_sector

st.header("Cantidad de nacientes por sector")
st.markdown("""El gráfico muestra la cantidad de nacientes identificadas en cada sector del sistema de acueducto. Se observa que el sector Santa Rosa presenta la mayor cantidad de nacientes, con un total de 2, mientras que los sectores Berlín, El Roble y Villa Nueva cuentan con 1 naciente cada uno. Esta distribución indica que Santa Rosa posee una mayor disponibilidad de fuentes de agua dentro del sistema, aspecto que puede ser relevante para la planificación de la protección y gestión del recurso hídrico.""")
# ----------------------------------

# ----------------------------------
nacientes = df[df["Tipo de componente"] == "Naciente"]
nac_por_sector = nacientes.groupby("Sector").size()

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    nac_por_sector.index,
    nac_por_sector.values,
    color="skyblue"
)

ax.set_title("Cantidad de nacientes por sector")
ax.set_xlabel("Sector")
ax.set_ylabel("Número de nacientes")

st.pyplot(fig)

# ----------------------------------


st.header("Distribución del estado de las nacientes")
st.markdown("""El gráfico muestra el estado de protección de las nacientes registradas en el sistema. Se observa que el 80 % de las nacientes se encuentran protegidas, mientras que el 20 % están desprotegidas. Estos resultados reflejan un nivel favorable de conservación de las fuentes de agua; sin embargo, la existencia de nacientes sin protección evidencia la necesidad de implementar acciones de manejo y conservación para reducir riesgos de contaminación o afectación de la calidad y disponibilidad del recurso hídrico.""")

import matplotlib.pyplot as plt
import streamlit as st

# Filtrar solo nacientes
nacientes = df[df["Tipo de componente"] == "Naciente"]

# Contar estados
estados_nacientes = nacientes["Estado"].value_counts()

# Crear figura
fig, ax = plt.subplots(figsize=(6, 6))

# Gráfico de pie
ax.pie(
    estados_nacientes,
    labels=estados_nacientes.index,
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title("Distribución de estados de las nacientes")

# Mostrar en Streamlit
st.pyplot(fig)

# ----------------------------------
# ----------------------------------

st.header("Mapa de puntos de ubicación de componentes de la ASADA")
st.markdown("""Este mapa de puntos muestra la ubicación geográfica de los principales componentes del sistema de abastecimiento de agua administrado por la ASADA, incluyendo usuarios, tanques de almacenamiento. La simbología empleada permite diferenciar cada tipo de componente y visualizar su distribución dentro del área de estudio. Se observa una mayor concentración de usuarios en los sectores poblados, mientras que los tanques se localizan en puntos estratégicos para garantizar la distribución del recurso hídrico. Este mapa facilita la identificación de la infraestructura existente, el análisis de la cobertura del servicio y la planificación de actividades de mantenimiento, expansión y gestión del sistema.""")

import geopandas as gpd



# Cargar datos
df = pd.read_csv(
    "https://raw.githubusercontent.com/Yaha14/hola-streamlit/refs/heads/main/tarea.csv"
)

# Crear mapa base
m = folium.Map(
    location=[9.35, -83.75],
    zoom_start=12,
    tiles="CartoDB Positron"
)

# Colores por tipo de componente
colores = {
    "Usuario": "blue",
    "Tanque": "red",
    "Tubería": "green"
}

# Agregar elementos
for _, registro in df.iterrows():

    tipo = registro["Tipo de componente"]
    color = colores.get(tipo, "gray")

    folium.CircleMarker(
        location=[registro["Latitud"], registro["Longitud"]],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        tooltip=f"{tipo}",
        popup=folium.Popup(
            f"""
            <b>Tipo:</b> {tipo}<br>
            <b>Sector:</b> {registro['Sector']}<br>
            <b>ID:</b> {registro['ID']}
            """,
            max_width=250
        )
    ).add_to(m)

# Leyenda
legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 180px;
background-color: white;
border:2px solid black;
padding:10px;
z-index:9999;
font-size:14px;
">

<b>Tipo de componente</b><br><br>

<span style="color:blue;">●</span> Usuario<br>
<span style="color:red;">●</span> Tanque<br>
<span style="color:green;">●</span> Tubería

</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# Mostrar en Streamlit
st_folium(m, width=700, height=500)

# ----------------------------------

