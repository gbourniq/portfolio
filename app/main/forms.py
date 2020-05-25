# sendemail/forms.py
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        widget=forms.Textarea(), required=True, max_length=2048,
    )

    def json(self):
        """
        Returns class attributes as a dictionary.
        """
        return {
            "name": self.name,
            "contact_email": self.contact_email,
            "subject": self.subject,
            "message": self.message,
        }
