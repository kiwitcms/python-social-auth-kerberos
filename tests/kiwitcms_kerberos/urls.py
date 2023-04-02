from django.urls import include, path
from tcms.urls import urlpatterns


urlpatterns += [
    path('', include('social_django.urls', namespace='social')),
]
