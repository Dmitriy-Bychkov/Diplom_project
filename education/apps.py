from django.apps import AppConfig


class EducationConfig(AppConfig):
    """ Представление заголовка в админке """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education'
    verbose_name = 'образовательные темы'
