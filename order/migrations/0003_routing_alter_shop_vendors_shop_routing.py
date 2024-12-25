# Generated by Django 5.0.3 on 2024-12-18 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Routing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Маршрут')),
            ],
        ),
        migrations.AlterField(
            model_name='shop',
            name='vendors',
            field=models.ManyToManyField(blank=True, null=True, related_name='shops', to=settings.AUTH_USER_MODEL, verbose_name='Продавцы'),
        ),
        migrations.AddField(
            model_name='shop',
            name='routing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shops', to='order.routing', verbose_name='Маршрут'),
        ),
    ]