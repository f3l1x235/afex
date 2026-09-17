from django import forms

from .models import Article, Category, ContactMessage, Course, CourseRegistration, Resource, SEOSettings, TrainingLevel, TrainingRequest


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
        fields = ['name', 'category', 'levels', 'summary', 'duration', 'price', 'start_date', 'end_date', 'modality', 'status', 'details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la formation'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'levels': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 4}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex. 2 jours / 3 semaines'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Résumé de la formation'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'modality': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Programme détaillé et objectifs'}),
        }
        labels = {
            'name': 'Nom de la formation',
            'category': 'Catégorie',
            'levels': 'Niveaux de formation',
            'summary': 'Résumé',
            'duration': 'Durée',
            'price': 'Prix (en F CFA)',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'modality': 'Modalité',
            'status': 'Statut',
            'details': 'Détails de la formation',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['levels'].queryset = TrainingLevel.objects.all()
        self.fields['levels'].help_text = 'Maintenez Ctrl (Windows) ou Cmd (Mac) pour sélectionner plusieurs niveaux.'
        for field_name in ['start_date', 'end_date', 'modality', 'status', 'details']:
            self.fields[field_name].required = False


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


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'resource_type', 'excerpt', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la ressource'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Extrait court'}),
            'files': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Contenu de la ressource'}),
        }
        labels = {
            'title': 'Titre',
            'resource_type': 'Type de ressource',
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


class TrainingRequestForm(forms.ModelForm):
    class Meta:
        model = TrainingRequest
        fields = ['name', 'email', 'phone', 'organization', 'participants', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entreprise ou organisation'}),
            'participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Nombre de participants'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Décrivez votre besoin'}),
        }
        labels = {
            'name': 'Nom complet', 'email': 'Email', 'phone': 'Téléphone',
            'organization': 'Entreprise / organisation', 'participants': 'Nombre de participants',
            'message': 'Votre besoin',
        }


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        fields = ['name', 'email', 'phone', 'organization', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entreprise ou organisation'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Question ou précision (facultatif)'}),
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
        fields = ['site_name', 'homepage_title', 'meta_description', 'canonical_url', 'focus_keyword']
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'homepage_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-control'}),
            'focus_keyword': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'site_name': 'Nom du site',
            'homepage_title': 'Titre de la page d’accueil',
            'meta_description': 'Description meta globale',
            'canonical_url': 'URL canonique',
            'focus_keyword': 'Mot-clé principal',
        }
