from django.urls import path
from .views import auth_views, category_views, charts_views, elements_views, home_views

urlpatterns = [
    path('login/', auth_views.login_page, name='login_page'),
    path('register/', auth_views.register_page, name='register_page'),
    path('logout/', auth_views.logout_page, name='logout_page'),

    path('', home_views.home, name='home'),
    path('charts_choice/', charts_views.charts_choice, name='charts_choice'),
    path('charts/<int:item_id>', charts_views.charts, name='charts'),
    path('elements/', elements_views.elements, name='elements'),
    path('category/', category_views.category, name='category')
]
