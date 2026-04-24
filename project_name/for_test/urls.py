from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    AssignRoleView,
    ProductCreateView,
    AvailableProductsView,
    ProductLessonsView,
    GrantAccessView,
    ProductListView,
    about_view,
    contacts_view,
    buy_product_view,
    home_view,
    profile_view
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('roles/assign/', AssignRoleView.as_view(), name='assign_role'),

    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/available/', AvailableProductsView.as_view(), name='available_products'),
    path('products/<int:product_id>/lessons/', ProductLessonsView.as_view(), name='product_lessons'),
    path('products/', ProductListView.as_view(), name='product-list'),

    path('access/grant/', GrantAccessView.as_view(), name='grant_access'),

    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('buy/<int:pk>/', buy_product_view, name='buy-product'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('', home_view, name='home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('buy/<int:pk>/', buy_product_view, name='buy-product'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
]