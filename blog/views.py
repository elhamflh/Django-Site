from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render
# Create your views here.
from cgitb import html
from tkinter import N
from django.shortcuts import render , get_object_or_404 
from django.http import HttpResponse , JsonResponse
import datetime
from .models import Article , Category , ArticleHit
from django.contrib.auth.models import User
from account.mixins import AuthorAccessMixin
from django.db.models import Q

#def home(request , page=1):
    #article_list=Article.objects.published()
   # paginator = Paginator(article_list, 2)
    #category=Category.objects.all()
    #article = paginator.get_page(page)
    #context={
     #   "articels":article,
      #  "category":category,
      #  }
    #return render(request,"blog/home.html",context)

 
 # تغیر دهیم  articel_list.html را به   home.html   را بدهیم با باید  template_name = "blog/home.html"   اینجا یا باید اسم 


class ArticelList(ListView):
    queryset = Article.objects.published()
    paginate_by = 2
    #models=Articel
    #template_name = "blog/home.html"
    #context_object_name = "articels"


    

#def detail(request,slug):
  #  html=get_object_or_404(Article,slug=slug)
   # context={
    #    "article" :html
     #   }
    #return render (request,"blog/detail.html",context)


    
class ArticelDetail(DetailView):
    def get_object(self):
        slug=self.kwargs.get('slug')
        article=  get_object_or_404(Article.objects.published(),slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article
       

 



#برای پیش نمایش مقالات در سایت از قسمت اکانت
class ArticelPreview(AuthorAccessMixin,DetailView):
    def get_object(self):
        pk=self.kwargs.get('pk')
        return ( get_object_or_404(Article ,pk=pk))
 

#def category(request, slug , page=1):
    #category= get_object_or_404(Category, slug=slug , status=True)
    #article_list= category.articels.published()
    #paginator = Paginator(article_list, 2)
    #articels = paginator.get_page(page)
    #context={
     #   "category": category,
      #  "articels":articels,
       # }
    #return render (request,"blog/category.html",context)



class CategoryList(ListView):
    paginate_by = 2
    template_name= 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug=self.kwargs.get('slug')
        category=  get_object_or_404(Category.objects.active(),slug=slug)
 
        return (category.articels.published())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 2
    template_name= 'blog/author_list.html'

    def get_queryset(self):
        global author
        username=self.kwargs.get('username')
        author=  get_object_or_404(User,username=username)
 
        return author.articel.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['author'] = author
        return context



class SearchList(ListView):
    paginate_by = 2
    template_name= 'blog/search_list.html'

    def get_queryset(self):
        search=self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains = search) | Q(title__icontains = search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['search'] = self.request.GET.get('q')
        return context






    
 