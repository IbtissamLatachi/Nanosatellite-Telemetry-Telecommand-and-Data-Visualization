from django.urls import path
from . import views

urlpatterns = [
    # Add a URL pattern for the obc_view view
    path('', views.obc_view, name='obc_view'),
    # Add other URL patterns as needed
]
