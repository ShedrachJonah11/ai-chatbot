# chat/views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Conversation, Message
import openai

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        # Process the file here (e.g., save it, send to AI models)
        return Response({'status': 'file uploaded successfully'})

def chat_view(request):
    return render(request, 'chat/chat.html')

@require_POST
def get_ai_response(request):
    user_input = request.POST.get('user_input')
    
    # Get or create a conversation
    conversation, created = Conversation.objects.get_or_create(user=request.user)
    
    # Save user message
    Message.objects.create(conversation=conversation, content=user_input, is_user=True)
    
    # Get AI response
    openai.api_key = settings.OPENAI_API_KEY
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )
        ai_response = response.choices[0].text.strip()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    # Save AI message
    Message.objects.create(conversation=conversation, content=ai_response, is_user=False)
    
    return JsonResponse({'response': ai_response})
