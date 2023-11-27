from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import crop_face, hair_synthesis
from .serializers import ImageUploadSerializer
import os
import cv2
from django.conf import settings

class HairSynthesis(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            faceImage = serializer.validated_data['faceImage']
            hairstyleImage = serializer.validated_data['hairstyleImage']
            
            faceImage_path = os.path.join(settings.MEDIA_ROOT, 'representative/custom/src', faceImage.name)
            hairstyleImage_path = os.path.join(settings.MEDIA_ROOT, 'representative/custom/ref', hairstyleImage.name)

            faceImage_crop_path = os.path.join(settings.MEDIA_ROOT, 'representative/hair/src/h', faceImage.name)
            hairstyleImage_crop_path = os.path.join(settings.MEDIA_ROOT, 'representative/hair/ref/h', hairstyleImage.name)

            with open(faceImage_path, 'wb') as f:
                for chunk in faceImage.chunks():
                    f.write(chunk)
            with open(hairstyleImage_path, 'wb') as f:
                for chunk in hairstyleImage.chunks():
                    f.write(chunk)

            try:
                cropped_face = crop_face(faceImage_path)
                cv2.imwrite(faceImage_crop_path, cropped_face)
                cropped_hairstyle = crop_face(hairstyleImage_path)
                cv2.imwrite(hairstyleImage_crop_path, cropped_hairstyle)
                
                hair_synthesis()

                respone_data = {
                    'hair_synthesis_result': os.path.join('/media/representative/results/reference_1.jpg')
                }
                return Response(respone_data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)