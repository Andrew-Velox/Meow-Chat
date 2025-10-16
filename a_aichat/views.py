from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import AIChat, HelperChat,TravelChat
import requests
import json
import logging

logger = logging.getLogger(__name__)

AIGF_WEBHOOK_URL = "http://localhost:5678/webhook/5b4ab579-2dc4-44a4-88b3-433eb2620ace"
HELPER_WEBHOOK_URL = "http://localhost:5678/webhook/046799b7-3aa8-4fe3-9176-3be752759db9"

TRAVEL_WEBHOOK_URL = "http://localhost:5678/webhook/173fa69d-d330-4682-b2b5-acace959c2e7"

@login_required
def ai_chat_view(request):
    """Main AI chat view"""
    chat_messages = AIChat.objects.filter(user=request.user)[:50]
    
    context = {
        'chat_messages': chat_messages,
        'chatroom_name': 'ai-girlfriend',
    }
    return render(request, 'a_aichat/ai_chat.html', context)

@login_required
def send_ai_message(request):
    """Send message to AI and get response"""
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Save user message
            user_chat = AIChat.objects.create(
                user=request.user,
                message=user_message,
                is_user_message=True
            )
            
            # Send to n8n webhook
            try:
                payload = {
                    'message': user_message,
                    'user_id': request.user.id,
                    'username': request.user.username
                }
                
                print(f"\n=== AI CHAT DEBUG ===")
                print(f"Sending to webhook: {AIGF_WEBHOOK_URL}")
                print(f"Payload: {payload}")
                
                response = requests.post(
                    AIGF_WEBHOOK_URL,
                    json=payload,
                    timeout=30
                )
                
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.text}")
                print(f"===================\n")
                
                if response.status_code == 200:
                    try:
                        ai_response = response.json()
                        print(f"Parsed JSON response: {ai_response}")
                        
                        # Check if n8n returned an error
                        if ai_response.get('message') == 'Error in workflow':
                            logger.error("n8n workflow returned an error")
                            ai_chat = AIChat.objects.create(
                                user=request.user,
                                message="There's an error in the n8n workflow configuration. Please check your n8n workflow. 💕",
                                is_user_message=False
                            )
                            return JsonResponse({
                                'success': True,
                                'user_message': {
                                    'id': str(user_chat.id),
                                    'message': user_message,
                                    'created': user_chat.created.strftime('%I:%M %p')
                                },
                                'ai_message': {
                                    'id': str(ai_chat.id),
                                    'message': ai_chat.message,
                                    'created': ai_chat.created.strftime('%I:%M %p')
                                }
                            })
                        
                    except json.JSONDecodeError:
                        # If response is not JSON, use the text directly
                        ai_response = {'response': response.text}
                        logger.info(f"Non-JSON response, using text: {response.text}")
                    
                    # Extract AI message from response - try multiple possible keys
                    print(f"DEBUG: ai_response.get('response') = {repr(ai_response.get('response'))}")
                    
                    ai_message = None
                    for key in ['response', 'message', 'output', 'reply', 'text']:
                        if key in ai_response and ai_response[key]:
                            ai_message = ai_response[key]
                            print(f"Found AI message in key '{key}': {ai_message[:100]}")
                            break
                    
                    if not ai_message:
                        if isinstance(ai_response, str):
                            ai_message = str(ai_response)
                        else:
                            ai_message = 'Sorry, I could not understand that.'
                    
                    print(f"Final ai_message: {ai_message[:100] if ai_message else None}")
                    
                    # Save AI response
                    ai_chat = AIChat.objects.create(
                        user=request.user,
                        message=ai_message,
                        is_user_message=False
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'user_message': {
                            'id': str(user_chat.id),
                            'message': user_message,
                            'created': user_chat.created.strftime('%I:%M %p')
                        },
                        'ai_message': {
                            'id': str(ai_chat.id),
                            'message': ai_message,
                            'created': ai_chat.created.strftime('%I:%M %p')
                        }
                    })
                else:
                    # If webhook fails, create a fallback response
                    logger.warning(f"Webhook returned non-200 status: {response.status_code}")
                    ai_chat = AIChat.objects.create(
                        user=request.user,
                        message=f"I'm having trouble connecting right now (Status: {response.status_code}). Please try again later. 💕",
                        is_user_message=False
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'user_message': {
                            'id': str(user_chat.id),
                            'message': user_message,
                            'created': user_chat.created.strftime('%I:%M %p')
                        },
                        'ai_message': {
                            'id': str(ai_chat.id),
                            'message': ai_chat.message,
                            'created': ai_chat.created.strftime('%I:%M %p')
                        }
                    })
                    
            except requests.exceptions.RequestException as e:
                # Webhook connection error
                logger.error(f"Webhook connection error: {str(e)}")
                ai_chat = AIChat.objects.create(
                    user=request.user,
                    message=f"I'm having trouble connecting right now. Please check if n8n is running. 💕",
                    is_user_message=False
                )
                
                return JsonResponse({
                    'success': True,
                    'user_message': {
                        'id': str(user_chat.id),
                        'message': user_message,
                        'created': user_chat.created.strftime('%I:%M %p')
                    },
                    'ai_message': {
                        'id': str(ai_chat.id),
                        'message': ai_chat.message,
                        'created': ai_chat.created.strftime('%I:%M %p')
                    }
                })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def clear_ai_chat(request):
    """Clear AI chat history for the current user"""
    if request.method == 'POST':
        AIChat.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# ============ HELPER ASSISTANT VIEWS ============

