from django.db import models


class UserManager(models.Manager):
    def get_queryset(self):
        # All users
        return super().get_queryset().filter(is_active=True)

    def all_active_users(self):
        # All posts
        return super().get_queryset().filter(is_active=True)

    def all_male(self):
        # All drafted posts
        return super().get_queryset().filter(gender__iexact="Male")

    def all_female(self):
        # All drafted posts
        return super().get_queryset().filter(gender__iexact="Female")

    def all_cheifs(self):
        # All drafted posts
        return super().get_queryset().filter(royals__iexact="Chief")
