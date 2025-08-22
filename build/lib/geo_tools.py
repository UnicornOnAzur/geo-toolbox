"""
author: UnicornOnAzur

This module provides functions to extract geographical coordinates from
GeoJSON files, calculate centroids, means, medians, and determine geographical
bounds using the Shapely and NumPy libraries.
"""
# Standard library
import typing
# Third party
import geojson
import numpy as np
import shapely


def _extract_coordinates_from_geojson(
    geojson_file: str
        ) -> typing.Tuple[typing.List[float], typing.List[float]]:
    """
    Extract latitude and longitude coordinates from a GeoJSON file.

    Parameters:
        geojson_file : Path to the GeoJSON file.

    Returns:
        A tuple containing lists of latitudes and longitudes.
    """
    coordinates = []

    # Load GeoJSON data and map coordinates
    with open(geojson_file) as file:
        geojson.utils.map_coords(lambda coord: coordinates.append(coord),
                                 geojson.load(file))

    # Separate latitude and longitude, the order is [lon, lat, lon, lat, ...]
    latitudes: typing.List[float] = coordinates[1::2]
    longitudes: typing.List[float] = coordinates[::2]

    return latitudes, longitudes


def get_centroid(
    bytes_object: bytes
        ) -> typing.Dict:
    """
    Calculate the centroid of a GeoJSON polygon using shapely. The returned
    point is in longitude/latitude and therefore, the outcome is reversed.

    Parameters:
        bytes_object : bytes : The GeoJSON data in bytes.

    Returns:
        A dictionary containing the latitude and longitude of the centroid.
    """
    polygon: shapely.GeometryCollection = shapely.from_geojson(bytes_object)
    centroid: shapely.Point = shapely.centroid(polygon)
    center: typing.Dict = dict(zip(["lat", "lon"],
                               list(*centroid.coords)[::-1]))
    return center


def get_mean(
    geojson_file: str
        ) -> typing.Dict[str, float]:
    """
    Calculate the mean latitude and longitude from a GeoJSON file.

    Parameters:
        geojson_file : Path to the GeoJSON file.

    Returns:
        A dictionary containing the mean latitude and longitude.
    """
    latitudes, longitudes = _extract_coordinates_from_geojson(geojson_file)

    # Return median of latitudes and longitudes
    return {"lat": np.mean(latitudes),
            "lon": np.mean(longitudes)}


def get_median(
    geojson_file: str
        ) -> typing.Dict[str, float]:
    """
    Calculate the median latitude and longitude from a GeoJSON file.

    Parameters:
        geojson_file : Path to the GeoJSON file.

    Returns:
        A dictionary containing the median latitude and longitude.
    """
    latitudes, longitudes = _extract_coordinates_from_geojson(geojson_file)

    # Return median of latitudes and longitudes
    return {"lat": np.median(latitudes),
            "lon": np.median(longitudes)}


def determine_bounds(
    geojson_file: str
        ) -> typing.List[float]:
    """
    Extracts the geographical bounds (minimum and maximum latitudes and
    longitudes) from a GeoJSON file.

    Parameters:
        geojson_file : The path to the GeoJSON file.

    Returns:
        A tuple containing the minimum longitude, minimum latitude, maximum
        longitude, and maximum latitude.
    """
    latitudes, longitudes = _extract_coordinates_from_geojson(geojson_file)
    return [min(longitudes), min(latitudes), max(longitudes), max(latitudes)]


if __name__ == "__main__":
    pass
