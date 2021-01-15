from django.contrib import admin
from .models import ShortenUrl, RedirectLink, UserClickStat

admin.site.register(ShortenUrl)
admin.site.register(RedirectLink)
admin.site.register(UserClickStat)
