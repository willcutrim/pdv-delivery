# Generated by Django 3.1.5 on 2023-12-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatorioEntradaSaida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=150)),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Saida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saida_status', models.CharField(default='saida', max_length=120)),
                ('tipo_de_despesa', models.CharField(default='outras_despesas', max_length=150, verbose_name='Tipo de Despesa')),
                ('valor_despesa', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Valor da despesa')),
                ('data_saida', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Saida',
                'verbose_name_plural': 'Saidas',
            },
        ),
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_entrada', models.CharField(default='entrada', max_length=120)),
                ('valor_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('data_compra', models.DateTimeField(auto_now_add=True)),
                ('produtos', models.ManyToManyField(to='pdv.Produtos')),
            ],
        ),
    ]
