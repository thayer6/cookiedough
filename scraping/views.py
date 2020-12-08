from django.shortcuts import render

from scraping.models import Job


# Create your views here.
def job_index(request):
    jobs = Job.objects.all()
    context = {"jobs": jobs}

    return render(request, "job_index.html", context)


def job_detail(request, pk):
    job = Job.objects.get(pk=pk)
    context = {"job": job}
    return render(request, "job_detail.html", context)
