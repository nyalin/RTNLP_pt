# Generated by Django 5.0.3 on 2024-07-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collected_data', '0004_remove_cltdata_maininfo_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navr_recentnews',
            name='news_title',
            field=models.CharField(max_length=250),
        ),
    ]
