from django.urls import path
from . import views

urlpatterns = [
    path("/command", views.adcs_view, name="adcs_view"),
    path("/getOperational", views.fetch_operational, name="getOperational"),
    path("/getHousekeeping", views.fetch_telemetry, name="getHousekeeping"),
]
