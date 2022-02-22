import streamlit as st
import json as json
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots
from copy import deepcopy
st.title("Renewable Power Plans in Switzerland")
st.header("Power Plants DataFrame")

clean_energy_ch_raw = pd.read_csv("../sit_academy_streamlit/data/raw/renewable_power_plants_CH.csv")
clean_energy_ch = clean_energy_ch_raw

if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=clean_energy_ch)

st.subheader("Number of Clean Energy Sources per Canton")

with open("../sit_academy_streamlit/data/raw/georef-switzerland-kanton.geojson") as response:
    cantons = json.load(response)
cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

clean_energy_ch["canton_name"] = clean_energy_ch["canton"].map(cantons_dict)
sources_per_canton = clean_energy_ch.groupby("canton_name").size().reset_index(name="count")
fig = px.choropleth_mapbox(
    sources_per_canton,
    color="count",
    geojson=cantons,
    locations="canton_name",
    featureidkey="properties.kan_name",
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="open-street-map",
    zoom=6.3,
    opacity=0.8,
    width=900,
    height=500,
    labels={"canton_name":"Canton",
           "count":"Number of Sources"},
    title="<b>Number of Clean Energy Sources per Canton</b>",
    color_continuous_scale="Cividis",
)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font={"family":"Sans",
                       "color":"maroon"},
                  hoverlabel={"bgcolor":"white",
                              "font_size":12,
                             "font_family":"Sans"},
                  title={"font_size":20,
                        "xanchor":"left", "x":0.01,
                        "yanchor":"bottom", "y":0.95}
                 )
st.plotly_chart(fig)

st.header("Sources per Canton")

left_column, middle_column, right_column  = st.columns([1.8, 1, 1])
# Widgets: selectbox
cantons = ["All"]+sorted(pd.unique(sources_per_canton["canton_name"]))
canton = left_column.selectbox("Choose a Canton", cantons)

if canton == "All":
    reduced_df = sources_per_canton
else:
    reduced_df = sources_per_canton[sources_per_canton["canton_name"] == canton]

left_column.dataframe(reduced_df)

fig_1 = px.bar(reduced_df, x="canton_name", y="count", title="Sources per Canton")
middle_column.plotly_chart(fig_1)
