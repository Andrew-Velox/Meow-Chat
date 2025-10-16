from django.urls import path
from .views import *

urlpatterns = [
    path('ai-chat/', ai_chat_view, name='ai-chat'),
    path('ai-chat/send/', send_ai_message, name='send-ai-message'),
    path('ai-chat/clear/', clear_ai_chat, name='clear-ai-chat'),
    
    path('helper-chat/', helper_chat_view, name='helper-chat'),
    path('helper-chat/send/', send_helper_message, name='send-helper-message'),
    path('helper-chat/clear/', clear_helper_chat, name='clear-helper-chat'),

    path('travel-chat/', travel_chat_view, name='travel-chat'),
    path('travel-chat/send/', send_travel_message, name='send-travel-message'),
    path('travel-chat/clear/', clear_travel_chat, name='clear-travel-chat'),
    
]
