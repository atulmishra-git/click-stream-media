from django.views.generic import TemplateView, ListView, View
from src.models import Plans, CmsPage
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = 'extra/index.html'


class LoginView(TemplateView):
    template_name = 'extra/login.html'


class PlansView(ListView):
    template_name = 'extra/plans.html'
    model = Plans


class PrivacyView(View):
    template_name = 'extra/privacy.html'

    def get(self, request, *args, **kwargs):
        cms = CmsPage.objects.get(page_name='privacy')
        return render(request, self.template_name, {'obj': cms})


class TermsOfUseView(View):
    template_name = 'extra/terms_of_use.html'

    def get(self, request, *args, **kwargs):
        cms = CmsPage.objects.get(page_name='terms')
        return render(request, self.template_name, {'obj': cms})


class AboutView(View):
    template_name = 'extra/about.html'

    def get(self, request, *args, **kwargs):
        cms = CmsPage.objects.get(page_name='about')
        return render(request, self.template_name, {'obj': cms})
