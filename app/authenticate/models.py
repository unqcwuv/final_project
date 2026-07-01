from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name = 'Email',
        max_length=255,
        unique=True,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )

    is_company_owner = models.BooleanField(default=False)

    company = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Company(models.Model):
    inn = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='ИНН'
    )

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название компании'
        )

    owner = models.OneToOneField(
        'User',
        on_delete=models.PROTECT,
        related_name='owned_company',
        verbose_name='Владелец компании'
    )

    address = models.TextField(blank=True, verbose_name='Юридический адрес')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'