@login_required
def helper_chat_view(request):
    """Main Helper Assistant chat view"""
    chat_messages = HelperChat.objects.filter(user=request.user)[:50]
    
    context = {
        'chat_messages': chat_messages,
        'chatroom_name': 'helping-assistant',
    }
    return render(request, 'a_aichat/helper_chat.html', context)

@login_required
def send_helper_message(request):
    """Send message to Helper Assistant and get response"""
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Save user message
            user_chat = HelperChat.objects.create(
                user=request.user,
                message=user_message,
                is_user_message=True
            )
            
            # Send to n8n webhook
            try:
                payload = {
                    'message': user_message,
                    'user_id': request.user.id,
                    'username': request.user.username
                }
                
                print(f"\n=== HELPER CHAT DEBUG ===")
                print(f"Sending to webhook: {HELPER_WEBHOOK_URL}")
                print(f"Payload: {payload}")
                
                response = requests.post(
                    HELPER_WEBHOOK_URL,
                    json=payload,
                    timeout=30
                )
                
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.text}")
                print(f"===================\n")
                
                if response.status_code == 200:
                    try:
                        ai_response = response.json()
                        print(f"Parsed JSON response: {ai_response}")
                        
                        # Check if n8n returned an error
                        if ai_response.get('message') == 'Error in workflow':
                            logger.error("n8n workflow returned an error")
                            ai_chat = HelperChat.objects.create(
                                user=request.user,
                                message="There's an error in the n8n workflow configuration. Please check your n8n workflow. 🤖",
                                is_user_message=False
                            )
                            return JsonResponse({
                                'success': True,
                                'user_message': {
                                    'id': str(user_chat.id),
                                    'message': user_message,
                                    'created': user_chat.created.strftime('%I:%M %p')
                                },
                                'ai_message': {
                                    'id': str(ai_chat.id),
                                    'message': ai_chat.message,
                                    'created': ai_chat.created.strftime('%I:%M %p')
                                }
                            })
                        
                    except json.JSONDecodeError:
                        # If response is not JSON, use the text directly
                        ai_response = {'response': response.text}
                        logger.info(f"Non-JSON response, using text: {response.text}")
                    
                    # Extract AI message from response - try multiple possible keys
                    print(f"DEBUG: ai_response.get('response') = {repr(ai_response.get('response'))}")
                    
                    ai_message = None
                    for key in ['response', 'message', 'output', 'reply', 'text']:
                        if key in ai_response and ai_response[key]:
                            ai_message = ai_response[key]
                            print(f"Found AI message in key '{key}': {ai_message[:100]}")
                            break
                    
                    if not ai_message:
                        if isinstance(ai_response, str):
                            ai_message = str(ai_response)
                        else:
                            ai_message = 'Sorry, I could not understand that.'
                    
                    print(f"Final ai_message: {ai_message[:100] if ai_message else None}")
                    
                    # Save AI response
                    ai_chat = HelperChat.objects.create(
                        user=request.user,
                        message=ai_message,
                        is_user_message=False
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'user_message': {
                            'id': str(user_chat.id),
                            'message': user_message,
                            'created': user_chat.created.strftime('%I:%M %p')
                        },
                        'ai_message': {
                            'id': str(ai_chat.id),
                            'message': ai_message,
                            'created': ai_chat.created.strftime('%I:%M %p')
                        }
                    })
                else:
                    # If webhook fails, create a fallback response
                    logger.warning(f"Webhook returned non-200 status: {response.status_code}")
                    ai_chat = HelperChat.objects.create(
                        user=request.user,
                        message=f"I'm having trouble connecting right now (Status: {response.status_code}). Please try again later. 🤖",
                        is_user_message=False
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'user_message': {
                            'id': str(user_chat.id),
                            'message': user_message,
                            'created': user_chat.created.strftime('%I:%M %p')
                        },
                        'ai_message': {
                            'id': str(ai_chat.id),
                            'message': ai_chat.message,
                            'created': ai_chat.created.strftime('%I:%M %p')
                        }
                    })
                    
            except requests.exceptions.RequestException as e:
                # Webhook connection error
                logger.error(f"Webhook connection error: {str(e)}")
                ai_chat = HelperChat.objects.create(
                    user=request.user,
                    message=f"I'm having trouble connecting right now. Please check if n8n is running. 🤖",
                    is_user_message=False
                )
                
                return JsonResponse({
                    'success': True,
                    'user_message': {
                        'id': str(user_chat.id),
                        'message': user_message,
                        'created': user_chat.created.strftime('%I:%M %p')
                    },
                    'ai_message': {
                        'id': str(ai_chat.id),
                        'message': ai_chat.message,
                        'created': ai_chat.created.strftime('%I:%M %p')
                    }
                })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def clear_helper_chat(request):
    """Clear Helper Assistant chat history for the current user"""
    if request.method == 'POST':
        HelperChat.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# ============ TRAVEL ASSISTANT VIEWS ============

