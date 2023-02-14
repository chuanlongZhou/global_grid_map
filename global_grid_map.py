from shapely.geometry import Polygon
import geopandas

def create_polygon(box):
    """create box polygon for clipping the geopands df
    """
    (max_lat, min_lon), (min_lat, max_lon) = box
    return Polygon([(min_lon, max_lat), 
                    (min_lon, min_lat), 
                    (max_lon, min_lat), 
                    (max_lon, max_lat), 
                    (min_lon, max_lat)])

class GlobalGridMap:
    def __init__(self, grid_size=1, crs="epsg:4326"):
        self.grid_size = grid_size
        self.crs = crs
        
        self.gdf = None
    
    def make_grid(self, polygon_dict, other_data={}):
        d = polygon_dict.update(other_data)
        self.gdf = geopandas.GeoDataFrame(d, crs=self.crs)
        