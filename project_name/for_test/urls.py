from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from .views import (
    home_view,
    ProductListView,
    about_view,
    contacts_view,
    buy_product_view,
    profile_view,
    profile_edit_view,
    register_view,
    edit_product_view,
    product_detail_view,
    lesson_create_view,
    lesson_edit_view,
    material_create_view,
    material_edit_view,
    ProductViewSet,
    LessonViewSet,
    LessonMaterialViewSet,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='api-product')
router.register(r'lessons', LessonViewSet, basename='api-lesson')
router.register(r'materials', LessonMaterialViewSet, basename='api-material')

urlpatterns = [
    path('', home_view, name='home'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', product_detail_view, name='product-detail'),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('buy/<int:pk>/', buy_product_view, name='buy-product'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
    path('profile/product/<int:pk>/edit/', edit_product_view, name='edit_product'),
    path('register/', register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include(router.urls)),
    path('products/<int:product_pk>/lessons/add/', lesson_create_view, name='lesson-create'),
    path('lessons/<int:pk>/edit/', lesson_edit_view, name='lesson-edit'),
    path('lessons/<int:lesson_pk>/materials/add/', material_create_view, name='material-create'),
    path('materials/<int:pk>/edit/', material_edit_view, name='material-edit'),
]