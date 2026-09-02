from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ArticleForm, CategoryForm, ContactMessageForm, CourseForm, SEOForm
from .models import Article, Category, ContactMessage, Course, SEOSettings


def custom_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Identifiants invalides ou droits d’administration insuffisants.')

    context = {
        'page_title': 'Connexion admin ASFEX',
        'meta_description': 'Connexion sécurisée à l’espace de gestion ASFEX.',
    }
    return render(request, 'admin/login.html', context)


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('custom_admin_login')


def home(request):
    courses = Course.objects.order_by('created_at')[:3]
    latest_articles = Article.objects.order_by('-created_at')[:3]
    context = {
        'page_title': 'ASFEX - Centre de Formation & Expertise',
        'meta_description': 'ASFEX - centre de formation et expertise au Tchad pour des formations professionnelles et un accompagnement sur mesure.',
        'meta_keywords': 'ASFEX, formations professionnelles, certification, expertise, Tchad, N’Djamena',
        'courses': courses,
        'articles': latest_articles,
    }
    return render(request, 'home.html', context)


def about(request):
    context = {
        'page_title': 'À propos d’ASFEX Formation Tchad',
        'meta_description': 'Découvrez l’histoire, la mission, la vision et la philosophie d’ASFEX Formation Tchad au Tchad.',
        'meta_keywords': 'ASFEX Tchad, mission, vision, expertise, formation professionnelle',
    }
    return render(request, 'about.html', context)


def courses(request):
    courses = Course.objects.order_by('name')
    context = {
        'page_title': 'Formations ASFEX | Programmes Professionnels',
        'meta_description': 'Explorez les formations professionnelles, expertises et programmes de renforcement de compétences proposés par ASFEX Formation Tchad.',
        'meta_keywords': 'formations ASFEX, programmes de formation, Excel, analyse de données, gestion de projet, Tchad',
        'courses': courses,
    }
    return render(request, 'courses.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
            )
            messages.success(request, 'Votre message a bien été envoyé. Nous vous répondrons rapidement.')
        return redirect('contact')

    context = {
        'page_title': 'Contact ASFEX Formation Tchad',
        'meta_description': 'Contactez ASFEX Formation Tchad pour une demande de formation, conseil, accompagnement ou projet personnalisé.',
        'meta_keywords': 'contact ASFEX Tchad, formation au Tchad, demande de devis, conseil',
    }
    return render(request, 'contact.html', context)


