# from unittest.mock import Mock
from typing import List, Union
from unittest.mock import Mock

import pytest

from app.tests.mocks import MockCategory, MockItem
from main.forms import ContactForm
from main.models import Category, Item


# Helpers functions
def existing_categories() -> Union[List[Category], None]:
    return [cat.category_name for cat in Category.objects.all()]


def existing_items() -> Union[List[Item], None]:
    return [itm.item_name for itm in Item.objects.all()]


def save_mock_category(monkeypatch, category: Category) -> None:
    mock_resize_image = Mock(return_value=category.image)
    monkeypatch.setattr("main.models.resizeImage", mock_resize_image)
    category.save()
    mock_resize_image.assert_called_once_with(category.image)


##########################
#
#   Category Fixtures
#
##########################
@pytest.fixture
def mock_default_category() -> Category:
    """Return a default category object (unsaved)"""
    return MockCategory.default_category()


@pytest.fixture
def load_default_category(mock_default_category: Category, monkeypatch) -> None:
    """Save a default category object, and return the object"""
    if mock_default_category.category_name not in existing_categories():
        save_mock_category(monkeypatch, mock_default_category)
    return mock_default_category


@pytest.fixture
def mock_default_categories() -> List[Category]:
    """Create, save, and return default category objects"""
    return MockCategory.default_categories(categories_count=5)


@pytest.fixture
def load_default_categories(
    mock_default_categories: List[Category], monkeypatch
) -> List[Category]:
    for mock_default_category in mock_default_categories:
        if mock_default_category.category_name not in existing_categories():
            save_mock_category(monkeypatch, mock_default_category)
    return mock_default_categories


##########################
#
#   Item Fixtures
#
##########################
@pytest.fixture
def mock_default_item(load_default_category) -> Item:
    """Return a default item object (unsaved)"""
    return MockItem.default_item(parent_category=load_default_category)


@pytest.fixture
def load_default_item(mock_default_item: Item) -> None:
    """Save a default item object, and the category it belongs to and return the object"""
    if mock_default_item.item_name not in existing_items():
        mock_default_item.save()
    return mock_default_item


@pytest.fixture
def mock_default_items(load_default_category) -> List[Item]:
    """Return a list of default item objects (unsaved)"""
    return MockItem.default_items(
        items_count=5, parent_category=load_default_category
    )


@pytest.fixture
def load_default_items(mock_default_items: List[Item]) -> List[Item]:
    [
        mock_default_item.save()
        for mock_default_item in mock_default_items
        if mock_default_item.item_name not in existing_items()
    ]
    return mock_default_items


@pytest.fixture
def load_default_items_and_categories(
    monkeypatch, categories_count=5, items_count=5
) -> List[Item]:
    created_categories = MockCategory.default_categories(categories_count)
    created_items = []
    for category in created_categories:
        save_mock_category(monkeypatch, category)
        items = MockItem.default_items(items_count, parent_category=category)
        [itm.save() for itm in items]
        created_items.append(items)
    return created_categories, created_items


##########################
#
#   Email Fixtures
#
##########################


@pytest.fixture
def mock_contact_form() -> ContactForm:
    mock_form = ContactForm()
    mock_form.name = "dummy name"
    mock_form.contact_email = "dummy@mail.com"
    mock_form.subject = "dummy subject"
    mock_form.message = "dummy content"
    return mock_form
