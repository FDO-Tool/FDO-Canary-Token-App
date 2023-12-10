from django.urls import path
from . import views

urlpatterns = [
    path('subdomains/', views.SubdomainListView.as_view(), name='subdomain_list'),
    path('subdomains/create/', views.SubdomainCreateView.as_view(), name='subdomain_create'),
    path('subdomains/delete/<int:pk>/', views.SubdomainDeleteView.as_view(), name='subdomain_delete'),
]
