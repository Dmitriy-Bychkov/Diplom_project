from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Section(models.Model):
    """ Модель образовательных разделов """

    section_name = models.CharField(max_length=100, verbose_name='название раздела')
    section_preview = models.ImageField(upload_to='sections/', default='no_image.jpg',
                                        verbose_name='изображение раздела', **NULLABLE)
    section_description = models.TextField(verbose_name='описание раздела', **NULLABLE)
    section_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      limit_choices_to={'is_staff': True},
                                      verbose_name='владелец раздела', **NULLABLE)

    def __str__(self):
        return self.section_name

    class Meta:
        """ Представление написания заголовков в админке """

        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'


class Material(models.Model):
    """ Модель обучающих материалов """

    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='раздел')
    material_name = models.CharField(max_length=100, verbose_name='название материала')
    material_description = models.TextField(verbose_name='описание материала', **NULLABLE)
    material_preview = models.ImageField(upload_to='materials/', default='no_image.jpg',
                                         verbose_name='изображение материала', **NULLABLE)
    material_url = models.URLField(verbose_name='ссылка на видео материала', **NULLABLE)
    material_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       limit_choices_to={'is_staff': True},
                                       verbose_name='владелец материала', **NULLABLE)

    def __str__(self):
        return f'{self.material_name}, {self.material_description}, {self.material_preview}'

    class Meta:
        """ Представление написания заголовков в админке """

        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
