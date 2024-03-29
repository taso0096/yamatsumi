from django.urls import path

from . import views

urlpatterns = [
    path('', views.ExercisesView.as_view(), name='exercises'),
    path('<str:cyberspace_id>/', views.ExerciseDetailView.as_view(), name='get exercise'),
]
