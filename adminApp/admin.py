from django.contrib import admin
from .models import Template, Category, SubCategory

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'questions', 'content')
    list_filter = ['category']
    search_fields = ('name', 'questions', 'content')
    readonly_fields = ('questions', 'content')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

    def get_queryset(self, request):
        # Assuming 'sub_categories' is a reverse relation; use prefetch_related
        return super().get_queryset(request).prefetch_related('subcategory_set')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
