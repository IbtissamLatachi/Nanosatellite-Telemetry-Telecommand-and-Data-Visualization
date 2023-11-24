from django.urls import path
from . import views

urlpatterns = [
    path("/command", views.cam_view, name="cam_view"),
    path("/getImages", views.fetch_images, name="fetch_images"),
]
