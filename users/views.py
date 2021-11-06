from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from blogs.models import Tag

from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utilities import search_profiles, paginate_profiles

# Create your views here.
def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")
    
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        
        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        else:
             messages.error(request, "Username or password is incorrect")
            
    return render(request, "users/login_registration.html")

def logout_user(request):
    logout(request)
    messages.info(request, "User was succesfully logged out")
    return redirect("login")

def register_user(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, "User account created succesfully")
            
            login(request, user)
            return redirect("edit_account")
        else:
             messages.error(request, "An error has occured during registration")
            
    context = {"page": page,
               "form": form,}
    return render(request, "users/login_registration.html", context)

def profiles(request):
    profiles, search_query = search_profiles(request) 
    custom_range, profiles = paginate_profiles(request, profiles, 6) 
    
    context = {"profiles": profiles,
               "search_query": search_query,
               "custom_range": custom_range}
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    
    context = {"profile": profile,
               "top_skills": top_skills,
               "other_skills": other_skills,
               }
    return render(request, 'users/user_profile.html', context)

@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    blogs = profile.blog_set.all()
    tags = Tag.objects.all()
    
    context = {"profile": profile,
               "skills": skills,
               "blogs": blogs,
               "tags": tags}
    return render(request, "users/account.html", context)

@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect("account")
    context = {"form": form}
    return render(request, "users/profile_form.html", context)

@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "A skill was added!")
            return redirect("account")
        
    context = {"form": form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, "A skill was updated!")
            return redirect("account")
        
    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == "POST":
        skill.delete()
        messages.success(request, "A skill was deleted!")
        return redirect("account")
    context = {"object": skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {"message_requests": message_requests,
               "unread_count": unread_count,
               }
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm
    
    try:
        sender = request.user.profile
    except: 
        sender = None
        
    if request.method == "POST":
        form = MessageForm(request.POST,)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            
            messages.success(request, "Your message was sent!")
            
            return redirect("user_profile", pk=recipient.id)
            
    context = {"recipient": recipient,
               "form": form}
    return render(request, "users/message_form.html", context)