from rest_framework import serializers
from .models import SynthesizedImage, hairsynthesis

class hairsynthesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = hairsynthesis
        fields = ('face_image', 'hairstyle_image', 'result_image', 'created_at')  

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = instance.image.url  
        return ret