from django.contrib import admin

from .models import Article, ContactMessage, Course, CourseRegistration, SEOSettings, TrainingLevel, TrainingRequest


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Référencement global', {'fields': ('site_name', 'homepage_title', 'meta_description', 'canonical_url', 'focus_keyword')}),
    )

    def has_add_permission(self, request):
        return not SEOSettings.objects.exists()


@admin.register(TrainingLevel)
class TrainingLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration', 'created_at')
    search_fields = ('name', 'category', 'summary')
    list_filter = ('category',)
    filter_horizontal = ('levels',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    list_filter = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(TrainingRequest)
class TrainingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'request_type', 'organization', 'created_at')
    search_fields = ('name', 'email', 'organization', 'message')
    list_filter = ('request_type', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'organization', 'created_at')
    search_fields = ('name', 'email', 'organization', 'course__name')
    list_filter = ('course', 'created_at')
    readonly_fields = ('created_at',)
