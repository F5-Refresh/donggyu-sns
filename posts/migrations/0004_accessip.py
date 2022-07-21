# Generated by Django 4.0.6 on 2022-07-22 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_tags_post_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(max_length=200)),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'db_table': 'access_ip',
            },
        ),
    ]
