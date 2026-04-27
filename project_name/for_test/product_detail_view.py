@login_required(login_url='login')
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    lessons = product.lessons.prefetch_related('materials').all()

    has_access = (
        request.user.is_superuser
        or product.creator == request.user
        or ProductAccess.objects.filter(user=request.user, product=product).exists()
    )

    return render(request, 'for_test/product_detail.html', {
        'product': product,
        'lessons': lessons,
        'has_access': has_access,
    })