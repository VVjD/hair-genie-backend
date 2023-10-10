from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SynthesizedImage
from .serializers import hairsynthesisSerializer
from .models import hairsynthesis
from .forms import ImageUploadForm  
import torch
import torchvision.transforms as transforms
from PIL import Image
from stargan_v2.models import Generator

# StarGAN v2 모델 로드
model_path = '/Users/gustnin/Desktop/050000_nets_ema.ckpt'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
generator = Generator().to(devicdce)
generator.load_state_dict(torch.load(model_path, map_location=device))
generator.eval()

class HairSynthesisListCreateView(generics.ListCreateAPIView):
    queryset = HairSynthesis.objects.all()
    serializer_class = HairSynthesisSerializer

def hairsynthesis(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            
            # 이미지 전처리
            image = Image.open(uploaded_image)
            image = image.convert('RGB')
            transform = transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            ])
            image = transform(image).unsqueeze(0).to(device)
            
            # 이미지 합성
            with torch.no_grad():
                synthesized_image = generator(image)
            
            # 합성된 이미지 저장
            synthesized_image = synthesized_image.squeeze(0).cpu()
            save_path = '/Users/gustnin/Desktop/capstone2/hairresultimg/'  # 저장할 디렉토리 지정
            synthesized_image = transforms.ToPILImage()(synthesized_image)
            synthesized_image.save(save_path + 'synthesized_image.png')

            # hairsynthesis 모델에 저장
            hairsynthesis.objects.create(image='synthesized_image.png')

            return redirect('hairsynthesis:home')

    else:
        form = ImageUploadForm()

    synthesized_images = SynthesizedImage.objects.all()
    return render(request, 'hairsynthesis/home.html', {'form': form, 'synthesized_images': synthesized_images})
