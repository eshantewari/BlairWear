# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20151227_1917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothing',
            old_name='large',
            new_name='l',
        ),
    ]
