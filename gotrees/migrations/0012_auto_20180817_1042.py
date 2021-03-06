# Generated by Django 2.0.3 on 2018-08-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gotrees', '0011_treecodes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('image', models.CharField(max_length=100)),
                ('offer_name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='profiles',
            name='points',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='offers',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='offers', to='gotrees.Profiles'),
        ),
    ]
