from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
import base64
from src.models import TrackingImage, UnsubscribeEmail, User, Campaign
from django.views.generic import View, CreateView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from src.forms import UnsubscribeForm

from django.conf import settings
import requests

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
        requests.get(settings.TACKER_WEBHOOK_URL + "sheet_id=" + kwargs['sheet_id'] + "rowIdx=" + kwargs['rowIdx'])
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
        return render(request)


class UnsubscribeView(CreateView):
    template_name = 'src/unsubscribe.html'
    form_class = UnsubscribeForm

    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(sheet_id=kwargs['campaign_id'])
        form = self.form_class(initial={'campaign': campaign.id})
        return render(request, self.template_name, {'form': form})
