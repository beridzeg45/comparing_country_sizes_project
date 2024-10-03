import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.affinity import translate
import warnings
import os

warnings.filterwarnings('ignore')
plt.style.use('ggplot')

# load the world shapefile
world = gpd.read_file("world-administrative-boundaries/world-administrative-boundaries.shp")

default_selected_countries = ['Georgia','Iceland']
colors = ['deepskyblue', 'orange','lawngreen','red','pink','grey','olive','purple','aqua','lavender']

def return_geopandas_graph(selected_countries):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    areas = []

    ax1.set_facecolor('black')
    fig1.patch.set_facecolor('black')  

    
    ax2.set_facecolor('black')  
    fig2.patch.set_facecolor('black') 

    if len(selected_countries) > 10:
        st.error('Please select no more than 10 countries')
        return None, None

    world_equal_area = world.to_crs('+proj=moll')#'(+proj=aea +lat_1=20 +lat_2=50 +lon_0=0')#'+proj=moll')

    for i, selected_country in enumerate(selected_countries):
        country_df = world_equal_area[world_equal_area['name'] == selected_country]

        if country_df.empty:
            continue

        area = int(country_df.to_crs(epsg=6933).geometry.area.iloc[0] / 10**6)
        areas.append(area)

        if i == 0:
            example = country_df
            example_x = example.geometry.centroid.iloc[0].x
            example_y = example.geometry.centroid.iloc[0].y
        if 'United States of America' or 'Russian Federation' in selected_countries:
            example_x,example_y=0,0

        country_x = country_df.geometry.centroid.iloc[0].x
        country_y = country_df.geometry.centroid.iloc[0].y

        x_offset = example_x - country_x
        y_offset = example_y - country_y

        country_translated = country_df.geometry.apply(lambda geom: translate(geom, xoff=x_offset, yoff=y_offset))
        country_df.geometry = country_translated
        country_df.plot(ax=ax1, edgecolor='black', color=colors[i % len(colors)], alpha=.7)

        ax1.set_title(f"Country Sizes Compared: {', '.join(selected_countries)}", fontweight='bold',size=10,color='white')
        ax1.axis('off')

        #dealing with individual boundaries
        if 'United States of America' in selected_countries:
            ax1.set_xlim(-5*10**6,5*10**6)
            ax1.set_ylim(-2.5*10**6,3*10**6)
        if 'Russian Federation' in selected_countries:
            ax1.set_xlim(-5*10**6,7*10**6)
            ax1.set_ylim(-2.5*10**6,3*10**6)


    ax2.bar(selected_countries, areas, color=colors[:len(selected_countries)])
    #ax2.set_ylabel('km²',color='white')
    ax2.set_yticklabels([])
    ax2.set_title('Country Sizes Compared Using Bar Chart', fontweight='bold',size=10,color='white')
    for i in range(len(selected_countries)):
        ax2.text(i, areas[i], f'{areas[i]:,} km2', ha='center', va='bottom', size=8 if len(selected_countries)<=5 else 5 ,fontweight='bold',rotation=0,color='white')
    ax2.tick_params(axis='x', labelsize=8,rotation=45,color='white')
    ax2.set_xticklabels(selected_countries,color='white')
    ax2.grid(False) 
    
    # Remove spines (borders) for ax2
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    return fig1, fig2

# Streamlit app
st.set_page_config(layout="wide")
st.header('Comparing Country Sizes 🌍- Python Project By Giorgi Beridze')
st.subheader('Visit my [GitHub](https://github.com/beridzeg45) account for code')

selected_countries = st.multiselect(label='Select Countries', options=[''] + list(world['name'].unique()), default=default_selected_countries,label_visibility="hidden")
fig1, fig2 = return_geopandas_graph(selected_countries)

if fig1 and fig2:
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)  
    with col2:
        st.pyplot(fig2)  
