from django.http import Http404
from django.shortcuts import render , get_object_or_404 , redirect
from blog.models import Article 
#فیللد های قسمت اکانت برای اضافه کردن مقاله
class FieldsMixin ():
    def dispatch(self, request, *args, **kwargs):
        self.fields =  ["title","slug","category","is_special","description","thumbnail","publish","status","tags",]
        
        if  request.user.is_superuser:
            self.fields.append("author")    
        return super().dispatch(request, *args, **kwargs)

#پست ها هم برای ادمین و هم برای  نویسنده سیو شود
class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit= False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status == 'd'
        return super().form_valid(form)
        #  if not self.obj.status in ['d','i']     :    میشد بنویسیم  

    


# برای اینکه فقط ادمین اصلی بتواند پست های منتشر شده را ادیت کند
#نویسنده قبل از اینکه مقاله تایید شود بتواند آن را ادیت کند
class AuthorAccessMixin ():

    def dispatch(self, request,pk, *args, **kwargs):
        articel= get_object_or_404(Article , pk=pk)
        if articel.author == request.user and articel.status in ['d','b'] or request.user.is_superuser:
             return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can't see this")

 #فقط ادمین اصلی بتواند پست هارا حذف کند

class SuperUserAccessMixin ():

    def dispatch(self, request, *args, **kwargs):
     
        if request.user.is_superuser:
             return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can't see this")


class AuthorsAccessMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
                
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect ("account:profile")
        else:
            return redirect ("account:login")


            
 