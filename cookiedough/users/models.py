from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Cookie Dough."""

    #: First and last name do not cover name patterns around the globe
    # add bio to user info
    name = CharField(_("Name of User"), blank=True, max_length=255)
    bio = CharField(("Short Bio"), blank=True, max_length=500)
    photo = models.ImageField(upload_to="profile_pics", blank=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
