from django.contrib import admin
from src.models import TrackingImage, UnsubscribeEmail, User

# Register your models here.


@admin.register(TrackingImage)
class TrackingImageAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False



@admin.register(UnsubscribeEmail)
class UnsubscribeEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_recorded', )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
