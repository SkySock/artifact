from django.contrib import admin
from . import models


@admin.register(models.UserSubscriptionType)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'description', 'image', 'price', )
    list_display_links = ('id', 'name', 'owner', )
