from django.contrib import admin

# Register your models here.

from .models import portfolio_site, Author, Category, Post, PostView




admin.site.register(portfolio_site)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostView)
