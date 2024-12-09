
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from authentication.models import User
from settings.models import SiteSettings
from data.models import Color, Glasses
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data.models import Glasses
from core import settings
from payment.models import OrderItem, PaymentOrder
from payment.utils import send_costumer_email_congrats
from .serializers import ShoppingGlassesSerializer
import stripe
from django.views.decorators.csrf import csrf_exempt
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY_TEST


class PaymentCheckout(APIView):

    def get(self, request):
        slugs = request.GET.get("query", None)
        if slugs is not None:
            try:
                slugs_list = slugs.split(",")
                products = Glasses.objects.filter(
                    slug__in=slugs_list).distinct()
                products_serializer = ShoppingGlassesSerializer(
                    products, many=True)

                return Response(products_serializer.data, status=status.HTTP_200_OK)
            except Exception as error:
                return Response({"error": str(error)}, status=400)
        return Response(status=405)

    @authentication_classes(JWTAuthentication)
    @permission_classes(IsAuthenticated)
    def post(self, request):
        site_settings = SiteSettings.objects.all().first()

        try:
            products, user_id = self.fetch_products_related_data(request.data)

            line_items, metadata = self.create_session_line_items(
                products, user_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                metadata=metadata,
                mode='payment',
                success_url=site_settings.external_domain + '/checkout/result?success=true',
                cancel_url=site_settings.external_domain + '/checkout/result?canceled=true',
            )
        except Exception as e:
            return str(e)

        return Response({"checkout_url": checkout_session.url}, status.HTTP_303_SEE_OTHER)

    def fetch_products_related_data(self, data):
        user_id = data.get("user_ID")
        products_data = data.get("data")
        products = []
        for product in products_data:
            productID = product.get("productID")
            colorID = product.get("colorID")
            qtd = int(product.get("quantitaty"))
            if productID is not None:
                instance = Glasses.objects.get(pk=productID)

                products.append({
                    "product": instance,
                    "color_id": colorID,
                    "quantitaty": qtd
                })
        return products, user_id

    def create_session_line_items(self, products, user_id):
        line_items = []
        info = {}

        for product in products:
            qtd = product["quantitaty"]
            instance = product["product"]
            color = product["color_id"]
            obj = {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price_data': {
                    "currency": "brl",
                    'product_data': {
                                "name": instance.name,
                                "description": instance.description,
                                "images": ["https://i.imgur.com/Uflesa2.jpeg"]
                    },
                    "unit_amount": round(instance.amount * 100)
                },
                'quantity': qtd,
            }
            info[f"product_{instance.id}"] = {
                "product_id": instance.id,
                "color": color,
                "quantitaty": qtd,
            }
            line_items.append(obj)
        metadata = {
            "info": json.dumps({
                "data": info,
                "user": user_id
            })
        }

        return line_items, metadata


@csrf_exempt
def payment_web_hook(request):

    # return Response(status=status.HTTP_200_OK)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        print('Error parsing payload: {}'.format(str(e)))
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('Error verifying webhook signature: {}'.format(str(e)))
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        print("payment succeeded.")
    elif event.type == 'payment_method.attached':
        print("payment attached")
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
    # ... handle other event types
    elif event.type == "checkout.session.completed":
        session_data = event.data.object  # contains a stripe.PaymentIntent

        metadata = json.loads(session_data.metadata.info)
        user_id = metadata["user"]
        data = metadata["data"]

        user_object = User.objects.get(pk=user_id)
        payment_order = PaymentOrder.objects.create(
            checkout_id=session_data.id,
            user=user_object,
            payment_method=session_data.payment_method_types[0],
            is_installment=False,
            amount=session_data.amount_total,

        )
        payment_order.save()
        for value in data.values():
            product_id = value.get("product_id")
            color = value.get("color")
            quantitaty = value.get("quantitaty")

            related_product = Glasses.objects.get(pk=product_id)
            color_related = Color.objects.get(pk=color)

            new_order = OrderItem.objects.create(
                order=payment_order,
                product=related_product,
                color=color_related,
                quantitaty=quantitaty,
            )
            new_order.save()

        send_costumer_email_congrats(
            products=payment_order, user_object=user_object)
    else:
        print('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)
