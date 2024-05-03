# Generated by Django 4.2.11 on 2024-05-02 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaManutencao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(choices=[('TVM', 'Trocar valvula de motor'), ('TO', 'Trocar de óleo'), ('BAL', 'Balanceamento'), ('ALI', 'Alinhamento')], max_length=3)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('data_incio', models.DateField(null=True)),
                ('data_entrega', models.DateField(null=True)),
                ('finalizado', models.BooleanField(default=False)),
                ('protocole', models.CharField(blank=True, max_length=32, null=True)),
                ('categoria_manutencao', models.ManyToManyField(to='servicos.categoriamanutencao')),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.cliente')),
            ],
        ),
    ]