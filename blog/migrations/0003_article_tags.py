# Generated by Django 4.1.7 on 2023-02-22 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_author_article_category_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.tag', verbose_name='#'),
        ),
    ]
