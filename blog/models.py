# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify 
from django.utils import timezone # new
from django.urls import reverse
import uuid


User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self) :
        return self.user.username 

class Category(models.Model):
    name = models.CharField(max_length=50 )

    def __str__(self) :
        return self.name
    
class Post(models.Model):

    options =(
        ("draft","Draft"),
        ("published","Published")
    )
    title = models.CharField( max_length=100)
    content  = RichTextField()
    post_id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    slug = models.SlugField(max_length=100,null=False,unique=True)
    timestamp = models.DateTimeField(default= timezone.now)
    updated_at = models.DateTimeField(auto_now= True)
    author   = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(null=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    status =models.CharField(max_length=10,choices =options, default="draft")


    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a particular post instance."""
        return reverse("blog-single", kwargs={"slug":self.slug})

    
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(self.timestamp))
        return super().save(*args, **kwargs)
    
   
        

