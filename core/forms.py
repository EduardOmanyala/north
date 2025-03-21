from django import forms 
from custom_user.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import Blog, Category, Subscriber




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    #username = forms.CharField(max_length=150)
    #password1 = forms.CharField(widget=forms.PasswordInput)
    #password2 = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['first_name', 'last_name', 'email', 'password1','password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1','password2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['type', 'title', 'category', 'image', 'main']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'image']




class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']