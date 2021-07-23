from django.contrib.auth import get_user_model
from home.models import App, Plan, Subscription
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "email": {
                "required": True,
                "allow_blank": False,
            },
        }

    def _get_request(self):
        request = self.context.get("request")
        if (
                request
                and not isinstance(request, HttpRequest)
                and hasattr(request, "_request")
        ):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address.")
                )
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get("email"),
            name=validated_data.get("name"),
            username=generate_unique_username(
                [validated_data.get("name"), validated_data.get("email"), "user"]
            ),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""

    password_reset_form_class = ResetPasswordForm


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = "__all__"

    def create(self, validated_data):
        new_app = App.objects.create(**validated_data)

        # update user who created app
        user = self.context['request'].user
        new_app.user = user.id
        new_app.save()

        # assign to default free plan so create subscription
        # free_plan = Plan.objects.get(id=1)
        # subscription = Subscription.objects.create({
        #     'plan': free_plan.id,
        #     'active': True,
        #     'app': new_app.id
        # })
        # subscription.save()

        return new_app


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

    def create(self, validated_data):
        # check if app already has a subscription
        if Subscription.objects.filter(app=validated_data['app']).exists():
            raise serializers.ValidationError("Subscription already exists for this app.")

        new_subscription = Subscription.objects.create(**validated_data)

        # not sure which user to assign here
        # the one who owns the app or from the session which might be different
        # app_owner_id = App.objects.get(id=validated_data['app'])

        # update user who owns app assume he/she is in session
        user = self.context['request'].user
        new_subscription.user = user.id
        new_subscription.save()

        # update app subscriptions status
        app = App.objects.get(id=validated_data['app'])
        app.subscription = new_subscription.id
        app.save()

        return new_subscription

    def update(self, instance, validated_data):

        # check if app already has a subscription and is not an instance
        if Subscription.objects.filter(app=validated_data['app']).exists() and Subscription.objects.get(
                app=validated_data['app']) != instance:
            raise serializers.ValidationError("Subscription already exists for this app.")

        instance.plan = validated_data['plan']
        instance.active = validated_data['active']
        instance.app = validated_data['app']
        instance.save()

        return instance
