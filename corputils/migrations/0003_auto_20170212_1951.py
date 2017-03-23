# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 19:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corputils', '0002_migrate_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corpstats',
            options={'permissions': (('corp_apis', 'Can view API keys of members of their corporation.'), ('alliance_apis', 'Can view API keys of members of their alliance.'), ('blue_apis', 'Can view API keys of members of blue corporations.'), ('view_corp_corpstats', 'Can view corp stats of their corporation.'), ('view_alliance_corpstats', 'Can view corp stats of members of their alliance.'), ('view_blue_corpstats', 'Can view corp stats of blue corporations.')), 'verbose_name': 'corp stats', 'verbose_name_plural': 'corp stats'},
        ),
    ]
