from django.urls import path

from socketio_app import views

urlpatterns = [
    path('answer/<str:network_id>/', views.AnswerView.as_view(), name='answer'),
]
