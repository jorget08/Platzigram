from django.apps import AppConfig


class UsersConfig(AppConfig):
    ##relacionarlo en la parte de setting.py en INSTALED APP
    name = 'users'
    #siempre debe ir el verbose
    verbose_name = 'Users'
