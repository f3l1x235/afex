from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from .models import Article, Category, ContactMessage, Course, CourseRegistration, TrainingLevel, TrainingRequest


class SeoAndAdminAccessTests(TestCase):
    def test_public_pages_have_seo_metadata(self):
        for path in ['/', '/a-propos/', '/formations/', '/contact/', '/actualites/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'meta name="description"')

    def test_contact_form_submits_and_saves_message(self):
        response = self.client.post('/contact/', {
            'name': 'Amine',
            'email': 'amine@example.com',
            'phone': '+235 60 00 00 00',
            'subject': 'Demande de formation',
            'message': 'Je souhaite organiser une formation pour mon équipe.'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/contact/'))
        self.assertEqual(1, len(__import__('siteapp.models', fromlist=['ContactMessage']).ContactMessage.objects.all()))

    def test_home_message_is_saved_and_visible_in_management(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Écrivez-nous directement')

        response = self.client.post('/', {
            'name': 'Mariam',
            'email': 'mariam@example.com',
            'phone': '+235 60 00 00 02',
            'subject': 'Question depuis l’accueil',
            'message': 'Je souhaite en savoir plus sur vos formations.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(name='Mariam').exists())

        User = get_user_model()
        user = User.objects.create_user(username='messagesadmin', password='secret123', is_staff=True)
        self.client.force_login(user)
        response = self.client.get('/gestion/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mariam')
        self.assertContains(response, 'Question depuis l’accueil')

    def test_training_calendar_detail_and_requests_work(self):
        category = Category.objects.create(name='Bureautique')
        course = Course.objects.create(
            name='Excel avancé', category=category, summary='Perfectionnez vos tableaux.',
            duration='20 h', price=25000, modality='presentiel', status='inscriptions',
        )

        response = self.client.get('/formations/calendrier/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Excel avancé')
        self.assertContains(response, 'Inscriptions ouvertes')

        response = self.client.get(f'/formations/{course.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'S’inscrire à cette formation')

        response = self.client.post(f'/formations/{course.pk}/', {
            'name': 'Moussa', 'email': 'moussa@example.com', 'phone': '+235 60 00 00 00',
            'organization': 'ASFEX', 'message': 'Je souhaite participer.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CourseRegistration.objects.filter(course=course, name='Moussa').exists())

        request_data = {
            'name': 'Amina', 'email': 'amina@example.com', 'phone': '+235 66 00 00 00',
            'organization': 'Entreprise test', 'participants': 8, 'message': 'Besoin d’un devis.',
        }
        response = self.client.post('/demande-devis/', request_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TrainingRequest.objects.filter(request_type='devis', name='Amina').exists())

        response = self.client.post('/formation-sur-mesure/', request_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TrainingRequest.objects.filter(request_type='sur_mesure', name='Amina').exists())

    def test_course_supports_multiple_training_levels(self):
        category = Category.objects.create(name='Informatique')
        beginner = TrainingLevel.objects.create(name='Débutant test', slug='debutant-test', display_order=1)
        advanced = TrainingLevel.objects.create(name='Avancé test', slug='avance-test', display_order=2)
        course = Course.objects.create(
            name='Excel multi-niveaux', category=category, summary='Formation progressive.', duration='20 h'
        )
        course.levels.set([beginner, advanced])

        self.assertEqual(list(course.levels.values_list('name', flat=True)), ['Débutant test', 'Avancé test'])
        response = self.client.get('/formations/')
        self.assertContains(response, 'Débutant test')
        self.assertContains(response, 'Avancé test')

        response = self.client.get('/gestion/formations/nouveau/')
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_requires_login(self):
        response = self.client.get('/gestion/')
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_shows_content_summary(self):
        User = get_user_model()
        user = User.objects.create_user(username='manager', password='secret123')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        category = Category.objects.create(name='Informatique')
        Course.objects.create(name='Excel Avancé', category=category, summary='Formation Excel.', duration='2 jours')
        Article.objects.create(title='Nouvelle formation', excerpt='Nouveau programme', content='Contenu test')
        ContactMessage.objects.create(name='Amina', email='amina@example.com', subject='Formation', message='Bonjour')

        self.client.force_login(user)
        response = self.client.get('/gestion/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Excel Avancé')
        self.assertContains(response, 'Nouvelle formation')
        self.assertContains(response, 'Amina')

    def test_custom_management_login_replaces_django_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/gestion/'))

        response = self.client.get('/gestion/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connexion admin')

    def test_superadmin_can_access_role_management(self):
        User = get_user_model()
        user = User.objects.create_user(username='superadmin', password='secret123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        group, _ = Group.objects.get_or_create(name='Superadmin')
        user.groups.add(group)
        self.client.force_login(user)

        response = self.client.get('/gestion/comptes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Superadmin')

    def test_superadmin_can_create_staff_user_with_role(self):
        User = get_user_model()
        user = User.objects.create_user(username='superadmin2', password='secret123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        response = self.client.post('/gestion/comptes/nouveau/', {
            'username': 'gestionnaire01',
            'email': 'gestionnaire@example.com',
            'password': 'secret456',
            'role': 'Gestionnaire',
        })

        self.assertEqual(response.status_code, 302)
        created = User.objects.get(username='gestionnaire01')
        self.assertTrue(created.is_staff)
        self.assertTrue(created.groups.filter(name='Gestionnaire').exists())

    def test_user_profile_page_allows_profile_update(self):
        User = get_user_model()
        user = User.objects.create_user(username='profileuser', email='profile@example.com', password='secret123')
        user.is_staff = True
        user.first_name = 'Jean'
        user.last_name = 'Dupont'
        user.save()
        self.client.force_login(user)

        response = self.client.get('/gestion/profil/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mon profil')

        response = self.client.post('/gestion/profil/', {
            'username': 'profileuser',
            'email': 'newprofile@example.com',
            'first_name': 'Jean-Pierre',
            'last_name': 'Martin',
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Jean-Pierre')
        self.assertEqual(user.last_name, 'Martin')
        self.assertEqual(user.email, 'newprofile@example.com')

    def test_management_pages_and_creation_forms_work(self):
        User = get_user_model()
        user = User.objects.create_user(username='admin', password='secret123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        response = self.client.get('/gestion/formations/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ajouter une formation')

        response = self.client.get('/gestion/actualites/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ajouter un article')

        response = self.client.get('/gestion/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Messages reçus')

        response = self.client.get('/gestion/seo/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SEO / Référencement')

        category = Category.objects.create(name='Business Intelligence')
        response = self.client.post('/gestion/formations/nouveau/', {
            'name': 'Power BI Avancé',
            'category': category.pk,
            'summary': 'Formation complète',
            'duration': '3 jours',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, Course.objects.filter(name='Power BI Avancé').count())

        response = self.client.post('/gestion/actualites/nouveau/', {
            'title': 'Nouvel atelier ASFEX',
            'excerpt': 'Résumé de l’atelier',
            'content': 'Contenu complet de l’atelier',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, Article.objects.filter(title='Nouvel atelier ASFEX').count())

        response = self.client.post('/gestion/messages/nouveau/', {
            'name': 'Brahim',
            'email': 'brahim@example.com',
            'phone': '+235 60 00 00 01',
            'subject': 'Demande de devis',
            'message': 'Bonjour, nous voulons une formation.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, ContactMessage.objects.filter(name='Brahim').count())

    def test_admin_can_view_training_requests_and_registrations(self):
        User = get_user_model()
        user = User.objects.create_user(username='leadsadmin', password='secret123')
        user.is_staff = True
        user.save()

        category = Category.objects.create(name='Data')
        course = Course.objects.create(
            name='Power BI', category=category, summary='Analysez vos données.', duration='3 jours'
        )
        TrainingRequest.objects.create(
            name='Nadia', email='nadia@example.com', request_type='devis',
            organization='Entreprise Tchad', participants=12, message='Un devis, merci.',
        )
        CourseRegistration.objects.create(
            course=course, name='Ali', email='ali@example.com', organization='Cabinet Ali',
        )

        self.client.force_login(user)
        response = self.client.get('/gestion/demandes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nadia')
        self.assertContains(response, 'Ali')
        self.assertContains(response, 'Power BI')

        response = self.client.get('/gestion/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Demandes récentes')
        self.assertContains(response, 'Inscriptions récentes')

    def test_admin_can_edit_and_delete_records(self):
        User = get_user_model()
        user = User.objects.create_user(username='manager2', password='secret123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        category = Category.objects.create(name='Bureautique')
        course = Course.objects.create(name='Excel', category=category, summary='Initial', duration='2 jours')
        article = Article.objects.create(title='Premier article', excerpt='Extrait', content='Contenu')
        message = ContactMessage.objects.create(name='Awa', email='awa@example.com', subject='Question', message='Bonjour')

        response = self.client.get(f'/gestion/formations/{course.pk}/modifier/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/gestion/formations/{course.pk}/modifier/', {
            'name': 'Excel Pro',
            'category': category.pk,
            'summary': 'Formation mise à jour',
            'duration': '3 jours',
        })
        self.assertEqual(response.status_code, 302)
        course.refresh_from_db(); self.assertEqual(course.name, 'Excel Pro')

        response = self.client.get(f'/gestion/actualites/{article.pk}/modifier/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/gestion/actualites/{article.pk}/modifier/', {
            'title': 'Article mis à jour',
            'excerpt': 'Nouveau résumé',
            'content': 'Nouveau contenu',
        })
        self.assertEqual(response.status_code, 302)
        article.refresh_from_db(); self.assertEqual(article.title, 'Article mis à jour')

        response = self.client.get(f'/gestion/messages/{message.pk}/modifier/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(f'/gestion/messages/{message.pk}/modifier/', {
            'name': 'Awa S.',
            'email': 'awa@example.com',
            'phone': '+235 66 66 66 66',
            'subject': 'Réponse',
            'message': 'Nous avons reçu votre demande.',
        })
        self.assertEqual(response.status_code, 302)
        message.refresh_from_db(); self.assertEqual(message.name, 'Awa S.')

        response = self.client.post(f'/gestion/formations/{course.pk}/supprimer/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Course.objects.filter(pk=course.pk).exists())

        response = self.client.post(f'/gestion/actualites/{article.pk}/supprimer/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())

        response = self.client.post(f'/gestion/messages/{message.pk}/supprimer/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ContactMessage.objects.filter(pk=message.pk).exists())

    def test_category_management_crud_works(self):
        User = get_user_model()
        user = User.objects.create_user(username='catadmin', password='secret123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        response = self.client.get('/gestion/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ajouter une catégorie')

        response = self.client.post('/gestion/categories/nouveau/', {'name': 'Business Intelligence'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Business Intelligence').exists())

        category = Category.objects.get(name='Business Intelligence')

        response = self.client.get(f'/gestion/categories/{category.pk}/modifier/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(f'/gestion/categories/{category.pk}/modifier/', {'name': 'Data Analytics'})
        self.assertEqual(response.status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Data Analytics')

        response = self.client.post(f'/gestion/categories/{category.pk}/supprimer/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())
