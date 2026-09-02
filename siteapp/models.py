from django.db import models


"""
Class Category: Represents a category for courses or articles.
Attributes: name (str): The name of the category.

"""

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='formations')
    summary = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    duration = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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


class SEOSettings(models.Model):
    site_name = models.CharField(max_length=120, default='ASFEX Formation Tchad')
    homepage_title = models.CharField(max_length=160, default='ASFEX Formation Tchad | Centre de Formation & Expertise')
    meta_description = models.TextField(default='Centre de formation et expertise au Tchad pour des formations professionnelles, certification et accompagnement sur mesure.')
    meta_keywords = models.TextField(default='ASFEX Formation Tchad, formations professionnelles, certification, expertise, Tchad, N’Djamena')
    service_name = models.CharField(max_length=160, default='Formation professionnelle & conseil ASFEX')
    service_description = models.TextField(default='Formations professionnelles, conseil et accompagnement sur mesure pour entreprises, ONG et particuliers au Tchad.')
    canonical_url = models.URLField(default='https://www.asfex-formation-tchad.com/')
    focus_keyword = models.CharField(max_length=120, blank=True, default='formation professionnelle Tchad')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paramètres SEO'
        verbose_name_plural = 'Paramètres SEO'

    def __str__(self):
        return self.site_name
