from pathlib import Path
from typing import Tuple

from django.db.models.fields.files import ImageFieldFile
from PIL import Image

from app.static_settings import MEDIA_URL


def create_dummy_png_image(
    image_name: str, IMAGE_SIZE: Tuple[int, int] = (300, 300)
) -> None:
    """
    Create dummy_media_dir if not already present and dummy image
    """
    Path(MEDIA_URL).mkdir(parents=True, exist_ok=True)
    Image.new("RGB", IMAGE_SIZE, (255, 255, 255)).save(
        f"{MEDIA_URL}/{image_name}", "png"
    )


def create_dummy_file(filename: str) -> None:
    """
    Create dummy_media_dir if not already present and dummy image
    """
    Path(MEDIA_URL).mkdir(parents=True, exist_ok=True)
    media_filepath = Path(MEDIA_URL) / filename
    with media_filepath.open("w", encoding="utf-8") as f:
        f.write("dummy content")


def check_image_attributes(
    image: ImageFieldFile, size_check: Tuple[int, int], ext_check: str
):
    assert Image.open(image).size == size_check
    assert Path(image.name).suffix == ext_check
