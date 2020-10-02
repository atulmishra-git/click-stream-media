from django.urls import path
from .views.src import EmailTackerOpen, UnsubscribeView, CampaignView, MyUnsubscribeView, UserPlansView, QuotaConsumedView, UserCreateView

from .views.extra import IndexView, PlansView, PrivacyView, TermsOfUseView, AboutView, UserCampaignView, \
MyUnsubscribeListView, MyUnsubscribeDeleteView, ContactView, PurchasePlanView, PaymentSuccessView, PaymentFailureView


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
    path('plans/', PlansView.as_view(), name='plans'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('terms/', TermsOfUseView.as_view(), name='terms'),
    path('about/', AboutView.as_view(), name='about'),
    path('campaigns/',UserCampaignView.as_view(), name='user_campaign'),
    path('unsubscriptions/',MyUnsubscribeListView.as_view(), name='my_unsubscribe_list'),
    path('unsubscriptions/<int:pk>/delete', MyUnsubscribeDeleteView.as_view(), name='my_unsubscribe_delete'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('purchase_plan/<int:pk>/plan', PurchasePlanView.as_view(), name='purchase_plan'),
    path('payment_success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment_failure/', PaymentFailureView.as_view(), name='payment_failure')
]
