from django.contrib import admin
#from import_export import resources
#from import_export.admin import ImportExportModelAdmin
from .read_chrono_file import start_reading_files, stop_reading_files

from .models import Tag, Competitor, Result, Race, ChronoFile, RoutePoint

admin.site.site_header = "RaceIT Admin"
admin.site.site_title = "RaceIT Admin Portal"
admin.site.index_title = "Welcome to RaceIT Portal"


class ResultInline(admin.StackedInline):
    model = Result


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'bib_number']


class ResultAdmin(admin.ModelAdmin):
    list_display = ['point', 'tag', 'gun_time']


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ['tag', 'name', 'surname', 'city', 'team', 'race']
    search_fields = ['tag__bib_number', 'name', 'surname']
    inlines = [ResultInline]


class ChronoFileAdmin(admin.ModelAdmin):
    list_display = ['point', 'file_type', 'chrono_file_path', 'reading_flag']
    actions = ['start_reading_file', 'stop_reading_file']

    def start_reading_file(self, request, queryset):
        start_reading_files(queryset)

    def stop_reading_file(self, request, queryset):
        stop_reading_files(queryset)

    start_reading_file.short_description = 'Start reading from file'
    stop_reading_file.short_description = 'Stop reading from file'


admin.site.register(Tag, TagAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Race)
admin.site.register(ChronoFile, ChronoFileAdmin)
admin.site.register(RoutePoint)
admin.site.register(Result, ResultAdmin)