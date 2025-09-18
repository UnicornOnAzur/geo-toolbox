# Third party
import cartopy
import matplotlib.pyplot as plt
# Constants for colors and dimensions
WATER_COLOR: str = "lightskyblue"
EARTH_COLOR: str = "tan"
BORDER_COLOR: str = "darkgrey"
HEIGHT: int = 5
WIDTH: int = 14


def equal_earth_cartopy() -> None:
    """
    Generates a series of maps using Cartopy to compare different projections.

    Parameters:
        None

    Returns:
        None
    """
    fig: plt.Figure = plt.figure(figsize=(WIDTH, HEIGHT))
    for rect, crs in zip((121, 122),
                         (cartopy.crs.Mercator(), cartopy.crs.EqualEarth())):
        ax: cartopy.mpl.geoaxes.GeoAxes = fig.add_subplot(rect, projection=crs)
        ax.add_feature(cartopy.feature.LAND, color=EARTH_COLOR)
        ax.add_feature(cartopy.feature.BORDERS, color=BORDER_COLOR)
        ax.coastlines(color=BORDER_COLOR)
        ax.set_facecolor(WATER_COLOR)
        ax.set_title(crs.proj4_params["proj"])
    fig.savefig("output/equal_earth_cartopy.png")