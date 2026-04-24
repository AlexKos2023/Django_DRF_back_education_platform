from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products')
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_group_size = models.PositiveSmallIntegerField(default=1)
    max_group_size = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name

    @property
    def has_started(self):
        return self.start_date <= timezone.now()


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    video_link = models.URLField()

    def __str__(self):
        return self.title


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='study_groups')
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='study_groups', blank=True)

    def __str__(self):
        return self.name


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_accesses')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accesses')
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} -> {self.product.name}'