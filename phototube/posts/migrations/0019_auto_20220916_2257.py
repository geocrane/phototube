# Generated by Django 2.2.16 on 2022-09-16 22:57

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_auto_20220913_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='no_self_following',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='pub_date',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='no_self_following'),
        ),
    ]
