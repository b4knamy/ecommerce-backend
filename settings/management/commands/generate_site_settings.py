
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from settings.models import SiteSettings, APIConfigs


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--og", action="store_true")

    def handle(self, *args, **kwargs):

        site_config = SiteSettings.objects.create(
            site_name="Oculos de Fábrica",
            site_domain="http://localhost",
            default_image_url="unknow",
            filter_1="Categorias",
            param_1="categoria",
            filter_2="Cores",
            param_2="cor",
            filter_3="Modelos",
            param_3="modelo",
            filter_4="Formatos",
            param_4="formato",
            filter_5="Marcas",
            param_5="Marca",
            filter_6="Ordem",
            param_6="ordem",
        )
        site_config.save()

        self.stdout.write(self.style.SUCCESS("Configuração criada!"))

        api_data = [
            ["checkout", "api/payment/create-checkout-session",
                "(PAYMENT) checkout"],
            ["payment_products", "api/payment/products",
                "(PAYMENT) get products information"],
            ["change", "api/auth/user/password/change",
                "(AUTH) password change"],
            ["reset_code", "api/auth/user/password/reset-code",
                "(AUTH) reset code"],
            ["user_profile", "api/auth/profile/user/",
                "(AUTH) user profile data"],
            ["csrf", "api/auth/csrftoken", "(AUTH) csrf token"],
            ["logout", "api/auth/token/logout", "(AUTH) token logout"],
            ["verify", "api/auth/token/verify", "(AUTH) token verify"],
            ["refresh", "api/auth/token/refresh", "(AUTH) token refresh"],
            ["token", "api/auth/token", "(AUTH) get user token"],
            ["get_user_data", "api/auth/user/data", "(AUTH) get user data"],
            ["create_user", "api/auth/user/create", "(AUTH) create user"],
            ["comments", "api/comments/glasses/", "(COMMENTS CRUD)"],
            ["navbar_filters", "api/glasses/nav", "(NAVBAR) filtros"],
            ["dynamic_search", "api/glasses/search/dynamic",
                "(NAVBAR) pesquisa dinamica"],
            ["product_profile", "api/glasses/profile/",
                "(PRODUTO) perfil de produto"],
            ["promotions", "api/glasses/promotions", "(HOME) Promoções"],
            ["filters", "api/glasses/filters", "(PESQUISA) dados de filtros"],
            ["products", "api/glasses/search", "(PESQUISA) produtos"],
        ]

        for api in api_data:
            api_settings = APIConfigs.objects.create(
                name=api[0],
                url=api[1],
                reference=api[2]
            )
            api_settings.save()

        self.stdout.write(self.style.SUCCESS("Apis criadas!"))
