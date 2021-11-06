from django.db import models
import uuid
from users.models import Profile



# Create your models here.
class Blog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to="profiles/blogs/", default="default.jpg")
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


    class Meta():
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property
    def image_url(self):
        try:
            url = self.featured_image.url
        except:
            url = " static\images\default.jpg"
        return url
    
    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list("owner__id", flat=True)
        return query_set
        
    
    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value="up").count()
        total_votes = reviews.count()
        
        ratio = (up_votes/total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()
        
        
    
class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote")
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [["owner", "blog"]]
    
    def __str__(self):
        return self.value
    

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name