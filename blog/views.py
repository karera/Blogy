from django.db.models import Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404,redirect
from django.utils.text import slugify
from .models import Post,Author
from django.contrib import messages
from .forms import *




def get_category_count():
    queryset  = Post.objects.values('categories__name').annotate(Count('categories__name'))
    return queryset


def home (request):
    featured = Post.objects.filter(featured = True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'posts':featured,
        'latest':latest
    }
    return render(request, 'blog/index.html',context)

def about (request):
    return render(request, 'blog/about.html')

def blogging (request):
    category_count = get_category_count()
    rook = Post.objects.all().order_by('-timestamp')
    latest = Post.objects.order_by('-timestamp')[0:3]
    popular_post = Post.objects.order_by('-timestamp')[0:3]
    paginator=Paginator(rook,3)
    page = request.GET.get('page',1)

    try:
        rooks = paginator.page(page)
    except PageNotAnInteger:
        rooks = paginator.page(1)
    except EmptyPage:
        # page = paginator.num_pages
        rooks = paginator.page(paginator.num_pages)
   
    context = {
        'rooks' : rooks,
        'latest':latest,
        'paginator':paginator,
        'popular_post':popular_post,
        'category_count':category_count
    }
    return render(request, 'blog/blogging.html',context)

def contact (request):
    return render(request, 'blog/contact.html')

def category (request):
    return render(request, 'blog/category.html')

def single (request, slug):
    detail = get_object_or_404(Post,slug=slug) 
    context = {
        'detail':detail
    }
    return render(request,'blog/single.html',context)   



def new_post(request):
    profile = request.user.author
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.author = profile
            post.save()
            messages.info(request,'Article created successfully')
            return redirect('new_post')
        else:
            messages.error(request,'Article not created')
    else:
        form = PostForm()
    return render(request, "blog/new_post.html", {'form': form})

def updatePost(request,slug):
    post = Post.objects.get(slug = slug)
    form =PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            # post.slug = slugify(post.title)
            form.save()
            messages.info(request,'Article updated successfully')
            return redirect('blog-blogging')
    return render(request, "blog/new_post.html", {'form': form})

def deletePost(request,slug):
    post = Post.objects.get(slug = slug)
    form =PostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        messages.info(request,'Article Deleted successfully')
        return redirect ('blog-blogging')
        # messages.success(request,"Your Blog has been deleted successfully")
    context = {'form': form}
    return render( request,'blog/confirm_delete.html',context)

 

def login(request):
    return render(request,'blog/login.html')