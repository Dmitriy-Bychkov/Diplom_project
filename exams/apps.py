from django.apps import AppConfig


class ExamsConfig(AppConfig):
    """ Представление общего заголовка 'тесты' в админке """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exams'
    verbose_name = 'тесты'
