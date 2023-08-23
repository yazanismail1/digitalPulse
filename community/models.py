from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    members = models.ManyToManyField('account.CustomUser', blank=True, through='Membership', related_name="communities")

class Membership(models.Model):
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="userMemberships")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="memberships")
    position = models.CharField(max_length=100)