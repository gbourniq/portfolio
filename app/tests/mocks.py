from typing import List

from main.models import Category, Item


class MockCategory:
    DEFAULT_ID = 1
    DEFAULT_CATEGORY_NAME = "Category "
    DEFAULT_SUMMARY = "summary for category "
    DEFAULT_IMAGE_NAME = "img-url"
    DEFAULT_IMAGE_EXTENSION = "png"
    DEFAULT_CATEGORY_SLUG = "cat-slug-"

    @staticmethod
    def default_category(_id: int = DEFAULT_ID, **kwargs) -> Category:

        category_data = {
            "id": _id,
            "category_name": kwargs.get(
                "category_name", f"{MockCategory.DEFAULT_CATEGORY_NAME}{_id}"
            ),
            "summary": kwargs.get(
                "summary", f"{MockCategory.DEFAULT_SUMMARY}{_id}"
            ),
            "image": kwargs.get(
                "image",
                f"{MockCategory.DEFAULT_IMAGE_NAME}{_id}.{MockCategory.DEFAULT_IMAGE_EXTENSION}",
            ),
            "category_slug": kwargs.get(
                "category_slug", f"{MockCategory.DEFAULT_CATEGORY_SLUG}{_id}"
            ),
        }

        dummy_category = Category.create(category_data)

        # create_dummy_png_image(dummy_category.image.name)

        return dummy_category

    @staticmethod
    def default_categories(categories_count: int, **kwargs) -> List[Category]:
        default_categories = []
        for idx in range(categories_count):
            default_categories.append(
                MockCategory.default_category(
                    MockCategory.DEFAULT_ID + idx, **kwargs
                ),
            )
        return default_categories


class MockItem:
    DEFAULT_ID = 1
    DEFAULT_ITEM_NAME = "Item "
    DEFAULT_SUMMARY = "summary for item "
    DEFAULT_CONTENT = "content for item "
    DEFAULT_DATE = "2020-05-22 19:49:50+00:00"
    DEFAULT_ITEM_SLUG = "item-slug-"
    DEFAULT_CATEGORY = MockCategory.DEFAULT_ID

    @staticmethod
    def default_item(
        parent_category: Category, item_id: int = DEFAULT_ID, **kwargs
    ) -> Item:

        if parent_category.category_name not in [
            cat.category_name for cat in Category.objects.all()
        ]:
            print(
                f"""Parent category {parent_category} does not exist in the databse.\n
                  Please creating it prior to running this function."""
            )

        _id = f"{parent_category.id}-{item_id}"

        item_data = {
            "item_name": kwargs.get(
                "item_name", f"{MockItem.DEFAULT_ITEM_NAME}{_id}"
            ),
            "summary": kwargs.get(
                "summary", f"{MockItem.DEFAULT_SUMMARY}{_id}"
            ),
            "content": kwargs.get(
                "content", f"{MockItem.DEFAULT_CONTENT}{_id}"
            ),
            "date_published": kwargs.get(
                "date_published", f"{MockItem.DEFAULT_DATE}",
            ),
            "item_slug": kwargs.get(
                "item_slug", f"{MockItem.DEFAULT_ITEM_SLUG}{_id}"
            ),
            "category_name": parent_category,
        }

        dummy_item = Item.create(item_data)

        return dummy_item

    @staticmethod
    def default_items(
        items_count: int, parent_category: Category, **kwargs
    ) -> List[Item]:
        """
        Creates list of default items, with Category ID = 1 as parent
        """
        default_items = []
        for idx in range(items_count):
            default_items.append(
                MockItem.default_item(
                    parent_category, MockItem.DEFAULT_ID + idx, **kwargs
                ),
            )
        return default_items
