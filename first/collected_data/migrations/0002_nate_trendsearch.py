# Generated by Django 5.0.3 on 2024-06-15 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collected_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NATE_TrendSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank_num', models.IntegerField()),
                ('search_word', models.CharField(max_length=200)),
                ('rank_updown', models.CharField(max_length=20)),
                ('provide_datetime', models.DateTimeField(verbose_name='When provided')),
            ],
            options={
                'db_table': 'NATE_TRENDSEARCH',
                'db_table_comment': '네이트 인기검색어',
            },
        ),
    ]
