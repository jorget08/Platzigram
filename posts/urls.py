# Importamos de nuestra app las vistas para poder mostrarlas en la url
from posts import views

#Importamos de django el manejo de las url
from django.urls import path

#en urlpatterns ponemos todos los links que perteneceran a esta app (estamos en posts)
#y lo haremos de forma ordenada para que se entienda 
urlpatterns = [
    #asi se llama para la forma modelo vista
   #path(
   #    route = '', 
   #    view = views.list_posts, 
   #    name = 'home'),
   
   #Y asi se llama para la forma de vista basado en clases:
   path(
       route = '',
       view = views.PostHomeView.as_view(),
       name = 'home'
   ),
    
    path(
        route = 'new/',
        view = views.CreatePostView.as_view(),
        name = 'create_post'
    ),
    
    path(
        route = '<int:pk>',
        view = views.DetailPostView.as_view(),
        name = 'detail'
    )
]