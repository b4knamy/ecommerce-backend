

# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# django.setup()


class Eoq:

    def __call__(self, *args, **kwargs):
        print("fui chamado aq em")
        return 1


a = Eoq()

print(a())
