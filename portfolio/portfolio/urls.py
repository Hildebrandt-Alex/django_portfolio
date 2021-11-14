"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import   portfolio_index, blog_index, blog_blog, blog_post, blog_search, post_create, blog_post_update, blog_post_delete, miREV_html


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portfolio_index),
    path('blog_index.html', blog_index),
    path('miREV.html', miREV_html),
    path('blog_blog/', blog_blog, name ='post-list'),
    path('blog_search/', blog_search, name='blog_search'),
    path('create/', post_create, name='post-create'),
    path('blog_post/<id>/', blog_post, name ='post-detail'),
    path('blog_post/<id>/update/', blog_post_update, name ='post-update'), # link from under the thumbnail for registered users
    path('blog_post/<id>/delete/', blog_post_delete, name ='post-delete'), # link from under the thumbnail for registered users
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
