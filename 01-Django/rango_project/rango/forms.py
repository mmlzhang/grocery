from django import forms
from rango.models import Page, Category
from user.models import UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="请输入分类名")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="请输入网页名称")
    url = forms.URLField(max_length=200, help_text="请输入网页链接")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # 添加 http//
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)
        #fields = ('title', 'url', 'views')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = UserProfile
        exclude = ('user',)