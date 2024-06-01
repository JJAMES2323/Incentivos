# Generated by Django 5.0.2 on 2024-04-23 03:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Incentivos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cedula", models.IntegerField()),
                ("nombre", models.CharField(max_length=30, null=True)),
                ("modulo", models.CharField(max_length=30)),
                ("eficiencia", models.CharField(max_length=30)),
                ("turno", models.FloatField()),
                ("fecha", models.DateField(null=True)),
                ("incentivo", models.FloatField()),
                ("estado", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Inventario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Referencia", models.CharField(max_length=30, null=True)),
                ("color", models.CharField(max_length=30, null=True)),
                ("talla", models.CharField(max_length=30, null=True)),
                ("SKU", models.CharField(max_length=30)),
                ("unidades", models.IntegerField()),
                ("SAM", models.FloatField()),
                ("minutosProducidos", models.FloatField()),
                ("fecha", models.DateField(null=True)),
                ("modulo", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Operario",
            fields=[
                ("cedula", models.IntegerField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=30, null=True)),
                ("modulo", models.CharField(max_length=30)),
                ("correoE", models.EmailField(max_length=30, null=True)),
                ("telefono", models.IntegerField(null=True)),
                ("fechaN", models.DateField(null=True)),
                ("direccion", models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Ordenes",
            fields=[
                ("orden", models.AutoField(primary_key=True, serialize=False)),
                ("Referencia", models.CharField(max_length=30, null=True)),
                ("color", models.CharField(max_length=30, null=True)),
                ("talla", models.CharField(max_length=30, null=True)),
                ("modulo", models.CharField(max_length=30)),
                ("SKU", models.CharField(max_length=30)),
                ("unidades", models.IntegerField()),
                ("unidadesLeidas", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Programacion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField(null=True)),
                ("nombre", models.CharField(max_length=30, null=True)),
                ("cedula", models.IntegerField()),
                ("modulo", models.CharField(max_length=30)),
                ("turnoReal", models.FloatField()),
                ("turnoLaborado", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Referencia",
            fields=[
                ("referencia", models.CharField(max_length=30)),
                ("color", models.CharField(max_length=30, null=True)),
                ("talla", models.CharField(max_length=30, null=True)),
                ("tipoPrenda", models.CharField(max_length=30, null=True)),
                ("SAM", models.FloatField()),
                ("SKU", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Usuarios",
            fields=[
                ("cedula", models.IntegerField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=30, null=True)),
                ("rol", models.CharField(max_length=30, null=True)),
                ("usuario", models.CharField(max_length=30, null=True)),
                ("password", models.CharField(max_length=30, null=True)),
            ],
        ),
    ]