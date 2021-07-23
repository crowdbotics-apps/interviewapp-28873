from django.conf import settings
from django.db import models

APP_TYPES = (('Web', 'Web'), ('Mobile', 'Mobile'))
APP_FRAMEWORKS = (('Django', 'Django'), ('React Native', 'React Native'))


class App(models.Model):
    "Generated Model"
    name = models.CharField(
        max_length=50,
    )
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=20,
        choices=APP_TYPES,
    )
    framework = models.CharField(
        max_length=30,
        choices=APP_FRAMEWORKS,
    )
    domain_name = models.CharField(
        max_length=50,
        blank=True,
    )
    screenshot = models.URLField(
        blank=True,
        editable=False,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    user = models.IntegerField(
        editable=False,
        null=True,
    )
    subscription = models.IntegerField(
        blank=True,
        editable=False,
        null=True,
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
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )


class Subscription(models.Model):
    "Generated Model"
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    user = models.IntegerField(
        blank=True,
        editable=False,
        null=True,
    )
    plan = models.IntegerField()
    app = models.IntegerField()
