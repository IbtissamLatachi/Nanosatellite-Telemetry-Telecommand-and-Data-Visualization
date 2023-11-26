from django.urls import path
from . import views

urlpatterns = [
    path("/command", views.obc_view, name="obc_view"),
    path(
        "/gettelem",
        views.fetch_obc_telemetry_command_data,
        name="fetch_obc_telemetry_command_data",
    ),
    path(
        "/getHk", views.fetch_obc_housekeeping_data, name="fetch_obc_housekeeping_data"
    ),
]
