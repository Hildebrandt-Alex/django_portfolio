from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# portfolio_index site

class portfolio_site(models.Model):
    user = models.CharField(max_length=30)
    qualifications = models.CharField(max_length=100)
    user_picture_1 = models.ImageField()
    user_picture_2 = models.ImageField()
    heading_1 = models.TextField()
    introduction = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # save time when modified
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

## blog_site

User = get_user_model()



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class PostView(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Post(models.Model):
    title = models.CharField(max_length=100)
    overview=models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    #comment_count = models.IntegerField(default=0)
    #view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })
