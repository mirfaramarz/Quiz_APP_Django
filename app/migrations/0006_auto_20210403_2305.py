# Generated by Django 3.1.7 on 2021-04-03 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_quiz_win_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='Win_Payment',
            field=models.IntegerField(default=5),
        ),
    ]