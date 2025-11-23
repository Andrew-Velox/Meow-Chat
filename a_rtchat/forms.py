from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Message #general', 'class': 'bg-transparent text-white placeholder-gray-400 border-0 focus:ring-0 focus:outline-none w-full py-2', 'maxlength': '300', 'autofocus': True}),
        }


class NewGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name', 'banner']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={'placeholder': 'Enter server name', 'class': 'bg-gray-700 text-white placeholder-gray-400 border border-gray-600 rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none', 'maxlength': '100', 'autofocus': True}),
            'banner': forms.FileInput(attrs={'class': 'bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none', 'accept': 'image/*'}),
        }



class ChatRoomEditForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name', 'banner']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={'placeholder': 'Enter server name', 'class': 'bg-gray-700 text-white placeholder-gray-400 border border-gray-600 rounded px-3 py-2 text-xl font-bold focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none', 'maxlength': '100', 'autofocus': True,
            }),
            'banner': forms.FileInput(attrs={'class': 'bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none', 'accept': 'image/*'}),
        }
