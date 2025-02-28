from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, PostForm, CategoryForm, SubscribeForm
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from core.models import Blog, Category, RequestCount
from django.db import IntegrityError


# Create your views here.

def home(request):
    mains = Blog.objects.filter(type="Main").order_by('-created_at')[:3]
    ordinary = Blog.objects.filter(type="Ordinary").order_by('-created_at')[:6]
    featured = Blog.objects.filter(type="Featured").order_by('-created_at')[:2]
    featured2 = Blog.objects.filter(type="Featured").order_by('-created_at')[2:6]
    allPosts = Blog.objects.all().order_by('-created_at')#[6:]
    active_styler = 'rd-nav-item active'
    paginator = Paginator(allPosts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'core/home.html',  {'mains':mains, 
                                               'featured':featured, 
                                               'ordinary':ordinary, 
                                               'featured2':featured2, 
                                               'posts': posts, 
                                               'activestyler':active_styler})
   
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account Created for {email}, you can now login')
            html_template = 'core/welcomemail.html'
            html_message = render_to_string(html_template)
            subject = 'Welcome to Testprep!'
            email_from = 'Testprep@testprepken.com'
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send(fail_silently=True)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form':form})



@login_required
def profile(request):
    return render(request, 'core/profile.html')


def about(request):
    return render(request, 'core/about.html')

def contactus(request):
    return render(request, 'core/contactus.html')


def mailtest1(request):
    send_mail('Using SparkPost with Django123', 'This is a message from Django using SparkPost!123', 'Testprep@testprepken.com',
    ['reuben.omanyala22@gmail.com'], fail_silently=True)
    return render(request, 'core/about.html')


def welcomemail(request):
    return render(request, 'core/welcomemail.html')

@login_required
def post(request):
    cats = Category.objects.all()
    if not cats:
        messages.success(request, f'Create At Least One Category To Be Able to Make Posts')
        return redirect('category-create')
    else:
        form = PostForm()
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect('post-detail', obj.slug, obj.id)
            else:
                form = PostForm()
            return render(request, 'core/post.html', {'form':form, })
        else:
            return render(request, 'core/post.html', {'form':form, 'cats':cats})
    

def post_detail(request, id, slug):
    post = Blog.objects.get(slug=slug, id=id)
    return render(request, 'core/post-detail.html', {'post':post, })


@login_required
def post_update(request, id, slug):
     post = Blog.objects.get(id=id, slug=slug)
     if request.method == 'POST':
         form = PostForm(request.POST, request.FILES, instance=post)
         if form.is_valid():
             #obj = form.save(commit=False)
             form.save()
             return redirect('post-detail', post.slug, post.id) 
     else:
         form = PostForm(instance=post)
     return render(request, 'core/post.html',  {'form': form})

    

def post_detail(request, id, slug):
    post = Blog.objects.get(slug=slug, id=id)
    related = Blog.objects.filter(category=post.category).exclude(id=post.id).order_by('-created_at')[:9]
    return render(request, 'core/post-detail.html', {'post':post, 'related':related })



@login_required
def categoryCreate(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            category = form.cleaned_data.get('title')
            obj.save()
            messages.success(request, f'New Category -- {category} -- Successfully Created')
            return redirect('post')
        else:
            form = CategoryForm()
        return render(request, 'core/category.html', {'form':form, })
    else:
        return render(request, 'core/category.html', {'form':form, })
    

@login_required
def category_update(request, id, slug):
     category = Category.objects.get(id=id, slug=slug)
     if request.method == 'POST':
         form = CategoryForm(request.POST, request.FILES, instance=category)
         if form.is_valid():
             form.save()
             return redirect('categories') 
     else:
         form = CategoryForm(instance=category)
     return render(request, 'core/category.html',  {'form': form})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'core/category-list.html',  {'categories': categories})


def categoryPosts(request, id, slug):
    cat = Category.objects.get(id=id, slug=slug)
    categoryPosts = Blog.objects.filter(category=cat.id).order_by('-created_at')[:20]
    #categoryPosts = Blog.objects.all()
    active_styler = 'rd-nav-item active'
    return render(request, 'core/category-posts.html', {'categoryPosts': categoryPosts, 'activestyler2':active_styler })


@login_required
def delete_post(request, id):
    # Fetch the object or return a 404 if it does not exist
    obj = Blog.objects.filter(id=id)
    obj.delete()
    messages.success(request, f'Post Successfully Deleted')
    return redirect('home') 

@login_required
def adminDashBoard(request):
    count = RequestCount.objects.first()
    count = count.count
    return render(request, 'core/admin-dashboard.html', {'count': count})



def search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        results = Blog.objects.filter(Q(title__icontains=query) | Q(main__icontains=query))
        results = results.order_by('-created_at')[:10]
    else:
        results = None #if query else Blog.objects.all()

    return render(request, 'core/search.html', {'results': results, 'query': query})



def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "You have successfully subscribed!")
            except IntegrityError:  # If email already exists
                messages.warning(request, "You are already subscribed.")
            return redirect('subscribe')
    else:
        form = SubscribeForm()
    
    return render(request, 'core/subscribe.html', {'form': form})




