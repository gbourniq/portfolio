import shutil
from pathlib import Path
from unittest.mock import Mock

import pytest
from django.db.models.fields.files import ImageFieldFile
from PIL import UnidentifiedImageError

from app.static_settings import MEDIA_URL
from app.tests.mocks import MockCategory
from app.tests.utils import (
    check_image_attributes,
    create_dummy_file,
    create_dummy_png_image,
)
from main.models import CROP_SIZE


@pytest.mark.django_db(transaction=True)
class TestCategory:
    def test_create_category(self, mock_default_category):
        """
        Test category created with the expected attributes
        """

        _id = MockCategory.DEFAULT_ID

        attr_mapping = {
            mock_default_category.category_name: f"{MockCategory.DEFAULT_CATEGORY_NAME}{_id}",
            mock_default_category.summary: f"{MockCategory.DEFAULT_SUMMARY}{_id}",
            mock_default_category.image: f"{MockCategory.DEFAULT_IMAGE_NAME}{_id}.{MockCategory.DEFAULT_IMAGE_EXTENSION}",
            mock_default_category.category_slug: f"{MockCategory.DEFAULT_CATEGORY_SLUG}{_id}",
        }

        assert all(
            cat_attr == dummy_var
            for cat_attr, dummy_var in attr_mapping.items()
        )

    def test_category_str_cast(self, mock_default_category):
        """
        Test category created with the expected attributes
        """
        assert str(mock_default_category) == mock_default_category.category_name

    def test_category_json_cast(self, mock_default_category):
        """
        Test category created with the expected attributes
        """
        expected_dict = {
            "category_name": mock_default_category.category_name,
            "summary": mock_default_category.summary,
            "image": mock_default_category.image,
            "category_slug": mock_default_category.category_slug,
        }
        assert mock_default_category.json() == expected_dict

    def test_attr_types(self, client, mock_default_category):
        """
        Test category created with the expected attributes types
        """

        type_mapping = {
            mock_default_category.category_name: str,
            mock_default_category.summary: str,
            mock_default_category.image: ImageFieldFile,
            mock_default_category.category_slug: str,
        }

        assert all(
            isinstance(attr, attr_type)
            for attr, attr_type in type_mapping.items()
        )

    def test_image_resize_called(self, monkeypatch, mock_default_category):
        """
        Ensures the resizeImage function is called when saving category
        """
        mock_resize_image = Mock(return_value=mock_default_category.image)
        monkeypatch.setattr("main.models.resizeImage", mock_resize_image)

        mock_default_category.save()

        mock_resize_image.assert_called_once_with(mock_default_category.image)

    @pytest.mark.parametrize(
        "INITIAL_SIZE, FILE_EXTENTION",
        [
            ((800, 1280), "png"),
            ((2000, 200), "png"),
            ((200, 2000), "png"),
            ((100, 100), "png"),
            ((800, 1280), "jpeg"),
            ((2000, 200), "jpeg"),
            ((200, 2000), "jpeg"),
            ((100, 100), "jpeg"),
            ((800, 1280), "bmp"),
            ((2000, 200), "bmp"),
            ((200, 2000), "bmp"),
            ((500, 500), "bmp"),
            ((800, 1280), "tiff"),
            ((500, 500), "tiff"),
        ],
    )
    def test_image_resize_success(
        self, mock_default_category, INITIAL_SIZE, FILE_EXTENTION
    ):
        """
        Ensures the resizeImage function returns the expected image
        when saving a Category object
        """

        mock_default_category.image = f"dummy_image_base_name.{FILE_EXTENTION}"
        create_dummy_png_image(
            mock_default_category.image.name, IMAGE_SIZE=INITIAL_SIZE
        )

        check_image_attributes(
            mock_default_category.image,
            size_check=INITIAL_SIZE,
            ext_check=f".{FILE_EXTENTION}",
        )

        mock_default_category.save()

        check_image_attributes(
            mock_default_category.image, size_check=CROP_SIZE, ext_check=".jpg"
        )

        shutil.rmtree(Path(MEDIA_URL))

    @pytest.mark.parametrize(
        "FILE_EXTENTION, EXCEPTION",
        [
            ("oops", UnidentifiedImageError),
            ("pdf", UnidentifiedImageError),
            ("txt", UnidentifiedImageError),
            ("docx", UnidentifiedImageError),
            ("xls", UnidentifiedImageError),
        ],
    )
    def test_image_resize_failed(
        self, mock_default_category, FILE_EXTENTION, EXCEPTION
    ):
        """
        Simulate what happens when user upload an invalid file format
        """

        mock_default_category.image = f"dummy_image_base_name.{FILE_EXTENTION}"
        create_dummy_file(mock_default_category.image.name)

        with pytest.raises(EXCEPTION):
            mock_default_category.save()

        shutil.rmtree(Path(MEDIA_URL))
