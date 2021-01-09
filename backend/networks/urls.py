from django.urls import path

from networks import views

urlpatterns = [
    path('', views.NetworksView.as_view(), name='networks'),
    path('<str:network_id>/', views.NetworkDetailView.as_view(), name='get network'),
]
