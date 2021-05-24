from django.contrib import admin
from .models import Site, Page, PageImages, ExceptedPages

admin.site.register(Site)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uri', 'site')
    list_filter = ('site',)
    list_display_links = ('id', 'title')
    list_per_page = 50

admin.site.register(Page, PageAdmin)

admin.site.register(PageImages)

class ExceptedPageAdmin(admin.ModelAdmin):
    list_display = ('id','uri', 'site')
    list_filter = ('site',)
    list_display_links = ('id', 'site')
    list_per_page = 50

admin.site.register(ExceptedPages, ExceptedPageAdmin)
