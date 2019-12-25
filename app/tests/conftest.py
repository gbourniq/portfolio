from unittest.mock import Mock
import pytest


# from main.models import Category, SubCategory, Article


@pytest.fixture
def category_instance():
    # return Category()
    return None


@pytest.fixture
def subcategory_instance():
    # return SubCategory()
    return None


@pytest.fixture
def article_instance():
    # return Article()
    return None


# from tests.mocks import (
#     MockDocumentClient,
#     MockDocumentTypeClient,
#     MockProjectClient,
#     MockQuestionClient,
#     MockTagClient,
#     MockUserClient,
# )


# @pytest.fixture
# def mock_timestamped_dir_attr(tmp_path, monkeypatch):
#     def func(instance, directory_name):
#         timestamped_dir = tmp_path / directory_name
#         timestamped_dir.mkdir()
#         monkeypatch.setattr(instance, "timestamped_dir", timestamped_dir)
#         return timestamped_dir

#     return func
