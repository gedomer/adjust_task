from django.db import models
from django.utils.translation import gettext_lazy as _


class PlatformType:
    ANDROID = 'android'
    IOS = 'ios'

    AS_CHOICES = (
        (ANDROID, _('Android')),
        (IOS, _('IOS')),
    )


class Metric(models.Model):
    date = models.DateField()
    channel = models.CharField(max_length=100)
    country = models.CharField(max_length=3)
    os = models.CharField(max_length=20, choices=PlatformType.AS_CHOICES)
    impressions = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()
    installs = models.PositiveIntegerField()
    spend = models.FloatField()
    revenue = models.FloatField()

    class Meta:
        verbose_name = _('Data log')
        verbose_name_plural = _('Data logs')

    @property
    def cpi(self):
        if self.installs:
            return self.spend / self.installs
