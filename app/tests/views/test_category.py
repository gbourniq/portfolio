import pytest
from django.db.models.query import QuerySet
from django.urls import reverse

from main.models import Category


@pytest.mark.django_db(transaction=True)
class TestViewCategory:
    def test_404_no_category_in_db(self, client):
        """
        Test that 404 is handled when no category exist
        """

        response = client.get(reverse("viewCategories"))

        assert "main/go_back_home.html" in (t.name for t in response.templates)
        assert response.status_code == 200
        assert response.context["code_handled"] == 404

    def test_view_category(self, client, load_default_category):
        """
        Test the view Category page when database contains one category object
        """

        response = client.get(reverse("viewCategories"))

        assert "main/categories.html" in (t.name for t in response.templates)
        assert response.status_code == 200
        assert isinstance(response.context["categories"], QuerySet)

    def test_view_categories(self, client, load_default_categories):
        """
        Test the view Category page when database contains one category object
        """

        assert Category.objects.all().count() == len(load_default_categories)

        # time.sleep(5)
        # response = client.get(reverse("viewCategories"))

        # assert "main/categories.html" in (t.name for t in response.templates)
        # assert response.status_code == 200
        # assert isinstance(response.context["categories"], QuerySet)
        # assert len(response.context["categories"]) == len(mock_categories)
