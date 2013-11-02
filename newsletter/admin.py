from django.contrib import admin
from newsletter.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
        fields = ('email',)
        list_display = ('email',)
        search_fields = ('email',)

admin.site.register(Subscription, SubscriptionAdmin)
