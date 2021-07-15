from django.conf import settings
from django.db import models


class App(models.Model):
    "Generated Model"
    name = models.CharField(
        max_length=50,
    )
    description = models.TextField()
    type = models.CharField(
        max_length=20,
    )
    framework = models.CharField(
        max_length=30,
    )
    domain_name = models.CharField(
        max_length=50,
    )
    screenshot = models.URLField()
    subscription = models.IntegerField()
    user = models.IntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Plan(models.Model):
    "Generated Model"
    name = models.CharField(
        max_length=20,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=30,
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Subscription(models.Model):
    "Generated Model"
    user = models.IntegerField()
    plan = models.IntegerField()
    app = models.IntegerField()
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
