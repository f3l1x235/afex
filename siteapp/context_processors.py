from .models import SEOSettings


def seo_settings(request):
    return {'seo_settings': SEOSettings.get_current()}