
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from data.models import Brand, Glasses, Model, Category, Color, Model, Shape
from faker import Faker
from random import randint


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--og", action="store_true")

    def handle(self, *args, **kwargs):

        if not kwargs["og"]:
            _categories = ["Oculos de Sol", "Oculos de Grau",
                           "Oculos de Leitura", "Oculos Esportivos", "Óculos de Luz Azul"]
            _models = ["Aviador", "Wayfarer", "Redondo", "Gato", "Retangular"]
            _shapes = ["Oval", "Quadrado", "Redondo", "Hexagonal", "Borboleta"]
            _colors = [["Preto", "rgb(0, 0, 0)"], ["Amarelo", "rgb(241, 235, 1)"], [
                "Verde", "rgb(95, 244, 1)"], ["Vermelho", "rgb(230, 20, 1)"], ["Laranja", "rgb(255, 172, 1)"]]
            _brands = ["Ana Hickmann", "Chilli Beans",
                       "Ray-Ban", "Oakley", "Gucci"]

            for _ in _categories:
                new = Category.objects.create(name=_)
                new.save()

            for _ in _colors:
                new = Color.objects.create(name=_[0], css_color=_[1])
                new.save()

            for _ in _models:
                new = Model.objects.create(name=_)
                new.save()

            for _ in _shapes:
                new = Shape.objects.create(name=_)
                new.save()

            for _ in _brands:
                new = Brand.objects.create(name=_)
                new.save()

        fk = Faker()
        sex = ["Masculino", "Feminino", "Unissex"]
        all_models = Model.objects.all()
        all_category = Category.objects.all()
        all_brands = Brand.objects.all()
        all_shapes = Shape.objects.all()
        all_colors = Color.objects.all()
        for i in range(100):
            name = fk.name()
            is_promo = fk.boolean(25)
            new_glass = Glasses.objects.create(
                name=name,
                amount=randint(200, 1000),
                quantitaty=randint(1, 20),
                gender=sex[randint(0, 2)],
                installments_amount=randint(100, 199),
                installments_count=12,
                discount=randint(10, 40) if is_promo else 0,
                is_sample=True if is_promo else False,
                is_promo=is_promo,
                bridge=fk.text(15),
                nose_pads=fk.text(15),
                temple=fk.text(20),
                rim=fk.text(20),
                description=fk.text(120),
                width=fk.text(12),
                height=fk.text(12),
                warranty=f"Garantia de 12 meses",
                material=fk.text(20),
            )
            new_glass.shape.add(all_shapes[randint(0, 4)])
            new_glass.category.add(all_category[randint(0, 4)])
            new_glass.model.add(all_models[randint(0, 4)])
            new_glass.brand.add(all_brands[randint(0, 4)])
            new_glass.color.add(all_colors[randint(0, 4)])
            new_glass.save()

        self.stdout.write(self.style.SUCCESS("Dados criados!"))
