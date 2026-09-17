from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0007_seosettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('resource_type', models.CharField(choices=[('article', 'Article'), ('tutoriel', 'Tutoriel'), ('conseil', 'Conseil pratique'), ('gratuite', 'Ressource gratuite'), ('actualite', 'Actualité ASFEX')], default='article', max_length=20)),
                ('excerpt', models.TextField(blank=True)),
                ('content', models.TextField()),
                ('files', models.FileField(blank=True, null=True, upload_to='resources/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
