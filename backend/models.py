from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.
class Tag(models.Model):
    word        = models.CharField(max_length=35)
    slug        = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.word

class Book(models.Model):
    title = models.CharField(max_length=200,unique=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    publisher = models.CharField(max_length=100,null=True,blank=True)
    desription = models.TextField(null=True,blank=True)
    publish_date = models.DateField(default=timezone.now,null=True,blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8,default=0.00)
    stock = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    width = models.DecimalField(decimal_places=2, max_digits=8,default=0,blank=True)
    height = models.DecimalField(decimal_places=2, max_digits=8,default=0,blank=True)
    rank_score = models.IntegerField(default=0)
    pdf_file = models.FileField(upload_to='pdf',editable = True,validators=[
        FileExtensionValidator(allowed_extensions=['pdf'])
    ],null=True,blank=True)
    cover_Image = models.ImageField(upload_to='image',editable = True,validators=[
        FileExtensionValidator(allowed_extensions=['jpg','png'])
    ],null=True,blank=True)
    tags = models.ManyToManyField(Tag,null=True,blank=True)
    
    
    def __str__(self):
        return self.title


    def get_api_url(self,request = None):
        return api_reverse("api-backend:Book-rud",kwargs={'pk':self.pk},request=request)


    """
    @property
    def owner(self):
        return self.author
    """

class UserAccountManager(BaseUserManager):

    def create_user(self,email,firstName,LastName,picture,addressName,street,subDistrict,district,province,zipcode,password=None):

        if not email :
            raise ValueError("User must have an email address.")

        email = self.normalize_email(email)
        user = self.model(
            email = email,
            firstName = firstName,
            LastName = LastName,
            picture = picture,
            addressName =  addressName,
            street =   street,
            subDistrict =   subDistrict,
            district = district,
            province =  province,
            zipcode  = zipcode,
            )
        
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        user = self.create_user(email,password)

        user.is_superuser = True
        user.is_admin = True

        user.save(using=self._db)

        return user



class UserAccount(AbstractBaseUser,PermissionsMixin) :

    username = None
    email = models.EmailField(unique=True)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('active', default=True)
    is_admin = models.BooleanField('admin', default=False)

    firstName = models.CharField(max_length=100,null=True,blank=True)
    lastName = models.CharField(max_length=100,null=True,blank=True)
    picture = models.ImageField(upload_to='user_image',editable = True,validators=[
        FileExtensionValidator(allowed_extensions=['jpg','png'])
    ],null=True,blank=True)
    addressName = models.TextField(null=True,blank=True)
    street = models.CharField(max_length=100,null=True,blank=True)
    subDistrict = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    province = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=50,null=True,blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.firstName + " " + self.lastName

    def __str__(self):
        return self.email

    """
    firstName = models.CharField(max_length=100,null=True,blank=True)
    LastName = models.CharField(max_length=100,null=True,blank=True)
    picture = models.ImageField(upload_to='user_image',editable = True,validators=[
        FileExtensionValidator(allowed_extensions=['jpg','png'])
    ],null=True,blank=True)
    addressName = models.TextField(null=True,blank=True)
    street = models.CharField(max_length=100,null=True,blank=True)
    subDistrict = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    province = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=50,null=True,blank=True)


    firstName,LastName,picture,addressName,street,subDistrict,district,province,zipcode
    """
