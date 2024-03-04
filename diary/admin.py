from django.contrib import admin
from .models import CreateDiary

class CreateDiaryAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(CreateDiary, CreateDiaryAdmin)
