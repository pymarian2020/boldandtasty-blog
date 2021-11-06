from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, Tag
from .forms import BlogForm, ReviewForm, TagForm
from .utilities import search_blogs, paginate_blogs


# Create your views here.

def blogs(request):
    blogs, search_query = search_blogs(request)
    custom_range, blogs = paginate_blogs(request, blogs, 6)
   

    context = {"blogs": blogs,
               "search_query": search_query,
               "custom_range": custom_range,}
    return render(request, "blogs/blogs.html", context)

def blog(request, pk):
    blog_obj = Blog.objects.get(id=pk)
    form = ReviewForm()
    # tags = Tag.objects.get(id=pk)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.blog = blog_obj
        review.owner = request.user.profile
        review.save()
        
        blog_obj.get_vote_count
        
        messages.success(request, "Your review was succesfully submitted!")
        
        return redirect("blog", pk=blog_obj.id)
    
    context = {"blog": blog_obj,
               "form": form,
               }              
    return render(request, "blogs/single-blog-post.html", context)

@login_required(login_url="login")
def create_blog(request):
    profile = request.user.profile
    form = BlogForm()
    
    if request.method == "POST":
        new_tags = request.POST.get("new_tags").replace(",", " ").split()
        new_tags = [tag.title() for tag in new_tags]
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = profile
            blog.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                blog.tags.add(tag)
            return redirect("account")
    context = {"form": form}
    return render(request, "blogs/blog_form.html", context)

@login_required(login_url="login")
def update_blog(request, pk):
    profile = request.user.profile
    blog = profile.blog_set.get(id=pk)
    blogs = Blog.objects.all()
    form = BlogForm(instance=blog)
    
    if request.method == "POST":
        new_tags = request.POST.get("new_tags").replace(",", " ").split()
        new_tags = [tag.title() for tag in new_tags]
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                blog.tags.add(tag)
            return redirect("account")
    context = {"form": form,
               "blog": blog,
               "blogs": blogs,
               }
    return render(request, "blogs/blog_form.html", context)

@login_required(login_url="login") 
def delete_blog(request, pk):
    profile = request.user.profile
    blog = profile.blog_set.get(id=pk)
    if request.method == "POST":
        blog.delete()
        return redirect("blogs")
    context = {"object": blog}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def delete_tag(request, pk):
    tag = Tag.objects.get(id=pk)
    blog = tag.blog_set.all().values_list("id", flat=True).first()
        
    if request.method == "POST":
        tag.delete()
        messages.success(request, "A tag was deleted!")
        return redirect(f"/update_blog/{blog}")
    context = {"object": tag}
    return render(request, "delete_template.html", context)
