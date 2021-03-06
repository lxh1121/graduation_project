# Generated by Django 2.1.7 on 2019-03-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0003_auto_20190310_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='principal',
            name='vip_time',
            field=models.DateTimeField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, '待审核'), (1, '已发布'), (2, '未通过')], default=0),
        ),
    ]
