from django.shortcuts import render
from django.views.generic import TemplateView


class NotificationPage(TemplateView):
    template_name = "notification/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notification"
        return context
