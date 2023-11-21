from django.urls import path
from . import views

urlpatterns = [
    path("", views.eps_view, name="eps_view"),
]
