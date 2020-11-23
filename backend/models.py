from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.reverse import reverse as api_reverse
from django.core.validators import FileExtensionValidator
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
