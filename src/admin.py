from django.contrib import admin
from src.models import TrackingImage, UnsubscribeEmail, User, Campaign, Plans, PurchasedPlans

# Register your models here.


@admin.register(UnsubscribeEmail)
class UnsubscribeEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date', )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'sheet_id', 'email_open', 'date', )


@admin.register(Plans)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'type', 'quota', )


@admin.register(PurchasedPlans)
class PurchasedPlansAdmin(admin.ModelAdmin):
    pass
