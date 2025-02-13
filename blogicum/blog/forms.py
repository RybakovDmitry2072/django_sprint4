from django import forms
from .models import Post, Comments



class CommentsForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ('text',)

class DynamicPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'   

