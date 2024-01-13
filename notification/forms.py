from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Title",
            "description": "Description",
        }
        help_texts = {
            "title": "Enter the title of the notification",
            "description": "Enter the description of the notification",
        }
