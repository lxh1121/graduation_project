# Generated by Django 2.1.7 on 2019-03-10 14:36

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('info', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('source', models.CharField(max_length=50, null=True)),
                ('digest', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='article/%Y%m%d/')),
                ('content', models.TextField()),
                ('view_count', models.PositiveSmallIntegerField(default=0)),
                ('votes_count', models.PositiveSmallIntegerField(default=0)),
                ('share_count', models.PositiveSmallIntegerField(default=0)),
                ('distribute_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '待审核中'), (1, '审核通过'), (2, '审核未通过')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='分享文章', max_length=20)),
                ('score', models.CharField(default='+50', max_length=10)),
                ('cost_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, unique=True)),
                ('content', models.CharField(default='0', max_length=200)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='society.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Consume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('tran_money', models.PositiveSmallIntegerField(default=0)),
                ('tran_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Corporate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('mass_code', models.CharField(default=0, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_mess', to='society.Article')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_messages', to='society.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('photo', models.ImageField(default='20181024/07.jpg', upload_to='%Y%m%d/')),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('info', models.CharField(default='本人很懒，什么都没留下', max_length=200)),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('money', models.PositiveSmallIntegerField(default=0)),
                ('vip', models.PositiveSmallIntegerField(choices=[(0, '普通用户'), (1, 'VIP 1'), (2, 'VIP 2'), (3, 'VIP 3')], default=0)),
                ('leave_count', models.PositiveSmallIntegerField(default=1)),
                ('stu_num', models.CharField(default=151210223, max_length=10)),
                ('user_code', models.CharField(default=0, max_length=10)),
                ('mass', models.CharField(max_length=100)),
                ('mass_code', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sharevote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yesno', models.PositiveSmallIntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arti_shares', to='society.Article')),
                ('pr_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stu_shares', to='society.Principal')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('photo', models.ImageField(default='20181024/07.jpg', upload_to='%Y%m%d/')),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('info', models.CharField(default='本人很懒，什么都没留下', max_length=200)),
                ('score', models.PositiveSmallIntegerField(default=0)),
                ('money', models.PositiveSmallIntegerField(default=0)),
                ('vip', models.PositiveSmallIntegerField(choices=[(0, '普通用户'), (1, 'VIP 1'), (2, 'VIP 2'), (3, 'VIP 3')], default=0)),
                ('leave_count', models.PositiveSmallIntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='pr_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='society.Principal'),
        ),
        migrations.AddField(
            model_name='consume',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumes', to='society.Principal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='pr_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stu_coms', to='society.Principal'),
        ),
        migrations.AddField(
            model_name='bill',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='society.Principal'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='society.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='pr_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='society.Principal'),
        ),
    ]
