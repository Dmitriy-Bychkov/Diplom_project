# Generated by Django 4.2.7 on 2023-11-30 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_alter_material_material_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['section__section_name'], 'verbose_name': 'материал', 'verbose_name_plural': 'материалы'},
        ),
    ]
