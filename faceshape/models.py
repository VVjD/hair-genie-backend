from django.db import models

class FaceAnalysisResult(models.Model):
    face_type = models.CharField(max_length=255)
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.face_type
