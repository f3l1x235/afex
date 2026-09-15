from django.db import migrations, models


def create_default_seo(apps, schema_editor):
    SEOSettings = apps.get_model('siteapp', 'SEOSettings')
    SEOSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'ASFEX Formation Tchad',
            'homepage_title': 'ASFEX Formation Tchad | Centre de Formation & Expertise',
            'meta_description': 'ASFEX Formation Tchad, centre de formation et expertise au Tchad pour des formations professionnelles et un accompagnement sur mesure.',
            'canonical_url': 'https://www.asfex-formation-tchad.com/',
            'focus_keyword': 'formation professionnelle Tchad',
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('siteapp', '0006_traininglevel_course_levels'),
    ]

    operations = [
        migrations.CreateModel(
            name='SEOSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='ASFEX Formation Tchad', max_length=120)),
                ('homepage_title', models.CharField(default='ASFEX Formation Tchad | Centre de Formation & Expertise', max_length=160)),
                ('meta_description', models.TextField(default='ASFEX Formation Tchad, centre de formation et expertise au Tchad pour des formations professionnelles et un accompagnement sur mesure.')),
                ('canonical_url', models.URLField(default='https://www.asfex-formation-tchad.com/')),
                ('focus_keyword', models.CharField(blank=True, default='formation professionnelle Tchad', max_length=120)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'paramètres SEO',
                'verbose_name_plural': 'paramètres SEO',
            },
        ),
        migrations.RunPython(create_default_seo, migrations.RunPython.noop),
    ]
