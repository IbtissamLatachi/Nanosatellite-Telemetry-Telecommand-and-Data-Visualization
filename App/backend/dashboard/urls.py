from django.urls import path
from . import views

urlpatterns = [
    path("/upload-passes", views.parse_and_store_gpredict_data, name="upload-passes"),
    path("/next-pass", views.get_next_satellite_pass, name="next-pass"),
]
