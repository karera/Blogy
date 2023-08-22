from django import forms
from django.forms import ModelForm
from .models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug','timestamp']


class CommentForm(forms.ModelForm):
    # name = forms.CharField(max_length=20,widget =forms.TextInput(attrs= {'placeholder': 'Enter name','class':'form-control'}))
    # email = forms.EmailField(max_length=20,widget =forms.EmailInput(attrs= {'placeholder': 'Enter name','class':'form-control'}))
    # body = forms.CharField(max_length=120,widget =forms.Textarea(attrs= {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'})) 
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}