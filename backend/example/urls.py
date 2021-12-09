from django.urls import path

from example import views

urlpatterns = [
    path('scores/', views.ScoresView.as_view(), name='score example'),
    path('questions/', views.QuestionsView.as_view(), name='questions example'),
    path('ipaddresses/', views.IpAddressesView.as_view(), name='ipaddresses example'),
    path('extra/', views.ExtraView.as_view(), name='extra example'),
]
