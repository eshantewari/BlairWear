# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20151226_0313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothing',
            old_name='small',
            new_name='s',
        ),
    ]
