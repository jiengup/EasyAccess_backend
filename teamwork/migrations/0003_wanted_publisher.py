# Generated by Django 3.0.5 on 2020-05-19 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
        ('teamwork', '0002_wanted_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='wanted',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wanted_who_publish', to='myauth.User'),
        ),
    ]