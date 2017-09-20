from django.contrib import admin

# Register your models here.
from .models import Platform, Event, EventHistory

admin.site.register(Platform)


class EventsAdmin(admin.ModelAdmin):
    list_display = ('platform', 'name', 'language', 'date')


admin.site.register(Event, EventsAdmin)
admin.site.register(EventHistory, EventsAdmin)
