from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class RespositoryConfig(AppConfig):
    name = 'respository'

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'