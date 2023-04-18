from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator
from account.models import User
from  .extentions.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# my manager

class ArticleAManager (models.Manager):
    def published(self):
        return self.filter(status='p')

class CategoryManager (models.Manager):
    def active(self):
        return self.filter(status=True)


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی پی")


# Create your models here.

class Category (models.Model):
    parent= models.ForeignKey('self' , default=None ,null=True,blank=True,on_delete=models.SET_NULL, related_name="children", verbose_name="زیر مجموعه ")
    title= models.CharField(max_length=200, blank=True, verbose_name=" دسته بندی" )
    slug= models.SlugField (max_length=100, unique=True, null=False, blank=True, db_index=True , verbose_name="اسلاگ")
    status= models.BooleanField(default=True , verbose_name="آیا نمایش داده شود؟")
    position=models.IntegerField(verbose_name="موقعیت")



    class meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering=["parent__id",'position']



    def __str__(self):
        return f"{self.title}"

    objects =CategoryManager()    



class Tag(models.Model):
    caption=models.CharField(max_length=20)

    def __str__ (self):
        return self.caption




class Authur(models.Model):
    name=models.CharField(max_length=50)
    family=models.CharField(max_length=50)
    email=models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} {self.family}"


 
class Article (models.Model):
    STATUS_CHOICES=[
    ("d","پیش نویس"),
    ("p","منتشر شده"),
    ("i"," در حال برسی"),
    ("b"," برگشت داده شده "),]
    
    author=models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, db_constraint=False, null=True, related_name="articel" , verbose_name="نویسنده")
    title= models.CharField(max_length=200, blank=True, verbose_name="عنوان مقاله")
    slug= models.SlugField (max_length=100, unique=True, null=False, blank=True, db_index=True , verbose_name="آدرس مقاله")
    category=models.ManyToManyField(Category , verbose_name="دسته بندی مقالات", related_name="articels")
    description = models.TextField(blank=True,validators=[MinLengthValidator(20)] , verbose_name="محتوا")
    thumbnail= models.ImageField(upload_to="images", blank=True , verbose_name="انتخاب تصویر")
    publish= models.DateTimeField(default=timezone.now , verbose_name="نشر")
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    status= models.CharField(max_length=1, choices=STATUS_CHOICES , verbose_name="وضعیت")
    is_special= models.BooleanField(default=False, verbose_name="کاربر ویژه")
    tags=models.ManyToManyField(Tag , verbose_name="#")
    comments = GenericRelation(Comment)
    hits= models.ManyToManyField(IpAddress , blank=True ,through="ArticleHit" , related_name="hits" , verbose_name="بازدید ها")
   



    class meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering=['-publish']
    

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('account:home')
        
    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description="زمان انتشار"


    def thumbnail_tag(self):
        return format_html("<img  src='{}' width:40px height:75px>".format(self.thumbnail.url))

    def category_to_str (self):
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description="دسته بندی مقالات"
    pass
    

    objects = ArticleAManager()    


class ArticleHit(models.Model):

    article = models.ForeignKey(IpAddress ,on_delete= models.CASCADE)
    IpAddress = models.ForeignKey(Article ,on_delete= models.CASCADE)
    created= models.DateTimeField(auto_now_add=True)








# class Comment(models.Model):
#     title=models.CharField(max_length=200)
#     name=models.CharField(max_length=100)
#     email=models.EmailField(max_length=500)
#     text=models.TextField(max_length=500)
#     post=models.ForeignKey(Article,on_delete=models.CASCADE,blank=True)
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def __str__ (self):
#         return self.title

    

#class Profile(models.Model):

        #user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE)
        #avatar = models.ImageField(default='1.jpg', upload_to='displays', height_field=None, width_field=None, max_length=None)
    




