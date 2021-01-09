from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('login/', obtain_jwt_token, name='login'),
    path('verify/', views.GetMyDataView.as_view(), name='token_verify'),
]
