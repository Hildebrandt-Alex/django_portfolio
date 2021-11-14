from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import  PostForm
from .models import Post, Author, PostView, portfolio_site
from marketing.models import Signup


def miREV_html(request):
    return render(request, 'miREV.html')


## views for blog site

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def blog_search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset' : queryset
    }
    return render(request, 'blog_search_results.html', context)




# sidebar count widget for categories
def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

def portfolio_index(request):
    home = portfolio_site.objects.latest('updated')
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'home': home,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
    }
    return render(request, 'portfolio_index.html', context)

def blog_index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except:
        paginated_queryset = paginator.page(paginator.num_pages)


    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
    }
    return render(request, 'blog_index.html', context)

def blog_blog(request):
    category_count = get_category_count() # calls the function defined above
    #print(category_count) # prints the result in the terminal
    most_recent = Post.objects.order_by('-timestamp')[0:4]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except:
        paginated_queryset = paginator.page(paginator.num_pages)


    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count' : category_count
    }
    return render(request, 'blog_blog.html', context)

def blog_post(request, id):
    category_count = get_category_count() # calls the function defined above
    most_recent = Post.objects.order_by('-timestamp')[0:4]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
            PostView.objects.get_or_create(user=request.user, post=post)

    context = {
        'post' : post,
        'most_recent': most_recent,
        'category_count' : category_count
    }
    return render(request, 'blog_post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog_post_create.html", context)

def blog_post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog_post_create.html", context)

def blog_post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))
