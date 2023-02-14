import streamlit as st
import pandas as pd
import os
from streamlit_folium import st_folium, folium_static

from utils import get_gdf, display

def init_state(state):
    if "map" not in state:
        image_path= "small"
        csv_path="bm18_data3_0pass1_freq0_big1_pa100_t12_eq1_lc1.csv"
        files = os.listdir(image_path)
        rdf = pd.read_csv(csv_path, header=None)

        rdf = rdf[(rdf[0]==4)&(rdf[4]>0)]
        gdf = get_gdf(rdf, files)
        m = display(gdf, image_path)
        state.map = m
        folium_static(state.map, width=1200, height=800)
        
        
    return state

    
st.set_page_config(layout="wide",
                   page_title='Biomass', page_icon = 'evergreen_tree')
st.title(':evergreen_tree: Biomass recovery after fire - Yidi Xu@LSCE')
state = st.session_state
init_state(state)

# st.markdown(state.map._repr_html_(), unsafe_allow_html =True)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: left;
}
</style>
<div class="footer">
<p> &nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp; Website developed with ❤ by <a href="https://defve1988.github.io/" target="_blank"> Chuanlong Zhou</a> @ LSCE</p>
<p> </p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
