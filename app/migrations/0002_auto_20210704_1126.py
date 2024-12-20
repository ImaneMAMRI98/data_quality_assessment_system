# Generated by Django 3.2.3 on 2021-07-04 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='float',
            name='MetaData',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.metadata'),
        ),
        migrations.AlterField(
            model_name='float',
            name='Val_Max',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='float',
            name='Val_Min',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='int',
            name='MetaData',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.metadata'),
        ),
        migrations.AlterField(
            model_name='int',
            name='Val_Max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='int',
            name='Val_Min',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='string',
            name='Expression_Reguliere',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='string',
            name='MetaData',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.metadata'),
        ),
        migrations.AlterField(
            model_name='string',
            name='longeur_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='string',
            name='longeur_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
