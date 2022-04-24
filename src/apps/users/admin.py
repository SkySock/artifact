from django.contrib import admin
from . import models


@admin.register(models.ArtifactUser)
class ArtifactUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    list_display_links = ('username', )


@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'link',)
