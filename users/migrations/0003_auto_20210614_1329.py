# Generated by Django 3.0.5 on 2021-06-14 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210613_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'пользователь'), ('moderator', 'модератор'), ('admin', 'администратор'), ('django admin', 'администратор Django')], default='user', max_length=30),
        ),
    ]