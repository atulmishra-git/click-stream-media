from django.views.generic import TemplateView, ListView, View, DeleteView, DetailView
from src.models import Plans, CmsPage, Campaign, UnsubscribeEmail, PurchasedPlans
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

import datetime
import hashlib
from random import randint

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'extra/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['plans'] = Plans.objects.all()
        return data


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


class UserCampaignView(ListView):
    template_name = 'extra/user_campaign.html'
    model = Campaign

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(user=self.request.user)
        return qs


class MyUnsubscribeListView(ListView):
    template_name = 'extra/my_unsubscribe_list.html'
    model = UnsubscribeEmail
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sheets'] = Campaign.objects.filter(user=self.request.user)
        return data

class MyUnsubscribeDeleteView(DeleteView):
    model = UnsubscribeEmail
    template_name = 'extra/unsubscribeemail_confirm_delete.html'
    success_url = reverse_lazy('my_unsubscribe_list')


class ContactView(TemplateView):
    template_name = 'extra/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        try:
            send_mail("{} contact".format(name), message, email, ['hello.mymailmerge@gmail.com'])
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect('/contact')

        messages.success(request, 'Thank you for contacting us.')
        return HttpResponseRedirect('/contact')


class PurchasePlanView(LoginRequiredMixin, DetailView):
    template_name = 'extra/purchase_plan.html'
    model = Plans

    def get_transaction_id(self):
        hash_object = hashlib.sha256(b'randint(0,20)')
        txnid = hash_object.hexdigest()[0:20]
        return txnid

    def get_hash_string(self):
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        posted= {
            'key': settings.PAYU_MERCHANT_KEY,
            'txnid': self.get_transaction_id(),
            'amount': f"{float(self.object.cost):.2f}",
            'productinfo': self.object,
            'firstname': self.request.user,
            'email': self.request.user.email,
            'udf1': self.object.pk
        }
        for seq in hashVarsSeq:
            try:
                hash_string += str(posted[seq])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += settings.PAYU_SALT
        return hash_string

    def generate_hash(self):
        hash_string = self.get_hash_string()
        hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return hash

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        hash_string = self.get_hash_string()
        hash = self.generate_hash()
        action = settings.PAYU_BASE_URL

        data['hash'] = hash
        data['hash_string'] = hash_string
        data['txnid'] = self.get_transaction_id()
        data['PAYU_MERCHANT_KEY'] = settings.PAYU_MERCHANT_KEY
        data['action'] = action
        data['furl'] = self.request.build_absolute_uri(reverse_lazy('payment_success'))
        data['surl'] = self.request.build_absolute_uri(reverse_lazy('payment_failure'))
        return data


@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(TemplateView):
    template_name = 'extra/payment_success.html'

    def post(self, *args, **kwargs):
        posted_hash = self.request.POST["hash"]
        plan_id = self.request.POST["udf1"]
        plan = Plans.objects.get(pk=int(plan_id))
        pp_obj = PurchasedPlans.objects.create(user=self.request.user, plan=plan)
        pp_obj.save()
        return render(self.request, self.template_name)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentFailureView(TemplateView):
    template_name = 'extra/payment_failure.html'

    def post(self, *args, **kwargs):
        return render(self.request, self.template_name)
