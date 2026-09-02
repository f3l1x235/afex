from django import forms

from .models import Article, Category, ContactMessage, Course, SEOSettings


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
        }
        labels = {
            'name': 'Nom de la catégorie',
        }


class CourseForm(forms.ModelForm):
    price = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix de la formation', 'step': '0.01'}),
        label='Prix (en F CFA)',
    )

    class Meta:
        model = Course
        fields = ['name', 'category', 'summary', 'duration', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la formation'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. 2 jours / 3 semaines'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Résumé de la formation'}),
        }
        labels = {
            'name': 'Nom de la formation',
            'category': 'Catégorie',
            'summary': 'Résumé',
            'duration': 'Durée',
            'price': 'Prix (en F CFA)',
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'excerpt', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’article'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Extrait court'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Contenu complet'}),
        }
        labels = {
            'title': 'Titre de l’article',
            'excerpt': 'Extrait',
            'content': 'Contenu',
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message'}),
        }
        labels = {
            'name': 'Nom',
            'email': 'Email',
            'phone': 'Téléphone',
            'subject': 'Objet',
            'message': 'Message',
        }


class SEOForm(forms.ModelForm):
    class Meta:
        model = SEOSettings
        fields = ['site_name', 'homepage_title', 'meta_description', 'meta_keywords', 'canonical_url', 'focus_keyword']
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'homepage_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'meta_keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-control'}),
            'focus_keyword': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'site_name': 'Nom du site',
            'homepage_title': 'Titre de la page d’accueil',
            'meta_description': 'Meta description',
            'meta_keywords': 'Mots-clés',
            'canonical_url': 'URL canonique',
            'focus_keyword': 'Mot-clé principal',
        }
