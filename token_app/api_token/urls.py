from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:uuid>/', views.receive_victim_request, name='receive_victim_request'),
]
