from django.urls import path
from .views import (
     ArticelList ,
     ArticelDetail ,
     CategoryList ,
     AuthorList ,
     ArticelPreview,
     SearchList
)



app_name="blog"
urlpatterns=[
    path('',ArticelList.as_view(),name="home"),
    #path('main',mainposts,name="mainposts"),
    path('page/<int:page>',ArticelList.as_view(),name="home"),
    path('preview/<int:pk>',ArticelPreview.as_view(),name="preview"),
    path("posts/<slug:slug>/", ArticelDetail.as_view() , name="detail"),
    path("category/<slug:slug>/", CategoryList.as_view() , name="category"),
    path("category/<slug:slug>/page/<int:page>", CategoryList.as_view() , name="category"),
    path("author/<slug:username>/", AuthorList.as_view() , name="author"),
    path("author/<slug:username>/page/<int:page>", AuthorList.as_view() , name="author"),
    path("search/", SearchList.as_view() , name="search"),
    path("search/page/<int:page>", SearchList.as_view() , name="search1"),

    ]