def articles(request):
    posts = Article.objects.order_by('-created_at')
    context = {
        'page_title': 'Actualités ASFEX Formation Tchad',
        'meta_description': 'Suivez les actualités, conseils et annonces de ASFEX Formation Tchad.',
        'meta_keywords': 'actualités ASFEX, blog formation, conseils, Tchad',
        'articles': posts,
    }
    return render(request, 'articles.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_dashboard(request):
    courses = Course.objects.order_by('-created_at')[:5]
    articles = Article.objects.order_by('-created_at')[:5]
    messages = ContactMessage.objects.order_by('-created_at')[:5]
    categories = Category.objects.order_by('name')[:5]
    context = {
        'page_title': 'Tableau de bord ASFEX',
        'meta_description': 'Espace d’administration ASFEX Formation Tchad pour gérer le site, les contenus et les ressources.',
        'meta_keywords': 'admin ASFEX, tableau de bord, gestion du site, ASFEX Formation Tchad',
        'courses': courses,
        'articles': articles,
        'messages': messages,
        'categories': categories,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_categories(request):
    categories = Category.objects.order_by('name')
    context = {
        'page_title': 'Gestion des catégories',
        'meta_description': 'Gérez les catégories de formations ASFEX depuis l’espace d’administration.',
        'categories': categories,
    }
    return render(request, 'admin/categories.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_category_new(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie ajoutée avec succès.')
            return redirect('admin_categories')
    else:
        form = CategoryForm()

    context = {
        'page_title': 'Ajouter une catégorie',
        'form': form,
        'form_title': 'Ajouter une catégorie',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_category_edit(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie mise à jour avec succès.')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'page_title': 'Modifier une catégorie',
        'form': form,
        'form_title': 'Modifier une catégorie',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    messages.success(request, 'Catégorie supprimée avec succès.')
    return redirect('admin_categories')


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_formations(request):
    courses = Course.objects.order_by('-created_at')
    context = {
        'page_title': 'Gestion des formations',
        'meta_description': 'Gérez les formations ASFEX depuis l’espace d’administration.',
        'courses': courses,
    }
    return render(request, 'admin/formations.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_formations_new(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation ajoutée avec succès.')
            return redirect('admin_formations')
    else:
        form = CourseForm()

    context = {
        'page_title': 'Ajouter une formation',
        'form': form,
        'form_title': 'Ajouter une formation',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_formation_edit(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation mise à jour avec succès.')
            return redirect('admin_formations')
    else:
        form = CourseForm(instance=course)

    context = {
        'page_title': 'Modifier une formation',
        'form': form,
        'form_title': 'Modifier une formation',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_formation_delete(request, pk):
    course = Course.objects.get(pk=pk)
    course.delete()
    messages.success(request, 'Formation supprimée avec succès.')
    return redirect('admin_formations')


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_articles(request):
    articles = Article.objects.order_by('-created_at')
    context = {
        'page_title': 'Gestion des actualités',
        'meta_description': 'Gérez les actualités et contenus éditoriaux ASFEX.',
        'articles': articles,
    }
    return render(request, 'admin/articles.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_articles_new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article ajouté avec succès.')
            return redirect('admin_articles')
    else:
        form = ArticleForm()

    context = {
        'page_title': 'Ajouter un article',
        'form': form,
        'form_title': 'Ajouter un article',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_article_edit(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article mis à jour avec succès.')
            return redirect('admin_articles')
    else:
        form = ArticleForm(instance=article)

    context = {
        'page_title': 'Modifier un article',
        'form': form,
        'form_title': 'Modifier un article',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_article_delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    messages.success(request, 'Article supprimé avec succès.')
    return redirect('admin_articles')


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_messages(request):
    messages_list = ContactMessage.objects.order_by('-created_at')
    context = {
        'page_title': 'Messages reçus',
        'meta_description': 'Consultez les demandes, demandes de devis et messages reçus.',
        'messages': messages_list,
    }
    return render(request, 'admin/messages.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_messages_new(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message enregistré avec succès.')
            return redirect('admin_messages')
    else:
        form = ContactMessageForm()

    context = {
        'page_title': 'Ajouter un message',
        'form': form,
        'form_title': 'Nouveau message',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_message_edit(request, pk):
    message = ContactMessage.objects.get(pk=pk)
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message mis à jour avec succès.')
            return redirect('admin_messages')
    else:
        form = ContactMessageForm(instance=message)

    context = {
        'page_title': 'Modifier un message',
        'form': form,
        'form_title': 'Modifier un message',
    }
    return render(request, 'admin/form_editor.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_message_delete(request, pk):
    message = ContactMessage.objects.get(pk=pk)
    message.delete()
    messages.success(request, 'Message supprimé avec succès.')
    return redirect('admin_messages')


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_seo(request):
    seo_settings, created = SEOSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = SEOForm(request.POST, instance=seo_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Les paramètres SEO ont été enregistrés avec succès.')
            return redirect('admin_seo')
    else:
        form = SEOForm(instance=seo_settings)

    context = {
        'page_title': 'SEO / Référencement',
        'meta_description': 'Gérez les paramètres SEO et la visibilité du site ASFEX.',
        'form': form,
    }
    return render(request, 'admin/seo.html', context)


@login_required(login_url='/gestion/login/')
def user_profile(request):
    user = request.user
    User = get_user_model()

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        password = request.POST.get('password') or ''

        if not username:
            messages.error(request, 'Le nom d’utilisateur est obligatoire.')
        else:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                messages.error(request, 'Ce nom d’utilisateur est déjà utilisé.')
            else:
                user.username = username
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                if password:
                    user.set_password(password)
                    user.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')
                return redirect('user_profile')

    context = {
        'page_title': 'Mon profil',
        'meta_description': 'Mettez à jour vos informations personnelles et votre mot de passe ASFEX.',
        'user': user,
    }
    return render(request, 'admin/profile.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_accounts(request):
    if not request.user.is_superuser:
        messages.error(request, 'Vous devez être Superadmin pour gérer les comptes et les rôles.')
        return redirect('admin_dashboard')

    for role_name in ['Superadmin', 'Gestionnaire', 'Support']:
        Group.objects.get_or_create(name=role_name)

    User = get_user_model()
    users = User.objects.filter(is_staff=True).prefetch_related('groups').order_by('username')
    groups = Group.objects.order_by('name')

    context = {
        'page_title': 'Gestion des comptes et rôles',
        'meta_description': 'Gérez les comptes d’administration, leurs rôles et leurs permissions ASFEX.',
        'users': users,
        'groups': groups,
    }
    return render(request, 'admin/accounts.html', context)


@login_required(login_url='/gestion/login/')
@staff_member_required
def admin_account_new(request):
    if not request.user.is_superuser:
        messages.error(request, 'Seuls les Superadmins peuvent créer des comptes d’administration.')
        return redirect('admin_accounts')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''
        role = request.POST.get('role') or 'Gestionnaire'

        if not username or not password:
            messages.error(request, 'Le nom d’utilisateur et le mot de passe sont obligatoires.')
        else:
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ce nom d’utilisateur existe déjà.')
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.is_staff = True
                    user.save()
                    if role:
                        group, _ = Group.objects.get_or_create(name=role)
                        user.groups.add(group)
                    messages.success(request, f'Compte administrateur {username} créé avec succès.')
                    return redirect('admin_accounts')
                except ValidationError as exc:
                    messages.error(request, str(exc))

    groups = Group.objects.order_by('name')
    context = {
        'page_title': 'Créer un compte admin',
        'meta_description': 'Créer un nouveau compte administrateur ASFEX avec son rôle associé.',
        'groups': groups,
    }
    return render(request, 'admin/account_form.html', context)


def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nAllow: /\nSitemap: https://www.asfex-formation-tchad.com/sitemap.xml\n",
        content_type='text/plain',
    )


def sitemap_xml(request):
    sitemap = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url>
    <loc>https://www.asfex-formation-tchad.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.asfex-formation-tchad.com/a-propos/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.asfex-formation-tchad.com/formations/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.asfex-formation-tchad.com/contact/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  <url>
    <loc>https://www.asfex-formation-tchad.com/actualites/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
"""
    return HttpResponse(sitemap, content_type='application/xml')
