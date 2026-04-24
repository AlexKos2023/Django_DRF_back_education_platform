from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Product

def home_view(request):
    return render(request, 'for_test/home.html')

class ProductListView(ListView):
    model = Product
    template_name = 'for_test/product_list.html'
    context_object_name = 'products'

def about_view(request):
    return render(request, 'for_test/about.html')

def contacts_view(request):
    return render(request, 'for_test/contacts.html')

@login_required(login_url='login')
def buy_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'for_test/buy.html', {'product': product})

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'for_test/profile.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})