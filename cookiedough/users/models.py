from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from localflavor.us.us_states import STATE_CHOICES


class User(AbstractUser):
    """Default user for Cookie Dough."""

    #: First and last name do not cover name patterns around the globe
    # add bio to user info
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First Name"), blank=True, max_length=255)
    last_name = CharField(_("Last Name"), blank=True, max_length=255)
    city = CharField(_("City"), blank=True, max_length=255)
    state = CharField(
        _("State"), max_length=2, choices=STATE_CHOICES, null=True, blank=True
    )
    bio = CharField(("Bio"), blank=True, max_length=500)
    photo = models.ImageField(upload_to="profile_pics", blank=True)
    skills = CharField(_("Skills"), blank=True, max_length=250)
    jobs_of_interest = CharField(
        _("Job Titles of Interest"), blank=True, max_length=250
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
