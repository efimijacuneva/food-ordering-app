from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, OrderForm
from .models import MenuItem, Order, OrderItem, CustomUser
from django.core.mail import send_mail
from django.conf import settings
from .forms import GuestOrderForm

def menu(request):
    items = MenuItem.objects.all()
    categories = MenuItem.CATEGORY_CHOICES
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for item_id, data in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            quantity = data.get('quantity', 0)
            if not isinstance(quantity, (int, float)) or quantity <= 0:
                continue
            cart_items.append({
                'menu_item': item,
                'quantity': quantity,
                'notes': data.get('notes', ''),
            })
            total_price += item.price * quantity
        except MenuItem.DoesNotExist:
            continue
    return render(request, 'menu.html', {
        'items': items,
        'categories': categories,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart': cart,
    })

def menu_by_category(request, category):
    valid_categories = [cat[0] for cat in MenuItem.CATEGORY_CHOICES]
    if category not in valid_categories:
        messages.error(request, "Invalid category.")
        return redirect('menu')
    
    items = MenuItem.objects.filter(category=category)
    categories = MenuItem.CATEGORY_CHOICES
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for item_id, data in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            quantity = data.get('quantity', 0)
            if not isinstance(quantity, (int, float)) or quantity <= 0:
                continue
            cart_items.append({
                'menu_item': item,
                'quantity': quantity,
                'notes': data.get('notes', ''),
            })
            total_price += item.price * quantity
        except MenuItem.DoesNotExist:
            continue
        except (ValueError, TypeError):
            continue
    
    return render(request, 'menu.html', {
        'items': items,
        'categories': categories,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart': cart,
        'selected_category': category,
    })

def add_to_cart(request, item_id):
    try:
        menu_item = MenuItem.objects.get(id=item_id)
    except MenuItem.DoesNotExist:
        messages.error(request, "Invalid item selected.")
        return redirect('menu')

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        notes = request.POST.get('notes', '').strip()

        if quantity < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('menu')
        if len(notes) > 500:
            messages.error(request, "Notes cannot exceed 500 characters.")
            return redirect('menu')

        if str(item_id) in cart:
            cart[str(item_id)]['quantity'] += quantity
            cart[str(item_id)]['notes'] = notes
        else:
            cart[str(item_id)] = {'quantity': quantity, 'notes': notes}

        request.session['cart'] = cart
        request.session.modified = True
        return redirect('menu')
    return render(request, 'add_to_cart.html', {'item': menu_item})

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    try:
        menu_item = MenuItem.objects.get(id=item_id)
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart
            request.session.modified = True
    except MenuItem.DoesNotExist:
        messages.error(request, "Invalid item.")
    return_to = request.GET.get('return_to', '/menu/')
    return redirect(return_to)

def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')
    cart_items = []
    total_price = 0
    items = MenuItem.objects.all()
    for item_id, data in cart.items():
        try:
            item = MenuItem.objects.get(id=item_id)
            quantity = data.get('quantity', 0)
            if not isinstance(quantity, (int, float)) or quantity <= 0:
                continue
            cart_items.append({
                'menu_item': item,
                'quantity': quantity,
                'notes': data.get('notes', ''),
            })
            total_price += item.price * quantity
        except MenuItem.DoesNotExist:
            continue

    if not cart_items:
        return redirect('menu')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = GuestOrderForm(request.POST)
            if form.is_valid():
                order = Order.objects.create(
                    user=None,
                    guest_email=form.cleaned_data.get('email'),
                    guest_phone=form.cleaned_data.get('phone'),
                    total_price=total_price,
                )
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        menu_item=item['menu_item'],
                        quantity=item['quantity'],
                        notes=item['notes'],
                    )
                request.session['cart'] = {}
                request.session.modified = True
                return redirect('order_success')
            else:
                messages.error(request, "Please fill in all required fields correctly.")
        else:
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item['menu_item'],
                    quantity=item['quantity'],
                    notes=item['notes'],
                )
            request.session['cart'] = {}
            request.session.modified = True
            return redirect('order_success')
    else:
        form = GuestOrderForm() if not request.user.is_authenticated else None

    return render(request, 'place_order.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
        'items': items,
    })

def order_success(request):
    items = MenuItem.objects.all()
    return render(request, 'order_success.html', {'items': items})

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def restaurant_dashboard(request):
    pending_orders = Order.objects.filter(status='PENDING').order_by('-created_at')
    accepted_orders = Order.objects.filter(status='ACCEPTED').order_by('-created_at')
    completed_orders = Order.objects.filter(status__in=['READY', 'DELIVERED']).order_by('-created_at')
    items = MenuItem.objects.all()
    return render(request, 'restaurant_dashboard.html', {
        'pending_orders': pending_orders,
        'accepted_orders': accepted_orders,
        'completed_orders': completed_orders,
        'items': items,
    })

@login_required
@user_passes_test(is_staff)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            if new_status == 'ACCEPTED' and order.status != 'ACCEPTED':
                email = order.guest_email if order.guest_email else (order.user.email if order.user else None)
                if email:
                    try:
                        send_mail(
                            subject='Your Order Has Been Accepted',
                            message=f'Dear Customer,\n\nYour order (ID: {order.id}) has been accepted by Tasty Restaurant. We are preparing it now!\n\nThank you for your order.',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email],
                            fail_silently=True,
                        )
                    except Exception as e:
                        print(f"Failed to send email: {e}")
            order.status = new_status
            order.save()
    return redirect('restaurant_dashboard')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    items = MenuItem.objects.all()
    return render(request, 'order_history.html', {'orders': orders, 'items': items})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('menu')
    else:
        form = CustomUserCreationForm()
    items = MenuItem.objects.all()
    return render(request, 'registration/register.html', {'form': form, 'items': items})