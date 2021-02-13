from django.db import models# ya viene por defecto

#la importamos para relacionar a los post con los usuarios
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    #Empezamos con las relaciones:
    #Aqui ponemos la relacion basado en la llave foranea de los posts con los usuarios
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #Aqui esta la relacion de los posts con los perfiles por la llave foraneo igual
    #En este caso para no tener que importar (como arriba, en la anteriot), lo que hacemso es pasarle
    #en el primer parametro el nombre de la app(nosotros creamos las app que son las carpetas de cada cosa)
    #asi que pasamos el nombre de la app entre '' y luego el nombre del modelo (de la clase que queramos en el 
    #models.py de la app(carpeta))y asi no hay necesidad de importar nada
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    
    
    #Ahora definimos lo que va a tener posts
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/fotos')#Donde esta almacenada la foto
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    #Creamos una funcion para poder devolver los parametros que queremos como string
    def __str__(self):
        return f'{self.title} by @{self.user.username}'