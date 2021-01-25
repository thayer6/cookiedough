from django.db import models
from django.utils import timezone


# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    job_url = models.CharField(max_length=250, unique=True, default="null")
    job_raw_text = models.CharField(max_length=250000, default="null")
    created_date = models.DateTimeField(default=timezone.now)
    job_clean_text = models.CharField(max_length=250000, default="null")

    """The parts of the model below here can't be added currently, need
    to remake the database
    """
    # is_job_expired = models.CharField(max_length=250, default="False")
    # # date job was posted on website gathered from
    # date_job_posted = models.DateTimeField(default=timezone.datetime(1999, 1, 1, 12, 12, 12))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

    class Admin:
        pass
