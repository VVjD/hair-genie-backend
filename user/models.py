from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, uid, email, password=None, **extra_fields):
        if not uid:
            raise ValueError('아이디는 필수입니다')
        email = self.normalize_email(email) # 이메일 정규화
        user = self.model(uid=uid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, email, password=None, **extra_fields):
        user = self.create_user(uid=uid, email=email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    FACE_SHAPE_CHOICES = [
        ('선택', '선택'),
        ('계란형', '계란형'),
        ('하트형', '하트형'),
        ('둥근형', '둥근형'),
        ('긴 얼굴형', '긴 얼굴형'),
        ('각진형', '각진형'),
    ]

    uid = models.CharField(max_length=24, unique=True, verbose_name='아이디')
    uname = models.CharField(max_length=24, verbose_name='이름')
    unickname = models.CharField(max_length=24, verbose_name='별명')
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_imgs', verbose_name='프로필 사진')
    face_shape = models.CharField(max_length=24, choices=FACE_SHAPE_CHOICES, default='선택', verbose_name='얼굴형')
    uphone = models.CharField(max_length=24, verbose_name='전화번호')
    email = models.EmailField(unique=True, verbose_name='이메일')
    signuptime = models.DateTimeField(auto_now_add=True, verbose_name='가입 시간')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "User"