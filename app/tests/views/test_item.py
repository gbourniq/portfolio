import pytest
from django.db.models.query import QuerySet
from django.urls import reverse

from main.models import Category, Item


@pytest.mark.django_db(transaction=True)
class TestViewItems:
    def test_view_items_no_data(self, client):
        """
        Test that 404 is handled when no item exist
        """

        response = client.get(
            reverse(
                "viewItems",
                kwargs={"category_slug": "sent-your-non-existent-cat"},
            )
        )
        assert "main/go_back_home.html" in (t.name for t in response.templates)
        assert response.status_code == 200
        assert response.context["code_handled"] == 404

    def test_view_items_valid_url(self, client, load_default_item):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse("viewItems", kwargs={"category_slug": "cat-slug-1"})
        )

        assert response.url == "/items/cat-slug-1/item-slug-1-1/"
        assert response.status_code == 302
        assert len(response.templates) == 0

    def test_view_items_invalid_url(self, client, load_default_item):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse("viewItems", kwargs={"category_slug": "unknown-cat-slug"})
        )

        assert response.status_code == 200
        assert response.context["code_handled"] == 404
        assert "main/go_back_home.html" in (t.name for t in response.templates)


@pytest.mark.django_db(transaction=True)
class TestViewItem:
    def test_view_item_no_data(self, client):
        """
        Test that 404 is handled when no item exist
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": "cat-slug-1",
                    "item_slug": "item-slug-1-1",
                },
            )
        )

        assert "main/go_back_home.html" in (t.name for t in response.templates)
        assert response.status_code == 200
        assert response.context["code_handled"] == 404

    @pytest.mark.parametrize(
        "category_slug, item_slug", [("cat-slug-1", "item-slug-1-1"),],
    )
    def test_view_item_valid_url_single_item(
        self, client, category_slug, item_slug, load_default_item
    ):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": category_slug,
                    "item_slug": item_slug,
                },
            )
        )

        assert (
            response.request["PATH_INFO"]
            == f"/items/{category_slug}/{item_slug}/"
        )
        assert response.status_code == 200
        assert "main/items.html" in (t.name for t in response.templates)
        assert isinstance(response.context["item"], Item)
        assert isinstance(response.context["sidebar"], QuerySet)
        assert isinstance(response.context["this_item_idx"], int)
        assert isinstance(response.context["category_slug"], str)
        assert isinstance(response.context["category_name"], Category)

    @pytest.mark.parametrize(
        "category_slug, item_slug",
        [
            ("invalid-slug", "invalid-slug"),
            ("cat-slug-1", "item-slug-1-2"),
            ("cat-slug-2", "item-slug-1-1"),
        ],
    )
    def test_view_item_invalid_url_single_item(
        self, client, category_slug, item_slug, load_default_item
    ):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": category_slug,
                    "item_slug": item_slug,
                },
            )
        )

        assert response.status_code == 200
        assert response.context["code_handled"] == 404
        assert "main/go_back_home.html" in (t.name for t in response.templates)

    @pytest.mark.parametrize(
        "category_slug, item_slug",
        [
            # ("cat-slug-1", "item-slug-1-1"),
            ("cat-slug-1", "item-slug-1-2"),
            ("cat-slug-1", "item-slug-1-3"),
        ],
    )
    def test_view_item_valid_url_multiple_items(
        self, client, category_slug, item_slug, load_default_items
    ):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": category_slug,
                    "item_slug": item_slug,
                },
            )
        )

        assert (
            response.request["PATH_INFO"]
            == f"/items/{category_slug}/{item_slug}/"
        )
        assert response.status_code == 200
        assert "main/items.html" in (t.name for t in response.templates)
        assert isinstance(response.context["item"], Item)
        assert isinstance(response.context["sidebar"], QuerySet)
        assert isinstance(response.context["this_item_idx"], int)
        assert isinstance(response.context["category_slug"], str)
        assert isinstance(response.context["category_name"], Category)

    @pytest.mark.parametrize(
        "category_slug, item_slug",
        [
            ("invalid-slug", "invalid-slug"),
            ("cat-slug-1", "item-slug-1-9"),
            ("cat-slug-2", "item-slug-2-1"),
            ("cat-slug-3", "item-slug-3-1"),
            ("cat-slug-9", "item-slug-1-1"),
        ],
    )
    def test_view_item_invalid_url_multiple_items(
        self, client, category_slug, item_slug, load_default_items
    ):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": category_slug,
                    "item_slug": item_slug,
                },
            )
        )

        assert response.status_code == 200
        assert response.context["code_handled"] == 404
        assert "main/go_back_home.html" in (t.name for t in response.templates)

    @pytest.mark.parametrize(
        "category_slug, item_slug",
        [
            ("cat-slug-1", "item-slug-1-4"),
            ("cat-slug-2", "item-slug-2-3"),
            ("cat-slug-3", "item-slug-3-1"),
            ("cat-slug-4", "item-slug-4-5"),
            ("cat-slug-5", "item-slug-5-2"),
        ],
    )
    def test_view_item_valid_url_multiple_categories(
        self,
        client,
        category_slug,
        item_slug,
        load_default_items_and_categories,
    ):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": category_slug,
                    "item_slug": item_slug,
                },
            )
        )

        assert (
            response.request["PATH_INFO"]
            == f"/items/{category_slug}/{item_slug}/"
        )
        assert response.status_code == 200
        assert "main/items.html" in (t.name for t in response.templates)
        assert isinstance(response.context["item"], Item)
        assert isinstance(response.context["sidebar"], QuerySet)
        assert isinstance(response.context["this_item_idx"], int)
        assert isinstance(response.context["category_slug"], str)
        assert isinstance(response.context["category_name"], Category)

    @pytest.mark.parametrize(
        "category_slug, item_slug",
        [
            ("invalid-slug", "invalid-slug"),
            ("cat-slug-1", "item-slug-1-9"),
            ("cat-slug-2", "item-slug-2-9"),
            ("cat-slug-7", "item-slug-7-1"),
            ("cat-slug-8", "item-slug-8-1"),
        ],
    )
    def test_view_item_invalid_url_multiple_categories(
        self,
        client,
        category_slug,
        item_slug,
        load_default_items_and_categories,
    ):
        """
        Test the view Items page when database contains item objects
        """

        response = client.get(
            reverse(
                "viewItem",
                kwargs={
                    "category_slug": category_slug,
                    "item_slug": item_slug,
                },
            )
        )

        assert response.status_code == 200
        assert response.context["code_handled"] == 404
        assert "main/go_back_home.html" in (t.name for t in response.templates)
