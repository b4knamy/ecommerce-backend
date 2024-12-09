from django.core.mail import send_mail

from authentication.models import User
from payment.models import PaymentOrder


def send_costumer_email_congrats(products: PaymentOrder, user_object: User):
    user_email = "juninhomainmid@gmail.com"
    try:
        send_mail(
            subject="Congrats for your new product!",
            message="Thanks for buying with us, you will not regret.",
            recipient_list=[user_email],
            from_email=None
        )
        msg = f'Congrats email sended to email "{user_email}" sucessfully.'
    except Exception as error:
        print(error)
