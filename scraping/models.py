from django.db import models
from django.utils import timezone


# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    job_url = models.CharField(max_length=250, unique=True, default="null")
    job_text = models.CharField(max_length=250000, default="null")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

    class Admin:
        pass
