# Generated by Django 2.0 on 2017-12-26 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_addressinfo_addnow'),
        ('dailyfresh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gcount', models.IntegerField(verbose_name='商品数量')),
                ('goods', models.ForeignKey(on_delete=False, to='dailyfresh.GoodInfo', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=True, to='df_user.UserInfo', verbose_name='购买用户')),
            ],
        ),
    ]