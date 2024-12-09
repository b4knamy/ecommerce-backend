from django.contrib import admin

@admin.action(description='Ativar status de "Administrador" em selecionados')
def change_user_is_superuser_to_true(modeladmin, request, queryset):
    queryset.update(is_superuser=True)

@admin.action(description='Desativar status de "Administrador" em selecionados')
def change_user_is_superuser_to_false(modeladmin, request, queryset):
    queryset.update(is_superuser=False)


@admin.action(description='Ativar "Membro da equipe" em selecionados')
def change_user_is_staff_to_true(modeladmin, request, queryset):
    queryset.update(is_staff=True)

@admin.action(description='Desativar "Membro da equipe" em selecionados')
def change_user_is_staff_to_false(modeladmin, request, queryset):
    queryset.update(is_staff=False)

@admin.action(description='Ativar status de "Ativo" em selecionados')
def change_user_is_active_to_true(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description='Desativar status de "Ativo" em selecionados')
def change_user_is_active_to_false(modeladmin, request, queryset):
    queryset.update(is_active=False)