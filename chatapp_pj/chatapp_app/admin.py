from django.contrib import admin

from .models import Chat, User

admin.site.register(User)
admin.site.register(Chat)