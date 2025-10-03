from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
# Create your views here.

@login_required
def chat_view(request, chatroom_name="public-chat"):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
            else:
                messages.warning(request, 'You need to verify your email address before joining group chats.')
                return redirect('profile-settings')

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
        
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group,
    }

    return render(request, 'a_rtchat/chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username = username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chatroom', chatroom.group_name)
   
    chatroom = ChatGroup.objects.create( is_private = True )
    chatroom.members.add(other_user, request.user)   
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST, request.FILES)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)


    context = {
        'form': form,
    }  
    return render(request, 'a_rtchat/create_groupchat.html', context)


@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    form = ChatRoomEditForm(instance=chat_group)

    if request.method == 'POST':
        action = request.POST.get('action', 'update')
        
        if action == 'remove_members':
            # Handle member removal
            remove_members = request.POST.getlist('remove_members')
            removed_count = 0
            for member_id in remove_members:
                try:
                    member = User.objects.get(id=member_id)
                    if member != chat_group.admin and member in chat_group.members.all():
                        chat_group.members.remove(member)
                        removed_count += 1
                except User.DoesNotExist:
                    pass
            
            if removed_count > 0:
                messages.success(request, f'Successfully removed {removed_count} member(s) from the server.')
            return redirect('edit-chatroom', chatroom_name)
        else:
            # Handle server info update
            form = ChatRoomEditForm(request.POST, request.FILES, instance=chat_group)
            if form.is_valid():
                form.save()
                messages.success(request, 'Server settings updated successfully.')
                return redirect('edit-chatroom', chatroom_name)
        

    context = {
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'a_rtchat/chatroom_edit.html', context)


@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == 'POST':
        chat_group.delete()
        messages.success(request, 'Chatroom deleted successfully.')
        return redirect('home')
    return render(request, 'a_rtchat/chatroom_delete.html', {'chat_group': chat_group})

@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
   
    if request.user not in chat_group.members.all():
        raise Http404()
    
    if request.method == 'POST':
        chat_group.members.remove(request.user)
        messages.success(request, 'You have left the chatroom.')
        return redirect('home')
    return render(request, 'a_rtchat/chatroom_leave.html', {'chat_group': chat_group})



@login_required
def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.htmx and request.FILES:
        file = request.FILES.get('file')
        messages = GroupMessage.objects.create(
            file=file,
            author=request.user,
            group=chat_group
        )

        channel_layer = get_channel_layer()

        event= {
            'type': 'message_handler',
            "message_id": messages.id,

        }

        async_to_sync(channel_layer.group_send)(chatroom_name, event)

    return HttpResponse()


@login_required
def user_chats_api(request):
    """API endpoint to get user's chats for the sidebar"""
    # Get user's group chats (excluding public chat)
    user_chats = ChatGroup.objects.filter(
        members=request.user
    ).exclude(
        group_name='public-chat'
    ).order_by('-id')[:10]  # Limit to 10 most recent chats
    
    chats_data = []
    for chat in user_chats:
        chat_data = {
            'group_name': chat.group_name,
            'groupchat_name': chat.groupchat_name,
            'is_private': chat.is_private,
            'member_count': chat.members.count(),
            'banner_url': chat.banner_url,  # Include banner URL for group chats
        }
        
        # For private chats, include the other user's information
        if chat.is_private:
            other_user = None
            for member in chat.members.all():
                if member != request.user:
                    other_user = member
                    break
            
            if other_user:
                chat_data.update({
                    'other_user_username': other_user.username,
                    'other_user_name': other_user.profile.name if hasattr(other_user, 'profile') else other_user.username,
                    'other_user_avatar': other_user.profile.avatar if hasattr(other_user, 'profile') else None,
                })
        
        chats_data.append(chat_data)
    
    return JsonResponse(chats_data, safe=False)