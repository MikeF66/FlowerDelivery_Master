from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.db.models import Avg, Count


def catalog(request):
    products = Product.objects.filter(available=True).order_by('name')
    paginator = Paginator(products, 6)  # потом можно увеличить до 12 продуктов на страницу,
    # см. твкже def search_products(request):  paginator = Paginator(products, 6)
    page_number = request.GET.get('page')  # Должно быть None, если параметр 'page' не передан
    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context = {
        'page_number': page_number,
        'page_obj': page_obj,
        'products': products,
    }
    for product in products:
        product.avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.review_count = product.reviews.aggregate(Count('id'))['id__count'] or 0
    return render(request, 'catalog/home.html', context)


def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(price__icontains=query) |
        Q(short_description__icontains=query) |
        Q(description__icontains=query)
    ) if query else Product.objects.none()

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'catalog/search_results.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    page_number = request.GET.get('page')  # Захватываем значение 'page' из GET-запроса
    referer_url = request.META.get('HTTP_REFERER', '/')  # Получаем предыдущий URL или домашнюю страницу по умолчанию
    context = {
        'page_number': page_number,
        'product': product,
        'referer_url': referer_url
    }
    return render(request, 'catalog/product_detail.html', context)

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно добавлен.')
            return redirect('catalog:home')
    else:
        form = ProductForm()
    context = {
        'form': form,
        'caption': 'Добавить товар',
    }

    return render(request, 'catalog/edit_product.html', context)


@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    page_number = request.GET.get('page', 1)  # Получаем номер страницы каталога из GET-запроса
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно обновлен.')
            return redirect(f'/product/{product_id}/?page={page_number}')
    else:
        form = ProductForm(instance=product)
    context = {
        'page_number': page_number,
        'form': form,
        'caption': 'Редактировать товар'
    }
    return render(request, 'catalog/edit_product.html', context)


@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('catalog:home')






