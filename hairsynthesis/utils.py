import cv2
import subprocess
import os

def crop_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return ValueError("이미지에서 얼굴을 찾을 수 없습니다.")

    x, y, w, h = faces[0]
    x = max(0, x - 20)
    y = max(0, y - 20)
    cropped_image = image[y:y+h+40, x:x+w+40]

    return cropped_image

def hair_synthesis():
    try:
        stargan_v2_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stargan-v2')
        print(stargan_v2_path)
        os.chdir(stargan_v2_path)

        subprocess.run([
            'python', 'main.py', '--mode', 'align',
            '--inp_dir', '../media/representative/hair/ref/h',
            '--out_dir', '../media/representative/hair/ref/h/'
        ])

        subprocess.run([
            'python', 'main.py', '--mode', 'align',
            '--inp_dir', '../media/representative/hair/src/h',
            '--out_dir', '../media/representative/hair/src/h/'
        ])

        subprocess.run([
            'python', 'main.py', '--mode', 'sample',
            '--num_domains', '1',
            '--resume_iter', '50000',
            '--w_hpf', '1',
            '--checkpoint_dir', 'expr/checkpoints/',
            '--result_dir', '../media/representative/results/',
            '--src_dir', '../media/representative/hair/src',
            '--ref_dir', '../media/representative/hair/ref'
        ])
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")

    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))