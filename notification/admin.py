from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .models import Notification
from django import forms


class SendNotificationForm(forms.Form):
    message = forms.CharField(label="Notification Message", max_length=255)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["message", "created_at"]
    add_form_template = "admin/notification/add_form.html"

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            form = SendNotificationForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data["message"]
                Notification.objects.create(message=message)
        else:
            form = SendNotificationForm()

        return super().add_view(request, form_url, extra_context={"form": form})
