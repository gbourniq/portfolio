# sendemail/forms.py
from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 200, 'cols': 40, 'style':'margin: 0px; height: 228px; width: 1008px;'}),
                              required=True,
                              max_length=2048)
    
    
#ß<textarea name="message" cols="40" rows="200" style="margin: 0px; height: 228px; width: 1008px;" maxlength="2048" required="" id="id_message"></textarea>
    
    
