from django.forms import ModelForm
from django import forms
from .models import Blog, Review, Tag


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "description", "featured_image",]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input",
                                       "placeholder": f"Add {name}"})
        
        
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]
            
        labels = {
            "value": "Place your vote!",
            "body": "Add a comment with your vote."
        }  
        
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"}) 
           
            
class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})