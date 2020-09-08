from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
import base64
from src.models import TrackingImage, UnsubscribeEmail, User, Campaign, Plans, PurchasedPlans, QuotaConsumed
from django.views.generic import View, CreateView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from src.forms import UnsubscribeForm

from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class EmailTackerOpen(View):
    image = base64.b64decode(b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")

    def get(self, *args, **kwargs):
        response = HttpResponse(self.image)
        response['Content-Type'] = 'image/gif'

        user = User.objects.get(email=kwargs['user'])
        try:
            campaign = Campaign.objects.get(sheet_id=kwargs['sheet_id'])
        except Campaign.DoesNotExist:
            campaign = Campaign.objects.create(user=user, sheet_id=kwargs['sheet_id'])

        email = kwargs['email']
        action = kwargs['action']
        rowIdx = kwargs['rowIdx']

        tracker = TrackingImage.objects.create(user=user, email=email, action=action, campaign=campaign, rowIdx=rowIdx)
        tracker.save()
        return response

    def post(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(sheet_id=request.POST['sheet_id'])
        user = User.objects.get(email=request.POST['user'])
        action = request.POST['action']

        tracker = TrackingImage.objects.filter(user=user, action=action, campaign=campaign)
        result = [{img.rowIdx:img.email} for img in tracker]

        return JsonResponse({'result': result})


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class CampaignView(View):
    def post(self, request, *args, **kwargs):
        sheet_id = request.POST['sheet_id']
        user = User.objects.get(email=request.POST['user'])
        try:
            campaign= Campaign.objects.create(sheet_id=sheet_id, user=user)
            campaign.save()
            saved = True
        except Exception:
            saved = False
        return JsonResponse({'saved': saved})

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.GET['user'])
        campaign = Campaign.objects.filter(sheet_id=request.GET['sheet_id'], user=user).all()
        results = []
        for c in campaign:
            tracker = c.tracker
            rowIdx = tracker.all()
            un_rowIdx = []
            for r in rowIdx:
                if r.rowIdx not in un_rowIdx:
                    un_rowIdx.append(r.rowIdx)
            unsubscribed = c.unsubscribed.all()
            results.append({
                'email_open': tracker.count(),
                'un_rowIdx': un_rowIdx,
                'unsubscribed': [un.email for un in unsubscribed]
            })
        return JsonResponse({'results': results})


class UnsubscribeView(CreateView):
    template_name = 'src/unsubscribe.html'
    form_class = UnsubscribeForm

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'We have informed the sender of this email that you dont want to receive more emails from them.')
        return reverse_lazy('unsubscribe', kwargs={'campaign_id': self.kwargs['campaign_id']})


    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(sheet_id=kwargs['campaign_id'])
        form = self.form_class(initial={'campaign': campaign.id})
        return render(request, self.template_name, {'form': form})


class MyUnsubscribeView(CreateView):
    template_name = 'src/my-unsubscribe.html'
    form_class = UnsubscribeForm

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Email added succesfully.')
        return reverse_lazy('my_unsubscribe', kwargs={'sheet_id': self.kwargs['sheet_id']})

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(sheet_id=kwargs['sheet_id'])
        form = self.form_class(initial={'campaign': campaign.id})
        return render(request, self.template_name, {'form': form})


class UserPlansView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=self.kwargs['user'])
        try:
            pp = PurchasedPlans.objects.get(user=user)
            results = dict(name=pp.plan.name, quota=pp.plan.quota, id=pp.plan.pk)
            return JsonResponse({'results': results})
        except PurchasedPlans.DoesNotExist:
            plan = Plans.objects.get(type='Free')
            results = dict(name=plan.name, quota=plan.quota, id=plan.pk)
            return JsonResponse({'results': results})


@method_decorator(csrf_exempt, name='dispatch')
class QuotaConsumedView(View):
    def post(self, request, *args, **kwargs):
        _user = request.POST['user']
        used = request.POST['used']
        date = datetime.strptime(request.POST['date'], "%d/%m/%Y")

        user = User.objects.get(email=_user)

        qc = QuotaConsumed.objects.filter(user=user, date=date).first()
        if qc:
            qc.amount +=used
        else:
            QuotaConsumed.objects.create(user=user, amount=round(used), date=date)

        return JsonResponse({'results': {'used': used}})


    def get(self, request, *args, **kwargs):
        _user = request.GET['user']
        date = datetime.strptime(request.GET['date'], "%d/%m/%Y")

        user = User.objects.get(email=_user)
        qc = QuotaConsumed.objects.filter(user=user, date=date).first()
        if qc is not None:
            results = dict(amount=qc.amount)
        else:
            results = dict(amount=0)
        return JsonResponse({'results': results})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            email = request.POST['email']
            user = User.objects.create(email=email, password="user123")
            user.save()
            message = 'success'
        except Exception:
            message = 'Failed'
        return JsonResponse({'results': message})
