import pytest
from django.urls import reverse


@pytest.mark.django_db(transaction=True)
class TestViewCategory:
    def test_view_homepage(self, client):
        """
        Test the view Category page when database contains one category object
        """

        response = client.get(reverse("viewHome"))

        assert "main/home.html" in (t.name for t in response.templates)
        assert response.status_code == 200
