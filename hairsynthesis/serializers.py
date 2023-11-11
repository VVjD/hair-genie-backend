from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    faceImage = serializers.ImageField()
    hairstyleImage = serializers.ImageField()