from .models import SEOSettings


def site_seo(request):
    seo_settings, created = SEOSettings.objects.get_or_create(pk=1)
    return {
        'site_seo': seo_settings,
    }
