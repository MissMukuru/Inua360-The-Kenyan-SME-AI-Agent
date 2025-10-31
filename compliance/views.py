import google.generativeai as genai
from PIL import Image
from django.shortcuts import render
from django.conf import settings

from .models import ComplianceChecker
from .serializers import ComplianceCheckerSerializer, GeminiRequestSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

genai.configure(api_key=settings.GEMINI_API_KEY)

# Create your views here.

class ComplianceCheckerViewSet(viewsets.ModelViewSet):
    queryset = ComplianceChecker.objects.all()
    serializer_class = ComplianceCheckerSerializer

class GeminiViewSet(viewsets.ViewSet):
    """
    A DRF ViewSet for text and image analysis using Google Gemini API.
    """

    @action(detail=False, methods=["post"], url_path="analyze")
    def analyze(self, request):
        serializer = GeminiRequestSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data.get("prompt", "Analyze this input.")
            image_file = serializer.validated_data.get("image")

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Prepare inputs (text + optional image)
                inputs = [prompt]
                if image_file:
                    image = Image.open(image_file)
                    inputs.append(image)

                # Generate AI response
                response = model.generate_content(inputs)

                return Response(
                    {"response": response.text},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)