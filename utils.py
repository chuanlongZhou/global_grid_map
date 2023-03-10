from shapely.geometry import Polygon
import geopandas
import folium
import base64
import streamlit as st

from folium import IFrame
import os


def create_polygon(box):
    """create box polygon for clipping the geopands df
    """
    (max_lat, min_lon), (min_lat, max_lon) = box
    return Polygon([(min_lon, max_lat), 
                    (min_lon, min_lat), 
                    (max_lon, min_lat), 
                    (max_lon, max_lat), 
                    (min_lon, max_lat)])
    
def get_gdf(rdf, files, image_path=""):
    lat =[]
    lon =[]
    R2 =[]
    geometry =[]
    file =[]
    RT = []
    added =[]
    for index, row in rdf.iterrows():
        la, lo, r2, rt = int(row[1]), int(row[2]), row[4], row[15]
        if rt>100:
            rt=100
        f = [files.index(l) for l in files if l.startswith(f"{la}_{lo}")]
        
        lat.append(la)
        lon.append(lo)
        R2.append(r2)
        RT.append(rt)
        geometry.append(create_polygon(((la,lo+1),(la-1, lo))))
        
        f_temp = None if len(f)==0 else files[f[0]]
        f_temp = None if f_temp is None else os.path.join(image_path, f_temp)
        file.append(f_temp)
        if f_temp is not None:
            added.append(files[f[0]])
        

    for ff in files:
        if ff not in added:
            la = int(ff.split("_")[0])
            lo = int(ff.split("_")[1])
            f = [files.index(l) for l in files if l.startswith(f"{la}_{lo}")]
            lat.append(la)
            lon.append(lo)
            R2.append(None)
            RT.append(None)
            geometry.append(create_polygon(((la,lo+1),(la-1, lo))))
            f_temp = None if len(f)==0 else files[f[0]]
            f_temp = None if f_temp is None else os.path.join(image_path, f_temp)
            file.append(f_temp)
        
    d = {'lat': lat, 'lon': lon, "r2":R2, "recovery time":RT, "file":file, "geometry": geometry}
    gdf = geopandas.GeoDataFrame(d, crs='epsg:4326')
    return gdf


def display(gdf, progressbar=False):
    # color_map = MplColorHelper("autumn_r",0,1)
    # m = folium.Map()
    m = gdf.explore(name="r2", column="r2", cmap="Reds",style_kwds={"weight":0.5})
    gdf.explore(name="recovery time", column="recovery time", cmap="YlGn",style_kwds={"weight":0.5}, m=m)

    fg = folium.FeatureGroup(name="plots", show=True)
    if progressbar:
        progress_text = "Loading images. Please wait."
        my_bar = st.progress(0, text=progress_text)
    
    # create a geojson layer for each feature
    for i, r in gdf.iterrows():
        # print(i)
        if progressbar:
            my_bar.progress((i + 1)/len(gdf), text=progress_text)

        # if i%3!=0 or r["file"] is None:
        #     continue
        # geodataframe of row
        gdf_ = geopandas.GeoDataFrame(r.to_frame().T, crs=gdf.crs)
        
        scr = ""
        opacity=0
        if r["file"] is not None:
            f_path = r["file"]
            encoded = base64.b64encode(open(f_path, 'rb').read())
            scr = "data:image/png;base64," + encoded.decode("utf-8")
        # URI encoded image of plotly figure
        img_ = f'<img width="450" height="450" src="{scr}"/>'
        
        html = '<img src="data:image/JPG;base64,{}">'.format
        iframe = IFrame(html(encoded.decode("UTF-8")), width=450, height=450)

        choro_ = folium.GeoJson(
            gdf_.__geo_interface__,
            name=r["file"],
            # note: this one can apply for only once, the last one
            style_function=lambda x: {"fillOpacity":0,
                                    #   "stroke":True,
                                    #   "color":"red" if r["file"] is None else "blue",
                                    "opacity":0,
                                    "weight":5},
            tooltip=folium.GeoJsonTooltip(gdf_.drop(columns=["file", "geometry"]).columns.tolist()),
            # popup=folium.Popup(iframe),
        )
        # this is the real work around, add to layer which is a choro
        folium.Popup(img_).add_to(choro_)
        choro_.add_to(fg)

    fg.add_to(m)
    folium.LayerControl().add_to(m)
    if progressbar:
        my_bar.empty()
    return m