from django.urls import path
from .views import detect_scam, home

urlpatterns = [
    path("", home),
    path("honeypot/", detect_scam),
]
