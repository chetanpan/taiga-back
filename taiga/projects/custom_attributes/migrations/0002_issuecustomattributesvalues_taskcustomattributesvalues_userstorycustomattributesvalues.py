# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20150114_0954'),
        ('projects', '0015_auto_20141230_1212'),
        ('userstories', '0009_remove_userstory_is_archived'),
        ('issues', '0004_auto_20150114_0954'),
        ('custom_attributes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueCustomAttributesValues',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('values', django_pgjson.fields.JsonField(default={}, verbose_name='values')),
                ('issue', models.OneToOneField(related_name='custom_attributes_values', to='issues.Issue', verbose_name='issue')),
                ('project', models.ForeignKey(related_name='issuecustomattributesvalues', to='projects.Project', verbose_name='project')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'issue custom attributes values',
                'verbose_name': 'issue ustom attributes values',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskCustomAttributesValues',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('values', django_pgjson.fields.JsonField(default={}, verbose_name='values')),
                ('project', models.ForeignKey(related_name='taskcustomattributesvalues', to='projects.Project', verbose_name='project')),
                ('task', models.OneToOneField(related_name='custom_attributes_values', to='tasks.Task', verbose_name='task')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'task custom attributes values',
                'verbose_name': 'task ustom attributes values',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserStoryCustomAttributesValues',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=1, verbose_name='version')),
                ('values', django_pgjson.fields.JsonField(default={}, verbose_name='values')),
                ('project', models.ForeignKey(related_name='userstorycustomattributesvalues', to='projects.Project', verbose_name='project')),
                ('user_story', models.OneToOneField(related_name='custom_attributes_values', to='userstories.UserStory', verbose_name='user story')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'user story custom attributes values',
                'verbose_name': 'user story ustom attributes values',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
