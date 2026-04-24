from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home_view,
    ProductListView,
    about_view,
    contacts_view,
    buy_product_view,
    profile_view,
    register_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('buy/<int:pk>/', buy_product_view, name='buy-product'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]