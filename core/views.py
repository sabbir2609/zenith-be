from django.views.generic import TemplateView


class Homepage(TemplateView):
    template_name = "home/page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Homepage"
        return context
