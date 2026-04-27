from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework import viewsets

from .forms import (
    LessonForm,
    LessonMaterialForm,
    CustomUserCreationForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import Product, ProductAccess, Profile, Lesson, LessonMaterial
from .serializers import ProductSerializer, LessonSerializer, LessonMaterialSerializer

User = get_user_model()

def home_view(request):
    products = Product.objects.all()
    return render(request, 'for_test/home.html', {'products': products})


def about_view(request):
    return render(request, 'for_test/about.html')


def contacts_view(request):
    return render(request, 'for_test/contacts.html')


def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    authored_products = Product.objects.filter(creator=user)
    purchased_products = Product.objects.filter(accesses__user=user, accesses__is_completed=False).distinct()
    completed_products = Product.objects.filter(accesses__user=user, accesses__is_completed=True).distinct()

    return render(request, 'for_test/profile.html', {
        'profile': profile,
        'authored_products': authored_products,
        'purchased_products': purchased_products,
        'completed_products': completed_products,
    })



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'for_test/edit_product.html', {'product': product})


class ProductListView(ListView):
    model = Product
    template_name = 'for_test/product_list.html'
    context_object_name = 'products'
    ordering = ['-start_date']


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    lessons = product.lessons.prefetch_related('materials').all()

    has_access = False
    if request.user.is_authenticated:
        has_access = (
            request.user.is_superuser
            or request.user == product.creator
            or ProductAccess.objects.filter(user=request.user, product=product).exists()
        )

    return render(request, 'for_test/product_detail.html', {
        'product': product,
        'lessons': lessons,
        'has_access': has_access,
    })


@login_required
def buy_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ProductAccess.objects.get_or_create(user=request.user, product=product)
    return redirect('product-detail', pk=product.pk)


@login_required
def lesson_create_view(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.product = product
            lesson.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = LessonForm()

    return render(request, 'for_test/lesson_form.html', {
        'form': form,
        'product': product,
    })


@login_required
def lesson_edit_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    product = lesson.product

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'for_test/lesson_form.html', {
        'form': form,
        'product': product,
        'lesson': lesson,
    })


@login_required
def material_create_view(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    product = lesson.product

    if request.method == 'POST':
        form = LessonMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.lesson = lesson
            material.save()
            return redirect('product-detail', pk=product.pk)
    else:
        initial = {}
        material_type = request.GET.get('type')
        if material_type in (
            LessonMaterial.MATERIAL_TEXT,
            LessonMaterial.MATERIAL_FILE,
            LessonMaterial.MATERIAL_VIDEO,
            LessonMaterial.MATERIAL_PRESENTATION,
        ):
            initial['material_type'] = material_type
        form = LessonMaterialForm(initial=initial)

    return render(request, 'for_test/material_form.html', {
        'form': form,
        'lesson': lesson,
        'product': product,
    })


@login_required
def material_edit_view(request, pk):
    material = get_object_or_404(LessonMaterial, pk=pk)
    lesson = material.lesson
    product = lesson.product

    if request.method == 'POST':
        form = LessonMaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('product-detail', pk=product.pk)
    else:
        form = LessonMaterialForm(instance=material)

    return render(request, 'for_test/material_form.html', {
        'form': form,
        'lesson': lesson,
        'product': product,
        'material': material,
    })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonMaterialViewSet(viewsets.ModelViewSet):
    queryset = LessonMaterial.objects.all()
    serializer_class = LessonMaterialSerializer

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    authored_products = Product.objects.filter(creator=user)
    purchased_products = Product.objects.filter(accesses__user=user, accesses__is_completed=False).distinct()
    completed_products = Product.objects.filter(accesses__user=user, accesses__is_completed=True).distinct()

    return render(request, 'for_test/profile.html', {
        'authored_products': authored_products,
        'purchased_products': purchased_products,
        'completed_products': completed_products,
    })


@login_required(login_url='login')
def profile_edit_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'for_test/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    })