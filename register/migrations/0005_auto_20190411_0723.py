# Generated by Django 2.1.7 on 2019-04-11 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_corporate_net_worth'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporate',
            name='pass_word',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='individual',
            name='pass_word',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]