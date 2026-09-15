from django.db import migrations, models
import django.db.models.deletion


def create_default_levels(apps, schema_editor):
    TrainingLevel = apps.get_model('siteapp', 'TrainingLevel')
    levels = [
        ('Débutant', 'debutant', 1),
        ('Intermédiaire', 'intermediaire', 2),
        ('Avancé', 'avance', 3),
        ('Expert', 'expert', 4),
    ]
    for name, slug, display_order in levels:
        TrainingLevel.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'display_order': display_order},
        )


def remove_default_levels(apps, schema_editor):
    TrainingLevel = apps.get_model('siteapp', 'TrainingLevel')
    TrainingLevel.objects.filter(slug__in=['debutant', 'intermediaire', 'avance', 'expert']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('siteapp', '0005_trainingrequest_course_details_course_end_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'niveau de formation',
                'verbose_name_plural': 'niveaux de formation',
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='levels',
            field=models.ManyToManyField(blank=True, related_name='formations', to='siteapp.traininglevel'),
        ),
        migrations.RunPython(create_default_levels, remove_default_levels),
    ]
