from django.urls import path
from . import views

urlpatterns = [
    path("/command", views.eps_view, name="eps_view"),
    path("/aespa", views.fetch_visualization_data, name="fetch_visualization_data"),
]
