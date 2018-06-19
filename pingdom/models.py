from django.contrib.auth.models import User
from django.db import models


class Site(models.Model):
    sitename = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    date = models.DateTimeField('date_published', null=True)
    testsuc = models.IntegerField(default=0)
    mailsent = models.IntegerField(default=0)
    testfail = models.IntegerField(default=0)
    auto_test_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return self.sitename

    class Meta:
        verbose_name_plural = "Sitename"


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    hassites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User"

class SiteLog(models.Model):
    site = models.ForeignKey(Site)
    month = models.CharField('month', max_length=10, null=True)        
