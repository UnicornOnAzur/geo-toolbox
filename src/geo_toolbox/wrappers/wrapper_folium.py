# Standard library
import io
import typing
# Third party
import folium
import geopandas as gpd
import matplotlib as mpl
import pandas as pd
import PIL


def folium_to_picture(
    map_: folium.Map
        ) -> None:
    """
    Converts a Folium map to a PNG image and saves it as 'folium.png'.

    Parameters:
    map_: A Folium map object that needs to be converted to an image.

    Returns:
    None
    """
    img_data: bytes = map_._to_png()
    img: PIL.PngImagePlugin.PngImageFile =\
        PIL.Image.open(io.BytesIO(img_data))
    img.save("folium.png")


def folium_to_html(
    map_: folium.Map
        ) -> None:
    """
    Save a Folium map to an HTML file.

    Parameters:
    map_: A Folium Map object that needs to be saved.

    Returns:
    None
    """
    map_.save("folium.html")


def folium_to_binary(
    map_: folium.Map
        ) -> None:
    """
    Converts a Folium map object to a binary file.

    Parameters:
    map_: A Folium map object that needs to be saved as a binary file.

    Returns:
    None
    """
    with open("folium.txt", "wb") as file:
        file.write(map_._to_png())


def make_map(
    file_list: str
        ) -> str:
    """
    Generates a folium map with GPX tracks.

    This function reads GPX files, extracts their coordinates, and creates a
    map with polylines representing the tracks that is fitted to the extent of
    the tracks.

    Parameters:
        file_list : An optional list of GPX files to be plotted on the map.

    Returns:
        The rendered HTML representation of the folium map.
    """
    colormap: typing.List[str] = list(map(mpl.colors.to_hex,
                                          mpl.colormaps["Set1"].colors))
    map_: folium.Map = folium.Map()
    gdfs: typing.List[gpd.GeoDataFrame] = []
    for file_name, color in zip(file_list, colormap):
        # Read the GPX file into a GeoDataFrame from the "tracks" layer and add
        # it to the list.
        gdf: gpd.GeoDataFrame = gpd.read_file(file_name, layer="tracks")
        gdfs.append(gdf)
        #  Create a FeatureGroup for the current file to hold its polyline and
        # add that to the map
        lines_layer: folium.FeatureGroup = folium.FeatureGroup(name=file_name)
        folium.PolyLine(locations=gdf.geometry.get_coordinates()[["y", "x"]],
                        color=color).add_to(lines_layer)
        lines_layer.add_to(map_)
    # Fit the extent of the map to the tracks
    xmin, ymin, xmax, ymax = pd.concat(gdfs).total_bounds if gdfs\
        else [-50, -50, 50, 50]
    map_.fit_bounds([[ymin, xmin], [ymax, xmax]])
    return folium.Figure().add_child(map_).render()


if __name__ == "__main__":
    pass
