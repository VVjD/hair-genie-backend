from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import crop_face, predict_face_type
from .serializers import ImageUploadSerializer
import os
import cv2
from django.conf import settings

class AnalyzeFaceShape(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_image = serializer.validated_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, 'uploads_faceshape', uploaded_image.name)
            out_path = os.path.join(settings.MEDIA_ROOT, 'cropped_faceshape', uploaded_image.name)

            with open(image_path, 'wb') as f:
                for chunk in uploaded_image.chunks():
                    f.write(chunk)

            try:
                cropped_face = crop_face(image_path)
                cv2.imwrite(out_path, cropped_face)
                
                predictions = predict_face_type(out_path)
                print(predictions)

                response_data = {
                    'predictions': predictions,
                    'cropped_face_url': os.path.join('/media/cropped_faceshape', uploaded_image.name),
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)