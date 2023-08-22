# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify 
from django.utils import timezone # new
from django.urls import reverse
import uuid
from PIL import Image


User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self) :
        return self.user.username 

class Category(models.Model):
    name = models.CharField(max_length=50 )
    categories_id = models.UUIDField(default= uuid.uuid4,primary_key=True,unique=True,editable=False)
    slug =models.SlugField(max_length=100,null=False,unique=True) 

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
    image = models.ImageField(upload_to='blog_images/',null=True, blank=True)
    thumbnail = models.ImageField(upload_to='blog_thumbnails/',null=True, blank=True)
    categories = models.ForeignKey('Category',on_delete =models.SET_NULL,blank=True,null=True)
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
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            # Open the uploaded image using Pillow
            img = Image.open(self.image.path)

            # Define the maximum image size you want to allow
            max_width = 1000
            max_height = 1000

            # Resize the image while preserving the aspect ratio
            img.thumbnail((max_width, max_height))

            # Save the resized image back to the same path
            img.save(self.image.path)

            # You can also create a thumbnail for the image
            thumb_size = (800, 600)
            img.thumbnail(thumb_size)
            thumb_path = f'{self.image.path.split(".")[0]}_thumbnail.png'
            img.save(thumb_path)

            # Save the thumbnail path to the model field
            self.thumbnail = thumb_path

            # Save the updated model with the resized image and thumbnail
            super().save(*args, **kwargs)

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)



class Comment(models.Model):
    post= models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name= models.CharField('Name', max_length=254 )
    email= models.EmailField()
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    body= models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now =True)
    active = models.BooleanField(default=True)

    class Meta():
        ordering=('-created',)

    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


