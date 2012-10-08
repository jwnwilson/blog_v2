from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django import forms
from blogV2.apps.accounts.models import UserProfile
from blogV2.apps.data.models import Entry

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        UserProfile.objects.create(user = user, email= self.cleaned_data['email'])
        
        return user
        
class BlogForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField( widget = forms.Textarea )
    
    """def __init__(self, title='',text='', *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField()
        self.fields['text'] = forms.CharField(widget = forms.Textarea, title = title, text= text )"""
    
    def clean_title(self):
        cd = self.cleaned_data
        
        title = cd.get('title')
        
        if len(title) < 3:
            raise forms.ValidationError("Please title more than 2 chars")
            
        return title
        
    def clean_text(self):
        cd = self.cleaned_data
        
        text = cd.get('text')
        
        if len(text) < 10:
            raise forms.ValidationError("Please more text.")
            
        return text
        
class BlogManagerForm(forms.Form):
    # Get titles of users blog posts
    user = None
    entryTitles=None
    # check box
    entry_List = None
    
    def __init__(self, user, *args, **kwargs):
        super(BlogManagerForm, self).__init__(*args, **kwargs)
        self.user = user
        self.entryTitles = self.getEntryTitles()
        self.fields['entry_List'] = forms.MultipleChoiceField(required= False,widget= CheckboxSelectMultiple, choices= self.entryTitles)
        
    def clean_entryList(self, submitType):
        cd = self.cleaned_data
        if submitType == 'edit_selected':
            ret = cd.get('entry_List')
            if len(ret) > 1:
                raise forms.ValidationError("Please select only one blog to edit.")
            else:
                return ret
        else:
            return cd.get('entry_List')
        
    def getEntryTitles(self):
        entries = Entry.objects.getUser_entries(self.user)
        self.entryTitles = []
        for entry in entries:
            self.entryTitles.append((entry.title,entry.title))
        return self.entryTitles
        
