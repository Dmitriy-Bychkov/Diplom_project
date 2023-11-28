from django.contrib import admin
from education.models import Section, Material


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """ Представление образовательных разделов в админке """

    list_display = ('section_name', 'section_owner')
    search_fields = ('section_name', 'section_description', 'section_owner',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """ Представление образовательных материалов в админке """

    list_display = ('material_name', 'section', 'material_description', 'material_url', 'material_owner')
    search_fields = ('section', 'material_name', 'material_description', 'material_owner',)
