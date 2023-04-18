from django.contrib.auth import views
from django.urls import path
from .views import (
    ArticelList,
    ArticelCreate ,
    ArticelUpdate , 
    ArticelDeleteView ,
    Profile,
    Login,
    PasswordChange,
)

app_name= "account"
urlpatterns = [
    path('', ArticelList.as_view(), name="home"),
    path('articel/create', ArticelCreate.as_view(), name="articel-create"),
    path('articel/update/<int:pk>', ArticelUpdate.as_view(), name="articel-update"),
    path('articel/delete/<int:pk>', ArticelDeleteView.as_view(), name="articel-delete"),
    path('profile/', Profile.as_view(), name="profile"),
]