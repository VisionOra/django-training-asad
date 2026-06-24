from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ['title', 'body', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your post here...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }       