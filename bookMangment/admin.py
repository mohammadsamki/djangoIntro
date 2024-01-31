from django.contrib import admin

# Register your models here.
from .models import *

class BookInstanceInline(admin.ModelAdmin):
    list_display = ('book', 'is_overdue', 'brower', 'due_back', 'id','loanPriceValue')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'brower', 'loanPrice')
        }),
    )

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(BookInstance, BookInstanceInline)
admin.site.register(Geneger)
# admin.py

from django.contrib import admin
from .models import Playlist

admin.site.register(Playlist)
