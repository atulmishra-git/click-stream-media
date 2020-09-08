from django.urls import path
from .views.src import EmailTackerOpen, UnsubscribeView, CampaignView, MyUnsubscribeView, UserPlansView, QuotaConsumedView, UserCreateView

from .views.extra import IndexView, LoginView


urlpatterns = [
    path('image_pix/<str:user>/<str:email>/<str:action>/<str:rand>/<str:sheet_id>/<str:rowIdx>', EmailTackerOpen.as_view(), name='image_pix'),
    path('unsubscribe/<str:campaign_id>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('campaign/', CampaignView.as_view(), name='campaign'),
    path('unsubscription/<str:sheet_id>/', MyUnsubscribeView.as_view(), name='my_unsubscribe'),
    path('userplan/<str:user>', UserPlansView.as_view(), name='user_plan'),
    path('quota_consumed/', QuotaConsumedView.as_view(), name='quota_consumed'),
    path('usercreate/', UserCreateView.as_view(), name='usercreate')
]


urlpatterns += [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login')
]
