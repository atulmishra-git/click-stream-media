from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'extra/index.html'


class LoginView(TemplateView):
    template_name = 'extra/login.html'
