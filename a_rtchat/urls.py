from django.urls import path
from .views import *


urlpatterns = [
    path('', chat_view, name='home'),
    path('chat/<username>', get_or_create_chatroom, name='start-chat'),
    path('chat/room/<chatroom_name>', chat_view, name='chatroom'),
    path('chat/new_groupchat/', create_groupchat, name='new-groupchat'),
    path('chat/edit/<chatroom_name>', chatroom_edit_view, name='edit-chatroom'),
    path('chat/delete/<chatroom_name>', chatroom_delete_view, name='delete-chatroom'),
    path('chat/leave/<chatroom_name>', chatroom_leave_view, name='chatroom-leave'),
    path('chat/fileupload/<chatroom_name>', chat_file_upload, name='chat-file-upload'),
    path("chat/voiceupload/<chatroom_name>", chat_voice_upload, name="chat-voice-upload"),
    
    path('chat/message_delete/<int:pk>/', delete_message_view, name='delete-chat-message'),
    path('api/user-chats/', user_chats_api, name='user-chats-api'),

]
