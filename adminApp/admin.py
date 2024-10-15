from django.contrib import admin
from .models import Template, Category

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'questions', 'content')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_categories')
