# Generated by Django 4.0.3 on 2022-03-10 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0007_alter_entry_user_alter_rec_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rec',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
