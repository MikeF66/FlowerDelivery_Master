from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from orders.models import Order
from .forms import ReviewForm
from .models import Review


@login_required
def leave_review(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id)
    product = get_object_or_404(Product, id=product_id)

    existing_review = Review.objects.filter(product=product, user=request.user).first()

    if request.method == "POST":
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)  # Обновляем существующий отзыв
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Ваш отзыв успешно добавлен!")
            return redirect('orders:user_orders')  # Замените 'success_url' на нужный вам URL
    else:
        form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()

    context = {
        'order': order,
        'product': product,
        'form': form,
    }
    return render(request, 'reviews/leave_review.html', context)

def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, 'reviews/product_reviews.html', {'product': product, 'reviews': reviews})




