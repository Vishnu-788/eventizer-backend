from django.urls import path
from llm_rag.views import ChatbotAPI

urlpatterns = [
    path('', ChatbotAPI.as_view(), name='chatbot'),
]