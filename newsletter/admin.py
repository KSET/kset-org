from django.contrib import admin

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
        fields = ('email',)
        list_display = ('email',)
        search_fields = ('email',)

admin.site.register(Subscription, SubscriptionAdmin)
