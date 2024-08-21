from django.contrib import admin
from BookApp.models import BookModel


# Register your models here.
class BookModelAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "price")


admin.site.register(BookModel, BookModelAdmin)
