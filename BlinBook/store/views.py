from django.shortcuts import render, get_object_or_404, redirect
from pyjsparser.pyjsparserdata import messages
from django.contrib.auth.decorators import login_reqired
from django.shortcuts import redirect, get_object_or_404
from .models import Product, CartItem ,Order, OrderItem, PaymentForm
from django.db.models import Q

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products' : products})
# Create your views here.

#render will helping rendering the template render - (req, template_name, context(in dict_))

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_reqired
def add_to_cart(requests, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=requests.user, product=product)
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('product_list') #Or redirect to 'view-cart'

@login_reqired
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def remove_from_cart(request,item_id):
    item = get_object_or_404(CartItem,id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_reqired
def update_cart_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity',1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('view_cart')

@login_reqired
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']

            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    payment = payment_method
                )
            cart_items.delete()
            messages.success(request, "Your order has been placed successfully")
            return redirect('order_success')
    else:
        form = PaymentForm()

    return render(request, 'store/checkout.html', {'form': form, 'cart_items': cart_items})

def order_success(request):
    return render(request, 'store/order_success.html')

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html',{'orders': orders})

def store_home(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()

    if query:
        products = products.filer(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    return render(request, 'store/store_home.html', {'products': products})
