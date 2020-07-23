from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns =[

    path('register/', views.register, name="register"),
    path('login_view/', views.login_view, name="login"),
    path('logout_view/', views.logout, name="logout"),

    # --------------api path----------
    path('put_user/', views.put_user),
    path('post_user/', views.post_user),
    path('login/', views.post_login, name='apilogin'),
]