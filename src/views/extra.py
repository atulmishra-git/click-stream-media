from django.views.generic import TemplateView, ListView
from src.models import Plans


class IndexView(TemplateView):
    template_name = 'extra/index.html'


class LoginView(TemplateView):
    template_name = 'extra/login.html'


class PlansView(ListView):
    template_name = 'extra/plans.html'
    model = Plans
