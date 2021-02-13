from django.db import models #viene por defecto

# importamos para poder crer la clase usuario que tendra los 
# valores de la tabla por defecto que nos da django, como son:
# id, password, last_login, is_superuser,username,first_name,
# email, is_staff,is_active,date_joined, last_name
from django.contrib.auth.models import User

#creamos la clase perfil de usuario
class Profile(models.Model):
    #El uso de OneToTOneField hace una relacion de 1:1(SQL) entre usuario y perfeil
    #(un usuario solo puede tener un perfil y un perfil solo puede tener un usuario)
    user = models.OneToOneField(User, on_delete=models.CASCADE)#on_delete=models.CASCADE -- Esto significa que si se llega a borrar uno se borra el otro de una tambien
    
    #añadimos los datos que queremos y que no vienen en django
    #los tipo de dato de django para sql son lo de models.bla_bla
    #blank significa que el espacio puede estar en blanco
    
    website = models.URLField(max_length = 200, blank = True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    
    #upload de donde se va a cargar la imagen
    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)
    
    #Para que de la fecha y hora en que se creo el usuario
    created = models.DateTimeField(auto_now_add=True)
    
    #Para conocer fecha y hora en que se modifique este perfil
    modified = models.DateTimeField(auto_now=True)
    
    #Creamos una funcion para poder devolver el nombre de usuario como string
    def __str__(self):
        return self.user.username