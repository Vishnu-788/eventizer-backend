from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from llm_rag.services.llm_service import get_llm_response


# Create your views here.
class ChatbotAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_query = request.data["user_query"]
        print(user_query)
        if not user_query:
            return Response(
                {"error": "User query is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        llm_response = get_llm_response(user_query)
        return Response({"user_query": user_query, "llm_response": llm_response})
