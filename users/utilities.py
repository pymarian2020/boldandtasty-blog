from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill


def paginate_profiles(request, profiles, results):
    page = request.GET.get("page")
    
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)        
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(page)  
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)      

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1
    
    right_index =(int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    
    custom_range = range(left_index, right_index)
    
    return custom_range, profiles

def search_profiles(request):
    search_querry = ""
    
    if request.GET.get('search_querry'):
        search_querry = request.GET.get("search_querry")
    
    
        
    skills = Skill.objects.filter(name__icontains=search_querry)
    
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_querry) |
                                      Q(short_intro__icontains=search_querry) |
                                      Q(skill__in=skills)
                                      )  
    return profiles, search_querry
