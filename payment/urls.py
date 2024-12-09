from django.urls import path
from .views import PaymentCheckout, payment_web_hook


app_name = "payment"

urlpatterns = [
    path("products", view=PaymentCheckout.as_view(),
         name="shopping_products"),
    path("create-checkout-session", view=PaymentCheckout.as_view(),
         name="create_checkout_session"),

    path("payment_process", view=payment_web_hook, name="payment_web_hook")
]
