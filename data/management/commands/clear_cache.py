

from django.core.management import BaseCommand
from django.conf import settings
from django.core.cache import caches, cache


class Command(BaseCommand):
    help = "Clear cache"

    def handle(self, **options):
        cache.clear()
        for k in settings.CACHES.keys():
            caches[k].clear()
            self.stdout.write("Cleared cache '{}'.\n".format(k))
