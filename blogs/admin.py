from django.contrib import admin
from .models import Category, Blog, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_at', 'updated_at')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category__category_name', 'status')
    list_editable = ('is_featured', 'status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Editor').exists() or request.user.groups.filter(name='Manager').exists():
            return qs
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if change == False:
            obj.author = request.user
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
