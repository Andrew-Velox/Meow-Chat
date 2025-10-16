from django.contrib import admin
from .models import AIChat, HelperChat, TravelChat

@admin.register(AIChat)
class AIChatAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'is_user_message']
    list_filter = ['user', 'is_user_message', 'created']
    search_fields = ['user__username', 'message']
    ordering = ['-created']

@admin.register(HelperChat)
class HelperChatAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'is_user_message']
    list_filter = ['user', 'is_user_message', 'created']
    search_fields = ['user__username', 'message']
    ordering = ['-created']

@admin.register(TravelChat)
class TravelChatAdmin(admin.ModelAdmin):
    list_display = ['user','created','is_user_message']
    list_filter = ['user', 'is_user_message', 'created']
    search_fields = ['user__username', 'message']
    ordering = ['-created']