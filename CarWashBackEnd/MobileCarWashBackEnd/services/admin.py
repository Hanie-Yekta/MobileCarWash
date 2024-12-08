from django.contrib import admin
from .models import Services, ServicePrice, Comment
import admin_thumbnails
# Register your models here.


class ServicePriceInline(admin.TabularInline):
    model = ServicePrice
    extra = 1

@admin_thumbnails.thumbnail('image')
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_thumbnail')
    inlines = [ServicePriceInline]

admin.site.register(Services, ServicesAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'created')

admin.site.register(Comment, CommentAdmin)

