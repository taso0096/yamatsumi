from django.urls import path

from cyberspaces import views

urlpatterns = [
    path('', views.CyberspacesView.as_view(), name='cyberspaces'),
    path('<str:exercise_id>/', views.CyberspaceDetailView.as_view(), name='get cyberspace'),
]
