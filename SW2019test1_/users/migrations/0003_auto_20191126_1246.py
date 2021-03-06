# Generated by Django 2.2.5 on 2019-11-26 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_movie_recommendedmovie_score_usermovie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='recommendedmovie',
            name='recommend_list',
            field=models.ManyToManyField(blank=True, to='users.Movie'),
        ),
        migrations.AlterField(
            model_name='usermovie',
            name='movie_list',
            field=models.ManyToManyField(blank=True, to='users.Movie'),
        ),
    ]
