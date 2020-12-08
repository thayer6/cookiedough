from django.urls import path

from . import views

urlpatterns = [
    # hook up the root URL with the project_index view
    # path("", views.project_index, name = "project_index"),
    path("jobs/", views.job_index, name="job_index"),
    # dynamically generate URL depending on the project you want to view
    # value passed in the URL is an integer and it's variable is pk
    # path("<int:pk>/", views.project_detail, name = "project_detail"),
    path("<int:pk>/", views.job_detail, name="job_detail"),
]
