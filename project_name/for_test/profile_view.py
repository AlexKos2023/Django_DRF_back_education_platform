from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Product, ProductAccess


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    is_superuser = user.is_superuser

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.username = request.POST.get('username', '').strip()

        if user.username:
            user.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('profile')
        else:
            messages.error(request, 'Ник не может быть пустым')

    if is_superuser:
        authored_products = Product.objects.all()
        purchased_products = Product.objects.all()
        all_users = User.objects.all()
        all_groups = Group.objects.all()
        all_accesses = ProductAccess.objects.all()
        is_author = True
    else:
        authored_products = Product.objects.filter(creator=user)
        purchased_products = Product.objects.filter(accesses__user=user).distinct()
        all_users = None
        all_groups = None
        all_accesses = None
        is_author = authored_products.exists()

    context = {
        'full_name': user.get_full_name() or user.username,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'authored_products': authored_products,
        'purchased_products': purchased_products,
        'all_users': all_users,
        'all_groups': all_groups,
        'all_accesses': all_accesses,
        'is_author': is_author,
        'is_superuser': is_superuser,
    }
    return render(request, 'for_test/profile.html', context)