from django.urls import include
from django.urls import path
from tcms.urls import urlpatterns


urlpatterns += [
    path("", include("social_django.urls", namespace="social")),
]
