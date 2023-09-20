from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, uid, uemail, password=None, **extra_fields):
        if not uid:
            raise ValueError('아이디는 필수입니다')
        email = self.normalize_email(uemail) # 이메일 정규화
        user = self.model(uid=uid, uemail=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, uemail, password=None, **extra_fields):
        user = self.create_user(uid=uid, uemail=uemail, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=24, unique=True)
    uname = models.CharField(max_length=24)
    unickname = models.CharField(max_length=24)
    profile_image = models.TextField()
    face_shape = models.CharField(max_length=24)
    uphone = models.CharField(max_length=24)
    uemail = models.EmailField(unique=True)
    signuptime = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['uemail']

    class Meta:
        db_table = "User"