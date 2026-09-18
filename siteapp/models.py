from django.db import models


"""
Class Category: Represents a category for courses or articles.
Attributes: name (str): The name of the category.

"""

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class SEOSettings(models.Model):
    site_name = models.CharField(max_length=120, default='ASFEX Formation Tchad')
    homepage_title = models.CharField(max_length=160, default='ASFEX Formation Tchad | Centre de Formation & Expertise')
    meta_description = models.TextField(default='ASFEX Formation Tchad, centre de formation et expertise au Tchad pour des formations professionnelles et un accompagnement sur mesure.')
    canonical_url = models.URLField(default='https://www.asfex-formation-tchad.com/')
    focus_keyword = models.CharField(
        max_length=250,
        blank=True,
        default='Formation MEAL Tchad, cours suivi et évaluation N\'Djamena, gestion de projet humanitaire Tchad, automatisation de rapports statistiques'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'paramètres SEO'
        verbose_name_plural = 'paramètres SEO'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_current(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings


class TrainingLevel(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'niveau de formation'
        verbose_name_plural = 'niveaux de formation'

    def __str__(self):
        return self.name


class Course(models.Model):
    MODALITY_CHOICES = [
        ('presentiel', 'Présentiel'),
        ('en_ligne', 'En ligne'),
        ('hybride', 'Présentiel / En ligne'),
    ]
    STATUS_CHOICES = [
        ('inscriptions', 'Inscriptions ouvertes'),
        ('bientot', 'Bientôt disponible'),
        ('complet', 'Complet'),
        ('terminee', 'Formation terminée'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='formations')
    levels = models.ManyToManyField(TrainingLevel, blank=True, related_name='formations')
    summary = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    duration = models.CharField(max_length=50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    modality = models.CharField(max_length=20, choices=MODALITY_CHOICES, default='presentiel')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bientot')
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    partners = models.ManyToManyField(Partner, blank=True, related_name='formations')
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('tutoriel', 'Tutoriel'),
        ('conseil', 'Conseil pratique'),
        ('gratuite', 'Ressource gratuite'),
        ('actualite', 'Actualité ASFEX'),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='article')
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    src = models.FileField(upload_to='resources/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.subject or "Message"}'


class TrainingRequest(models.Model):
    REQUEST_TYPES = [
        ('devis', 'Demande de devis'),
        ('sur_mesure', 'Formation sur mesure'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    organization = models.CharField(max_length=150, blank=True)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    participants = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.get_request_type_display()}'


class CourseRegistration(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    organization = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.course.name}'


