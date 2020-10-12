from django.contrib import admin
from src.models import TrackingImage, UnsubscribeEmail, User, Campaign, Plans, PurchasedPlans, QuotaConsumed, CmsPage

# Register your models here.


@admin.register(UnsubscribeEmail)
class UnsubscribeEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', )
    list_filter = ('campaign__user', )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_admin', )


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'sheet_id', 'email_open', 'date', )
    list_filter = ('user__user_plan', 'user__user_plan__plan', 'date')


@admin.register(Plans)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'type', 'quota', )
    list_filter = ('purchased_plan', )


@admin.register(PurchasedPlans)
class PurchasedPlansAdmin(admin.ModelAdmin):
    list_display = ('plan', 'user', 'date')
    list_filter = ('plan', 'user', 'date')


@admin.register(QuotaConsumed)
class QuotaConsumedAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date')
    list_filter = ('user__user_plan__plan', 'user__user_plan')


@admin.register(CmsPage)
class CmsPageAdmin(admin.ModelAdmin):
    pass
