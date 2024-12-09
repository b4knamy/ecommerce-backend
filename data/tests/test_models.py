import pytest
from data.models import OculosType, Color, Oculos, OculosModelo
from faker import Faker
from random import randint

fk = Faker()
obj_range = 5
sex_list = ["M", "F", "U"]


@pytest.fixture
def c_f_d():
    oculos_types = [OculosType.objects.create(
        oculos_type=fk.name()) for _ in range(obj_range)]
    oculos_color = [Color.objects.create(
        name=fk.color()) for _ in range(obj_range)]
    oculos_model = [OculosModelo.objects.create(
        modelo=fk.name()) for _ in range(obj_range)]
    oculos = [Oculos.objects.create(
        name=fk.name(),
        tipo=oculos_types[randint(0, 3)],
        modelo=oculos_model[randint(0, 3)],
        cor=oculos_color[randint(0, 3)],
        quantidade=randint(0, 50),
        preco=randint(0, 2000),
        preco_parcelado=randint(100, 250),
        is_promocao=fk.boolean(),
        preco_promocao=randint(0, 1800),
        preco_parcelado_promocao=randint(100, 200),
        sexo=sex_list[randint(0, 2)],
        image=fk.image_url(),
        produto_inicio=fk.boolean(),
    ) for _ in range(obj_range)
    ]
    yield {
        "types": oculos_types,
        "models": oculos_model,
        "colors": oculos_color,
        "oculos": oculos,

    }


@pytest.mark.django_db
def test_create_oculos_type(c_f_d):
    types = c_f_d["types"]

    assert obj_range == len(types)


@pytest.mark.django_db
def test_create_model(c_f_d):
    models = c_f_d["models"]
    assert obj_range == len(models)


@pytest.mark.django_db
def test_create_color(c_f_d):

    colors = c_f_d["colors"]

    assert obj_range == len(colors)


@pytest.mark.django_db
def test_create_oculos(c_f_d):
    oculos = c_f_d["oculos"]

    assert obj_range == len(oculos)
