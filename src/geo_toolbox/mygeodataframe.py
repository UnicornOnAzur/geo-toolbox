"""
author: UnicornOnAzur

This module provides a custom GeoDataFrame class that extends GeoPandas'
GeoDataFrame to include additional methods as well as function for
transforming coordinate reference systems (CRS) using different strategies.
"""
# Standard library
import typing
# Third party
import geopandas as gpd
# Constant
DEFAULT_CRS: str = "EPSG:4087"


class MyGeoDataFrame(gpd.GeoDataFrame):
    """
    Custom GeoDataFrame class that extends GeoPandas' GeoDataFrame
    to include additional CRS transformation methods.
    """
    def __init__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any
            ) -> None:
        super().__init__(*args, **kwargs)

    def always_to_crs(
        self,
        crs: typing.Union[int, str],
        method: str,
        inplace: bool = True,
            ) -> typing.Optional[gpd.GeoDataFrame]:
        """
        Transforms the GeoDataFrame to a specified coordinate reference system
        (CRS).

        Parameters:
            crs : The target CRS.
            method : The method to use for transformation ('lbyl' or 'eafp').
            inplace : If True, modifies the GeoDataFrame in place.

        Returns:
            The transformed GeoDataFrame if inplace is False.
        """
        match method:
            case "lbyl":
                return self._to_crs_lbyl(crs, inplace)
            case "eafp":
                return self._to_crs_eafp(crs, inplace)
            case _:
                raise ValueError("Method must be either 'lbyl' or 'eafp'.")

    def _to_crs_lbyl(
        self,
        crs: typing.Union[int, str],
        inplace: bool
            ) -> typing.Optional[gpd.GeoDataFrame]:
        """
        Transform CRS using the 'Look Before You Leap' method.

        Parameters:
            crs : The target CRS.
            inplace : If True, modifies the GeoDataFrame in place.

        Returns:
            The transformed GeoDataFrame if inplace is False.
        """
        if self.crs is None:
            self.set_crs(DEFAULT_CRS, inplace=True)
        return self.to_crs(crs, inplace=inplace)

    def _to_crs_eafp(
        self,
        crs: typing.Union[int, str],
        inplace: bool
            ) -> typing.Optional[gpd.GeoDataFrame]:
        try:
            return self.to_crs(crs, inplace=inplace)
        except ValueError:
            self.set_crs(DEFAULT_CRS, inplace=True)
            return self.to_crs(crs, inplace=inplace)


if __name__ == "__main__":
    pass
