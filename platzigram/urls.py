"""Platzigram URLs module."""
#propio de django, que importamos para manejar las url 
from django.urls import path, include

from django.contrib import admin

#importamos para poder que se vean las imagenes de los usuarios y eso
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('admin/', admin.site.urls),
    
    #vamos a separar las urls para segmentarlas por cada app,
    #Lo primero que hacemos es poner el path con el include y el include recibe 2 argumentos
    #los cuales son: la app con el "." del archivo donde tendremos las url en esa app
    #en nuestro caso creamos un archivo urls.py
    path('', include(('posts.urls', 'post'), namespace='posts')),
    
    #Ahora haremos lo mismo pero con todo lo que tiene que ver con las urls que se manejan
    #en la parte de usuarios; en esta el primer campo del path como tenemos todo los urls 
    #con users/login, users/signup, etc. Lo que hacemos es porner el users y ya luego el include
    path ('users/', include(('users.urls', 'users'), namespace='users'))
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#Esto es 
#paraque se puedan ver las imagenes de los usuarios, no los posts, sino
#la de los usuarios de la plataforma
#Tambiens e tuvo que editar el archivo de setting 
