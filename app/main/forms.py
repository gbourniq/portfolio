# sendemail/forms.py
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(
        widget=forms.Textarea(), required=True, max_length=2048,
    )
