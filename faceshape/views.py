from django.http import JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np

# 모델 불러오기
model_path = r"C:\faceshape\model7.h5"
model = load_model(model_path)

# 얼굴형 분류 레이블
face_types = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']

def analyze_face(request):
    if request.method == 'POST':
        try:
            # 클라이언트로부터 이미지 파일을 받음
            image_file = request.FILES['image']

            # 이미지 전처리
            img = image.load_img(image_file, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # 얼굴형 분석 예측
            preds = model.predict(x)
            top_pred_indices = np.argsort(preds[0])[::-1][:3]  # 상위 3개 예측 인덱스

            # 결과 반환
            result = []
            for i, pred_index in enumerate(top_pred_indices):
                face_type = face_types[pred_index]
                probability = preds[0][pred_index]
                result.append({'face_type': face_type, 'probability': probability})

            return JsonResponse({'predictions': result})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'POST 요청만 지원합니다.'})
