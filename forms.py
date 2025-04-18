from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput
from api.models import Message, Forum, Theme


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", )


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'creator']

        widgets = {
            "name": TextInput(attrs={
                'placeholder': 'Название форума'
            }),
            "creator": TextInput(attrs={
                'type': 'hidden'
            })
        }


class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description', 'forum', 'start_usr']

        widgets = {
            "name": TextInput(attrs={
                'placeholder': 'Название темы'
            }),
            "description": TextInput(attrs={
                'placeholder': 'Описание если нужно'
            }),
            "forum": TextInput(attrs={
                'type': 'hidden'
            }),
            "start_usr": TextInput(attrs={
                'type': 'hidden'
            })
        }
