from django.urls import path
from .views.src import EmailTackerOpen, UnsubscribeView, CampaignView

from .views.extra import IndexView, LoginView


urlpatterns = [
    path('image_pix/<str:user>/<str:email>/<str:action>/<str:rand>/<str:sheet_id>/<str:rowIdx>', EmailTackerOpen.as_view(), name='image_pix'),
    path('unsubscribe/<str:campaign_id>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('campaign/', CampaignView.as_view(), name='campaign'),
]


urlpatterns += [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login')
]
