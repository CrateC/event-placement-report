from django.db import models
from django_mysql.models import Model


class Platform(models.Model):

    CATEGORY_NAMES = (
            ('PL', 'Place'),
            ('TS', 'Ticket Seller'),
            ('FB', 'Facebook Event'),
            ('MP', 'Media Partner'),
    )

    name = models.CharField(max_length=120, null=True, blank=True)
    short_name = models.CharField(max_length=2, null=True, blank=True)
    link = models.CharField(max_length=120, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_NAMES)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return '{} | {}'.format(self.short_name, self.name)

    class Meta:
        db_table = 'events_platforms'
        unique_together = ('name', 'category',)
        verbose_name = 'events_platform'
        verbose_name_plural = 'events_platforms'


class Event(Model):
    platform = models.ForeignKey(Platform, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    link = models.CharField(max_length=180, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    # date = models.CharField(max_length=25, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events_events'
        unique_together = ('platform', 'name', 'link', 'date',)
        verbose_name = 'event'
        verbose_name_plural = 'events'
        # unique_together = ("platform", "name", "link", "date")

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    @property
    def date_time_formatted(self):
        return self.date.strftime('%Y-%m-%d %H:%M')



class EventHistory(models.Model):
    platform = models.ForeignKey(Platform, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    link = models.CharField(max_length=180, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events_events_history'
        # unique_together = ("platform", "name", "link", "date")

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name
