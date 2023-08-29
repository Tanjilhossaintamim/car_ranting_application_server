from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_owner, **kwargs):
        if not email:
            raise ValueError('Please Insert An Email !')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, is_owner=is_owner)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **kwargs):
        superuser = self.create_user(email=email, password=password)
        superuser.is_active = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self.db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Owner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner_profile')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='ownerImage', null=True, blank=True)
    company_name = models.CharField(max_length=20, null=True, blank=True
                                    )
    date_of_birth = models.DateField(null=True, blank=True)


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='clientImage', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, created, instance, **kwargs):
    if created:
        if instance.is_owner:
            Owner.objects.create(user=instance)
        else:
            Client.objects.create(user=instance)
