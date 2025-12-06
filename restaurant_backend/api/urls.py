from django.urls import path
from . import views


urlpatterns =[
    path('register/', view=views.register),
    path('login/', view=views.login),
    path('update_user/<str:email>/', view=views.update_user),
    path('delete_user/', view=views.delete_user),

    path('get_menu/', view=views.get_menu),
    path('admin_only/', view=views.createmenu),
    path('update_menu/<str:name>/', view=views.update_menu),
    path('delete_item/', view=views.delete_item)
]