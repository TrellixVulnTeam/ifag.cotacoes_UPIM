# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 21:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ifag', '0004_auto_20170904_1826'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={
                'verbose_name': 'Histórico de Indicador',
                'verbose_name_plural': 'Históricos de Indicadores'
            },
        ),
        migrations.AlterModelOptions(
            name='quotation',
            options={
                'permissions': (('can_add_quotation', 'Add Quotation'),),
                'verbose_name': 'Cotação',
                'verbose_name_plural': 'Cotações'
            },
        ),
        migrations.AlterModelOptions(
            name='quotationapprove',
            options={
                'permissions': (
                    ('can_approve_quotation', 'Approve Quotation'),
                ),
                'verbose_name': 'cotação',
                'verbose_name_plural': 'aprovar cotações'
            },
        ),
    ]