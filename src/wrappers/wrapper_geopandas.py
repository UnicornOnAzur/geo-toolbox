# Standard library
import io
import pathlib
import tempfile
import typing
import zipfile
# Third party
import geopandas as gpd
# Constant
DEFAULT_CRS: str = "EPSG:4087"


def to_crs_lbyl(
    gdf: gpd.GeoDataFrame,
    crs: typing.Union[int, str]
        ) -> gpd.GeoDataFrame:
    """
    Transform a GeoDataFrame to a specified CRS using the 'Look Before You
    Leap' method.

    Parameters:
        gdf : The GeoDataFrame to transform.
        crs : The target CRS.

    Returns:
        The transformed GeoDataFrame.
    """
    if gdf.crs is None:
        gdf.set_crs(DEFAULT_CRS, inplace=True)
    return gdf.to_crs(crs)


def to_crs_eafp(
    gdf: gpd.GeoDataFrame,
    crs: typing.Union[int, str]
        ) -> gpd.GeoDataFrame:
    """
    Transform a GeoDataFrame to a specified CRS using the 'Easier to Ask for
    Forgiveness than Permission' method.

    Parameters:
        gdf : The GeoDataFrame to transform.
        crs : The target CRS.

    Returns:
        The transformed GeoDataFrame.
    """
    try:
        return gdf.to_crs(crs)
    except ValueError:
        return gdf.set_crs(DEFAULT_CRS).to_crs(crs)


def geopandas_to_geojson(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a GeoJSON file.

    Parameters:
    gdf: A GeoDataFrame containing geometrical data.

    Returns:
    None
    """
    gdf.to_file("geopandas.geojson", driver="GeoJSON")


def geopandas_to_shapefile(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a shapefile.

    Parameters:
    gdf: A GeoDataFrame containing geometrical data.

    Returns:
    None: This function does not return any value.
    """
    gdf.to_file("geopandas.shp", driver="ESRI Shapefile")


def geopandas_to_zipped_shapefile(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a zipped shapefile.

    Parameters:
    gdf: A GeoDataFrame containing the geographical data to be converted.

    Returns:
    None: This function does not return any value.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path: pathlib.Path = pathlib.Path(temp_dir)
        gdf.to_file(f"{temp_dir_path}/geopandas.shp", driver="ESRI Shapefile")
        with zipfile.ZipFile("geopandas.zip", "w") as zip_file:
            for file in temp_dir_path.glob("*"):
                zip_file.write(file, arcname=file.name)


def geopandas_to_binary2(
    gdf: gpd.GeoDataFrame
        ) -> None:
    """
    Converts a GeoDataFrame to a binary format and saves it to a file.

    Parameters:
    gdf: A GeoDataFrame containing geospatial data.

    Returns:
    None
    """
    with io.BytesIO() as buffer:
        gdf.to_file(buffer, driver="GeoJSON")
        buffer.seek(0)  # Move to the beginning of the buffer
        with open("geopandas_binary2.txt", "wb") as file:
            file.write(buffer.getvalue())


if __name__ == "__main__":
    pass
