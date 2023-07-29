from django.contrib import admin
from .models import Author, Category,Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content",)
    prepopulated_fields = {"slug": ("title",)}  # new



admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post,PostAdmin)

# Register your models here.
