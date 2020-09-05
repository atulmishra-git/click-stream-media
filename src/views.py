from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
import base64
from src.models import TrackingImage, UnsubscribeEmail, User

# Create your views here.


def email_open(request, user, email, uuid, subject, action, rand, campaign, rowIdx):
    user = User.objects.get(email=user)
    campaign_obj = Campaign.objects.get(campaign_uid=campaign)
    tracking_image = TrackingImage.objects.create(user=user, email=email, uuid=uuid, subject=subject, action=action, campaign=campaign_obj, rowIdx=rowIdx)
    tracking_image.save()
    return HttpResponse(base64.b64decode(b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"), content_type='image/gif')


def unsubscribe_email(request, campaign, user):
    context = {'message': ''}
    if request.method == 'POST':
        obj = UnsubscribeEmail.objects.create(email=request.POST['email'])
        obj.save()
        context['message'] = 'Unsubscribe successful'
    return render(request, "unsubscribe_email.html", context)


def start_campaign(request, campaign_uid, user):
    user = User.objects.get(email=user)
    campaign_obj = Campaign.objects.create(campaign_uid=campaign_uid, user=user)
    campaign_obj.save()
    return JsonResponse({'saved': True})


def get_read(request, campaign_uid, user):
    campaign_obj = Campaign.objects.get(campaign_uid=campaign_uid)
    user = User.objects.get(email=user)
    tracking_images = TrackingImage.objects.filter(campaign=campaign_obj, user=user)
    result = [(img.rowIdx, img.email) for img in tracking_images]
    return JsonResponse({'result': result})
