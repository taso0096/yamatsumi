from django.urls import path

from example import views

urlpatterns = [
    path('scores/', views.ScoresView.as_view(), name='score example'),
    path('questions/', views.QuestionsView.as_view(), name='questions example'),
]
