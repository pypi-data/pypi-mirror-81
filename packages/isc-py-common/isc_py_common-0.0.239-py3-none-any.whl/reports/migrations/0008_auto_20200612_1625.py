# Generated by Django 3.0.7 on 2020-06-12 16:25

from django.conf import settings
from django.db import migrations
import isc_common.fields.code_field


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0007_jasper_reports_users_editor_identifier'),
    ]

    operations = [
        migrations.RunSQL('delete from reports_jasper_reports_users'),
        migrations.AlterField(
            model_name='jasper_reports_users',
            name='editor_identifier',
            field=isc_common.fields.code_field.CodeStrictField(),
        ),
        migrations.AlterUniqueTogether(
            name='jasper_reports_users',
            unique_together={('report', 'user', 'editor_identifier')},
        ),
    ]
