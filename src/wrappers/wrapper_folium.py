# Standard library
import io
# Third party
import folium
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


if __name__ == "__main__":
    pass
