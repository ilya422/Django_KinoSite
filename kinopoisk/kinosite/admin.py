from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *

# region Inlines

class FilmCountryInline(admin.TabularInline):
    model = FilmCountriesAssociations
    extra = 1

class FilmGenresInline(admin.TabularInline):
    model = FilmGenresAssociations
    extra = 1

class FilmStaffInline(admin.TabularInline):
    model = FilmStaffAssociations
    extra = 1

class FilmPhotoInline(admin.TabularInline):
    model = FilmPhotos
    extra = 1
    fields = ('get_html_photo', 'image', 'type', 'is_main')
    readonly_fields = ('get_html_photo', )

    def get_html_photo(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=200>")
    get_html_photo.short_description = "Представление"


class FilmStaffPhotoInline(admin.TabularInline):
    model = FilmStaffPhotos
    extra = 1

# endregion

# region ModelAdmin

class BaseModelsAdmin(admin.ModelAdmin):
    """
        Админ панель базовых моделей
    """
    search_fields = ('name', )
    readonly_fields = ('created_at', 'updated_at')


class FilmsAdmin(BaseModelsAdmin):
    """
        Админ панель фильма
    """
    list_display = ('id', 'name', 'released_at', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    inlines = (FilmPhotoInline, FilmCountryInline, FilmGenresInline, FilmStaffInline)
    save_on_top = True


class FilmStaffAdmin(BaseModelsAdmin):
    """
        Админ панель работников над фильмом
    """
    list_display = ('id', 'full_name', 'birthday', 'created_at', 'updated_at')
    search_fields = ('full_name', )
    inlines = (FilmStaffPhotoInline, FilmStaffInline)
    save_on_top = True

# endregion

admin.site.register(Films, FilmsAdmin)
admin.site.register(FilmStaff, FilmStaffAdmin)
admin.site.register(FilmGenres, BaseModelsAdmin)
admin.site.register(Countries, BaseModelsAdmin)
admin.site.register(FilmPhotoTypes, BaseModelsAdmin)
admin.site.register(FilmStaffTypes, BaseModelsAdmin)

