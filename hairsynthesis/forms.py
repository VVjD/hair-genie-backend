from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='이미지 업로드')
