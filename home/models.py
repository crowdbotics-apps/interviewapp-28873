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
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    subscription = models.ManyToManyField(
        "home.Subscription",
        blank=True,
        related_name="app_subscription",
    )
    user = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="app_user",
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
    active = models.BooleanField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    user = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="subscription_user",
    )
    plan = models.ManyToManyField(
        "home.Plan",
        blank=True,
        related_name="subscription_plan",
    )
    app = models.ManyToManyField(
        "home.App",
        blank=True,
        related_name="subscription_app",
    )
