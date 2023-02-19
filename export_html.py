import os
import pandas as pd
from utils import get_gdf, display

image_paths = [
    "/home/orchidee02/ydxu/AGBrecovery/1-data/TMF/4-30m-1deg_cf/bm18_data3_0pass1_freq0_big1_pa100_t12_eq1_lc1/figure/combf",
    "/home/orchidee03/ydxu/AGBrecovery/1-data/DEA/4-30m-1deg_cf/bm20_data3_0pass1_freq0_big1_pa100_t122_eq1_lc0/figure/combf"
]

csvs=[
    "/home/orchidee02/ydxu/AGBrecovery/1-data/TMF/4-30m-1deg_cf_noplot/allresult3/bm18_data3_0pass1_freq0_big1_pa100_t12_eq1_lc1.csv",
    "/home/orchidee03/ydxu/AGBrecovery/1-data/DEA/4-30m-1deg_cf_noplot/allresult2/bm20_data3_0pass1_freq0_big1_pa100_t122_eq2_lc0.csv"
]

gdf = None
for image_path, csv_path in zip(image_paths, csvs):
    files = os.listdir(image_path)
    rdf = pd.read_csv(csv_path, header=None)

    rdf = rdf[(rdf[0]==4)&(rdf[4]>0)]
    temp = get_gdf(rdf, files, image_path)
    if gdf is None:
        gdf = temp
    else:
        gdf = pd.concat([gdf, temp])
    
m = display(gdf)
m.save("map.html")

# print(gdf)
