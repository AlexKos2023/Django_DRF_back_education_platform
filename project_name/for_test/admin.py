from django.contrib import admin
from .models import Product, Lesson, Group, ProductAccess

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'start_date', 'cost')
    fields = ('name', 'creator', 'start_date', 'cost', 'min_group_size', 'max_group_size')

admin.site.register(Lesson)
admin.site.register(Group)
admin.site.register(ProductAccess)