from django.shortcuts import render
from django.views.generic import TemplateView


class IoTPage(TemplateView):
    template_name = "iot/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "IoT Devices Websocket Test"
        return context
