from django.contrib import admin
from .models import Author, Category,Post,Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content",)
    prepopulated_fields = {"slug": ("title",)}  # new
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')



admin.site.register(Author)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)

# Register your models here.
