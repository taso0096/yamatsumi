from django.urls import path

from . import views

urlpatterns = [
    path('', views.GamesView.as_view(), name='games'),
    path('<str:network_id>/', views.GameDetailView.as_view(), name='get game'),
]
