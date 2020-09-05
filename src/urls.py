from django.urls import path
from .views import email_open, unsubscribe_email, start_campaign, get_read

urlpatterns = [
    path('email_open/<str:user>/<str:email>/<str:uuid>/<str:subject>/<str:action>/<str:rand>/<str:campaign>/<str:rowIdx>', email_open, name='email_open'),
    path('unsubscribe/<str:campaign_uid>/<str:email>', unsubscribe_email, name='unsubscribe_email'),
    path('start_campaign/<str:campaign_uid>/<str:email>', start_campaign, name='start_campaign'),
    path('get_read/<str:campaign_uid>/<str:email>', get_read, name='get_read')
]
