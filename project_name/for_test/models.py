from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class Product(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_products'
    )
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_group_size = models.PositiveSmallIntegerField(default=1)
    max_group_size = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name

    def clean(self):
        if self.min_group_size > self.max_group_size:
            raise ValidationError({'min_group_size': 'min_group_size не может быть больше max_group_size.'})

    @property
    def has_started(self):
        return self.start_date <= timezone.now()


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class LessonMaterial(models.Model):
    MATERIAL_VIDEO = 'video'
    MATERIAL_PRESENTATION = 'presentation'
    MATERIAL_TEXT = 'text'
    MATERIAL_FILE = 'file'

    MATERIAL_CHOICES = [
        (MATERIAL_VIDEO, 'Видео'),
        (MATERIAL_PRESENTATION, 'Презентация'),
        (MATERIAL_TEXT, 'Текст'),
        (MATERIAL_FILE, 'Файл'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    file = models.FileField(upload_to='lesson_materials/', blank=True, null=True)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f'{self.lesson.title} — {self.title}'


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='study_groups')
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='study_groups', blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class ProductAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='accesses')
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} -> {self.product}'