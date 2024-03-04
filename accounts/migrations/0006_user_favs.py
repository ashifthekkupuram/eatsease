# Generated by Django 5.0.1 on 2024-02-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_contactaddress_house_number_and_more'),
        ('foods', '0003_alter_item_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favs',
            field=models.ManyToManyField(blank=True, related_name='favs', to='foods.item'),
        ),
    ]