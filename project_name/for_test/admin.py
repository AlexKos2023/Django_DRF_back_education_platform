from django.contrib import admin

from .models import Product, Lesson, LessonMaterial, ProductAccess, Profile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'start_date')
    search_fields = ('name', 'creator__username', 'creator__email')
    list_filter = ('start_date', 'creator')
    ordering = ('-start_date',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    search_fields = ('product__name',)
    list_filter = ('product',)


@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'material_type')
    search_fields = ('lesson__product__name',)
    list_filter = ('material_type', 'lesson')


@admin.register(ProductAccess)
class ProductAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'is_completed')
    search_fields = ('user__username', 'user__email', 'product__name')
    list_filter = ('is_completed', 'product')
    list_editable = ('is_completed',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'avatar')
    search_fields = ('user__username', 'user__email')