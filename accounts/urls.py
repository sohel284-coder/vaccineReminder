from django.urls import path
from knox import views as knox_views

from accounts.views import *


urlpatterns = [
    path('login', login_page, name='login_page'),
    path('logout', logout_view, name='logout_view'),
    path('health-complex-user-register', health_complex_user_registration, name='health_complex_registration'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), ),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]