
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from comments.models import Comments
from data.models import Glasses
from authentication.models import User
from faker import Faker


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--og", action="store_true")

    def handle(self, *args, **kwargs):
        glasses = Glasses.objects.all()
        users = User.objects.all()
        fk = Faker()

        for _ in glasses:
            will_have_comments = fk.boolean(80)
            if will_have_comments:
                for i in range(fk.random_int(1, 10)):
                    current_user = users[i]
                    text = fk.text(120)
                    title = fk.text(30)
                    color = _.color.all().first()
                    new_comment = Comments.objects.create(
                        glasses=_,
                        color=color,
                        text=text,
                        title=title,
                        rating=fk.random_int(1, 5),
                        user=current_user
                    )
                    new_comment.save()

        self.stdout.write(self.style.SUCCESS("Comentários criados!"))
