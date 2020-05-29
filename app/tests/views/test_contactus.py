from unittest.mock import Mock

import pytest
from django.urls import reverse

from app.portfolio import settings
from main.forms import ContactForm


@pytest.mark.django_db(transaction=True)
class TestViewCategory:
    @pytest.mark.integration
    def test_view_contact_us_page(self, client):
        """
        Test the view Category us page is rendered with the Contact Form
        """

        response = client.get(reverse("viewContactUs"))

        assert "main/contact_us.html" in (t.name for t in response.templates)
        assert response.status_code == 200
        assert isinstance(response.context["form"], ContactForm)

    @pytest.mark.integration
    def test_post_valid_form(
        self, monkeypatch, client, mock_contact_form: ContactForm
    ):
        """
        Test the `Go Back Home` page is rendered when user submit valid form
        """

        create_contact_form = Mock(return_value=mock_contact_form)
        monkeypatch.setattr("main.views.send_email", create_contact_form)

        response = client.post(reverse("viewContactUs"), data={})

        create_contact_form.assert_called_once_with(
            response.context["request"],
            [settings.EMAIL_HOST_USER],
            settings.EMAIL_HOST_USER,
        )
        assert "main/go_back_home.html" in (t.name for t in response.templates)
        assert response.status_code == 200

    @pytest.mark.integration
    def test_post_empty_form(self, monkeypatch, client):
        """
        Ensure that, when a user submits an empty form:
        - Redirect to the current page
        - Email function not called
        """

        send_email = Mock()
        monkeypatch.setattr("main.services.send_email_function", send_email)

        contact_us_url = reverse("viewContactUs")
        response = client.post(
            contact_us_url, data={}, HTTP_REFERER=contact_us_url
        )

        send_email.assert_not_called()

        assert len(response.templates) == 0
        assert response.status_code == 302

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "name, contact_email, subject, message",
        [
            ("", "valid@email.com", "valid subject", "valid message"),
            ("valid name", "invalid email", "valid subject", "valid message"),
            ("valid name", "", "valid subject", "valid message"),
            ("valid name", "valid@email.com", "", "valid message"),
            ("valid name", "valid@email.com", "valid subject", ""),
        ],
    )
    def test_post_invalid_form(
        self,
        monkeypatch,
        client,
        name: str,
        contact_email: str,
        subject: str,
        message: str,
    ):
        """
        When invalid forms are submitted, ensures we have a page rediction
        (return code 302) and that the email function is not called,
        """

        send_email = Mock()
        monkeypatch.setattr("main.services.send_email_function", send_email)

        invalid_form = ContactForm()
        invalid_form.name = name
        invalid_form.contact_email = contact_email
        invalid_form.subject = subject
        invalid_form.message = message

        contact_us_url = reverse("viewContactUs")
        response = client.post(
            contact_us_url,
            data=invalid_form.json(),
            HTTP_REFERER=contact_us_url,
        )

        send_email.assert_not_called()

        assert len(response.templates) == 0
        assert response.status_code == 302

    @pytest.mark.integration
    def test_send_email(
        self, monkeypatch, client, mock_contact_form: ContactForm
    ):
        """
        Test the send_mail_function is called when a valid form is submitted
        """

        send_email = Mock()
        monkeypatch.setattr("main.services.send_email_function", send_email)

        response = client.post(
            reverse("viewContactUs"), data=mock_contact_form.json()
        )

        send_email.assert_called()

        assert "main/go_back_home.html" in (t.name for t in response.templates)
        assert response.status_code == 200
