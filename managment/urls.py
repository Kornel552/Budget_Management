from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('logout/', views.logout_page, name='logout_page'),

    path('', views.home, name='home'),
    path('charts/', views.charts, name='charts'),
    path('category/', views.category, name='category')
]
