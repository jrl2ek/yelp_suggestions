# Generated by Django 2.1.4 on 2018-12-13 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Combine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('similar', models.ManyToManyField(blank=True, related_name='_restaurants_similar_+', to='yelp.Restaurants')),
            ],
        ),
        migrations.CreateModel(
            name='YelpCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('yelp_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='YelpCombo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userCat', models.CharField(max_length=90)),
                ('names', models.ManyToManyField(blank=True, through='yelp.Combine', to='yelp.Restaurants')),
            ],
        ),
        migrations.CreateModel(
            name='YelpUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('yelp_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='combine',
            name='combo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yelp.YelpCombo'),
        ),
        migrations.AddField(
            model_name='combine',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yelp.Restaurants'),
        ),
    ]
