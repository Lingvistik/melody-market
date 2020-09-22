from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from cart.contexts import cart_content

import stripe

def payment(request):

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your shopping cart is empty...")
        return redirect(reverse('items'))

    current_cart = cart_content(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'payment/payment.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51HTvuPJari3DupfHRQJ0XuqrOVNPdMegdbpvSCtZFf5Y5lOQFVNnhieURYMR25zu68npeenxGq1WeaNZVeGot02S00MQ1JcaWh',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)