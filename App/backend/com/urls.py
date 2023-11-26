from django.urls import path
from . import views

urlpatterns = [
    path("/command", views.com_view, name="cam_view"),
    path("/getRate", views.getRate, name="getRate"),
]
