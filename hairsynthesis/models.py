from django.db import models

class hairsynthesis(models.Model):
    face_image = models.ImageField(upload_to='uploads/')  
    hairstyle_image = models.ImageField(upload_to='uploads/')  
    result_image = models.ImageField(upload_to='uploads/') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'hairSynthesis Request {self.id}'
