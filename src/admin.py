from django.contrib import admin
from src.models import TrackingImage, UnsubscribeEmail, User, Campaign

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
