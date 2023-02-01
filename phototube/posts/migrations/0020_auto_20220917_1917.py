# Generated by Django 2.2.16 on 2022-09-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20220916_2257'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='no_self_following',
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Оставьте сообщение', verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Оставьте сообщение', verbose_name='Текст'),
        ),
    ]