@login_required
def travel_chat_view(request):
    """Main Travel Assistant chat view"""
    chat_messages = TravelChat.objects.filter(user=request.user)[:50]
    
    context = {
        'chat_messages': chat_messages,
        'chatroom_name': 'travel-assistant',
    }
    return render(request, 'a_aichat/travel_chat.html', context)

@login_required
def send_travel_message(request):
    """Send message to Travel Assistant and get response"""
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Save user message
            user_chat = TravelChat.objects.create(
                user=request.user,
                message=user_message,
                is_user_message=True
            )
            
            # Send to n8n webhook
            try:
                payload = {
                    'message': user_message,
                    'user_id': request.user.id,
                    'username': request.user.username
                }
                
                print(f"\n=== TRAVEL CHAT DEBUG ===")
                print(f"Sending to webhook: {TRAVEL_WEBHOOK_URL}")
                print(f"Payload: {payload}")
                
                response = requests.post(
                    TRAVEL_WEBHOOK_URL,
                    json=payload,
                    timeout=30
                )
                
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.text}")
                print(f"===================\n")
                
                if response.status_code == 200:
                    try:
                        ai_response = response.json()
                        print(f"Parsed JSON response: {ai_response}")
                        
                        # Check if n8n returned an error
                        if ai_response.get('message') == 'Error in workflow':
                            logger.error("n8n workflow returned an error")
                            ai_chat = TravelChat.objects.create(
                                user=request.user,
                                message="There's an error in the n8n workflow configuration. Please check your n8n workflow. 🤖",
                                is_user_message=False
                            )
                            return JsonResponse({
                                'success': True,
                                'user_message': {
                                    'id': str(user_chat.id),
                                    'message': user_message,
                                    'created': user_chat.created.strftime('%I:%M %p')
                                },
                                'ai_message': {
                                    'id': str(ai_chat.id),
                                    'message': ai_chat.message,
                                    'created': ai_chat.created.strftime('%I:%M %p')
                                }
                            })
                        
                    except json.JSONDecodeError:
                        # If response is not JSON, use the text directly
                        ai_response = {'response': response.text}
                        logger.info(f"Non-JSON response, using text: {response.text}")
                    
                    # Extract AI message from response - try multiple possible keys
                    print(f"DEBUG: ai_response.get('response') = {repr(ai_response.get('response'))}")
                    
                    ai_message = None
                    for key in ['response', 'message', 'output', 'reply', 'text']:
                        if key in ai_response and ai_response[key]:
                            ai_message = ai_response[key]
                            print(f"Found AI message in key '{key}': {ai_message[:100]}")
                            break
                    
                    if not ai_message:
                        if isinstance(ai_response, str):
                            ai_message = str(ai_response)
                        else:
                            ai_message = 'Sorry, I could not understand that.'
                    
                    print(f"Final ai_message: {ai_message[:100] if ai_message else None}")
                    
                    # Save AI response
                    ai_chat = TravelChat.objects.create(
                        user=request.user,
                        message=ai_message,
                        is_user_message=False
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'user_message': {
                            'id': str(user_chat.id),
                            'message': user_message,
                            'created': user_chat.created.strftime('%I:%M %p')
                        },
                        'ai_message': {
                            'id': str(ai_chat.id),
                            'message': ai_message,
                            'created': ai_chat.created.strftime('%I:%M %p')
                        }
                    })
                else:
                    # If webhook fails, create a fallback response
                    logger.warning(f"Webhook returned non-200 status: {response.status_code}")
                    ai_chat = TravelChat.objects.create(
                        user=request.user,
                        message=f"I'm having trouble connecting right now (Status: {response.status_code}). Please try again later. 🤖",
                        is_user_message=False
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'user_message': {
                            'id': str(user_chat.id),
                            'message': user_message,
                            'created': user_chat.created.strftime('%I:%M %p')
                        },
                        'ai_message': {
                            'id': str(ai_chat.id),
                            'message': ai_chat.message,
                            'created': ai_chat.created.strftime('%I:%M %p')
                        }
                    })
                    
            except requests.exceptions.RequestException as e:
                # Webhook connection error
                logger.error(f"Webhook connection error: {str(e)}")
                ai_chat = TravelChat.objects.create(
                    user=request.user,
                    message=f"I'm having trouble connecting right now. Please check if n8n is running. 🤖",
                    is_user_message=False
                )
                
                return JsonResponse({
                    'success': True,
                    'user_message': {
                        'id': str(user_chat.id),
                        'message': user_message,
                        'created': user_chat.created.strftime('%I:%M %p')
                    },
                    'ai_message': {
                        'id': str(ai_chat.id),
                        'message': ai_chat.message,
                        'created': ai_chat.created.strftime('%I:%M %p')
                    }
                })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def clear_travel_chat(request):
    """Clear Travel Assistant chat history for the current user"""
    if request.method == 'POST':
        TravelChat.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
