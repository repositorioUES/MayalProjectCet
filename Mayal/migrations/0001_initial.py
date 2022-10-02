# Generated by Django 3.2.4 on 2022-08-31 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreCat', models.CharField(help_text='Nombre de la Categoría', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreSub', models.CharField(help_text='Nombre de la Subcategoría', max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mayal.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='Galeria')),
                ('nombreProd', models.CharField(max_length=250)),
                ('coleccion', models.CharField(max_length=250)),
                ('material', models.CharField(max_length=250)),
                ('color', models.CharField(max_length=250)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Mayal.categoria')),
                ('subCategoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Mayal.subcategoria')),
            ],
        ),
    ]
