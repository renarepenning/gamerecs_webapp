# Generated by Django 4.0.3 on 2022-03-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0010_alter_rec_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rec',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]