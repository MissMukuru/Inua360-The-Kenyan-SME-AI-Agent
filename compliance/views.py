import google.generativeai as genai
from PIL import Image
from django.shortcuts import render
from django.conf import settings

from .models import ComplianceChecker, Document, ValidationResult
from .serializers import ComplianceCheckerSerializer, GeminiRequestSerializer, GeminiValidationSerializer, DocumentSerializer, ValidationResultSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

genai.configure(api_key=settings.GEMINI_API_KEY)

# Create your views here.

class ComplianceCheckerViewSet(viewsets.ModelViewSet):
    queryset = ComplianceChecker.objects.all()
    serializer_class = ComplianceCheckerSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        """
        Upload document -> save -> analyze with Gemini -> return validation result.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()

        try:
            # Prepare Gemini model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Load the uploaded file (image/pdf)
            file_path = document.file.path
            image = Image.open(file_path)

            # Generate AI feedback
            prompt = (
                f"Analyze this {document.get_document_type_display()} "
                "and determine if it appears valid or authentic. "
                "Explain your reasoning and identify potential issues."
            )
            response = model.generate_content([prompt, image])
            ai_text = response.text or "No response from Gemini AI."

            # Simple heuristic for 'valid'
            valid = "valid" in ai_text.lower() and "invalid" not in ai_text.lower()
            confidence = 0.9 if valid else 0.6

            # Save validation result
            result, _ = ValidationResult.objects.update_or_create(
                document=document,
                defaults={
                    "valid": valid,
                    "reason": ai_text,
                    "confidence": confidence,
                    "recommendations": {"ai_feedback": ai_text},
                },
            )

            return Response(
                {
                    "document": DocumentSerializer(document).data,
                    "validation_result": ValidationResultSerializer(result).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # Even if AI fails, return document info
            return Response(
                {
                    "document": DocumentSerializer(document).data,
                    "error": str(e),
                },
                status=status.HTTP_201_CREATED,
            )

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

class GeminiValidationViewSet(viewsets.ViewSet):
    """
    Validates uploaded compliance documents using Google Gemini AI.
    """

    @action(detail=False, methods=["post"], url_path="validate")
    def validate_document(self, request):
        serializer = GeminiValidationSerializer(data=request.data)
        if serializer.is_valid():
            document_id = serializer.validated_data["document_id"]
            prompt = serializer.validated_data.get("prompt", "Validate this compliance document.")

            try:
                document = Document.objects.get(id=document_id)
                model = genai.GenerativeModel("gemini-1.5-flash")

                image = Image.open(document.file)
                inputs = [prompt, image]
                response = model.generate_content(inputs)

                # Basic result parsing (can be made richer)
                text_response = response.text
                valid = "valid" in text_response.lower()
                confidence = 0.8 if valid else 0.5

                result, _ = ValidationResult.objects.update_or_create(
                    document=document,
                    defaults={
                        "valid": valid,
                        "reason": text_response,
                        "confidence": confidence,
                        "recommendations": {"ai_feedback": text_response},
                    },
                )

                return Response(
                    ValidationResultSerializer(result).data,
                    status=status.HTTP_200_OK,
                )

            except Document.DoesNotExist:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)