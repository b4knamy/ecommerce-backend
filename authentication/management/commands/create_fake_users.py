
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from authentication.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--og", action="store_true")

    def handle(self, *args, **kwargs):
        fk = Faker()
        password = make_password("1234!@#$Fk")
        for _ in range(10):
            f_name = fk.first_name()
            l_name = fk.last_name()
            email = fk.email()

            new_user = User.objects.create(
                first_name=f_name,
                last_name=l_name,
                email=email,
                password=password
            )
            new_user.save()

        self.stdout.write(self.style.SUCCESS("Usuários criados!"))
