# -*- coding: utf-8 -*-
# pylint: skip-file
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifag', '0001_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('default', models.BooleanField(help_text='Categoria principal nos formulários do sistema', verbose_name='padrão')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
            ],
            options={
                'verbose_name': 'Grupo de Indicador',
                'verbose_name_plural': 'Grupos de Indicadores',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, verbose_name='data')),
                ('value', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='valor')),
                ('create_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
            ],
            options={
                'verbose_name': 'Histórico de Indicador',
                'verbose_name_plural': 'Histórico de Indicadores',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='nome')),
                ('slug', models.SlugField(blank=True, help_text='Identificação única do indicador para as APIS', max_length=128, unique=True, verbose_name='permalink')),
                ('group_short_name', models.CharField(blank=True, help_text='Nome curto dentro do grupo. Ex: "0-12 Meses"', max_length=50, null=True, unique=True, verbose_name='abreviação')),
                ('group_order', models.SmallIntegerField(blank=True, null=True, verbose_name='ordem de apresentação')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.Category', verbose_name='Categoria')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ifag.Group', verbose_name='Grupo')),
            ],
            options={
                'verbose_name': 'Indicador Econômico',
                'verbose_name_plural': 'Indicadores Econômicos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, verbose_name='data')),
                ('value', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='valor')),
                ('create_on', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('approved', models.BooleanField(default=False, help_text='Se já foi aprovado pelo gerente', verbose_name='Aprovado?')),
                ('calculated', models.BooleanField(default=False, help_text='Se já gerou a média desta cotação', verbose_name='Calculado?')),
            ],
            options={
                'verbose_name': 'Cotação',
                'verbose_name_plural': 'Cotações',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='nome')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='observações')),
            ],
            options={
                'verbose_name': 'Fonte de Informação',
                'verbose_name_plural': 'Fontes de Informação',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SourceIndicatorCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Fonte/Indicador/Cidade',
                'verbose_name_plural': 'Fontes/Indicadores/Cidades',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nome')),
                ('symbol', models.CharField(max_length=9, verbose_name='símbolo')),
            ],
            options={
                'verbose_name': 'Unidade de Medida',
                'verbose_name_plural': 'Unidades de Medida',
            },
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name_ascii'], 'verbose_name': 'Cidade', 'verbose_name_plural': 'Cidades'},
        ),
        migrations.AddField(
            model_name='sourceindicatorcity',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_indicator', to='ifag.City', verbose_name='cidade'),
        ),
        migrations.AddField(
            model_name='sourceindicatorcity',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_indicator', to='ifag.Indicator', verbose_name='indicador'),
        ),
        migrations.AddField(
            model_name='sourceindicatorcity',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_indicator', to='ifag.Source', verbose_name='fonte'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.City'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.Indicator'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.Source'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.Unit', verbose_name='Unidade de Medida'),
        ),
        migrations.AddField(
            model_name='history',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.City'),
        ),
        migrations.AddField(
            model_name='history',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ifag.Indicator'),
        ),
        migrations.AlterUniqueTogether(
            name='sourceindicatorcity',
            unique_together=set([('source', 'indicator', 'city')]),
        ),
        migrations.AlterUniqueTogether(
            name='indicator',
            unique_together=set([('group', 'group_order')]),
        ),
    ]
