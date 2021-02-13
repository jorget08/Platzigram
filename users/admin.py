#ya viene
from django.contrib import admin
#necesaria para la clase UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#importamos los modelos que usaremos
from users.models import Profile #usado en la class ProfileAdmin

from django.contrib.auth.models import User

# Con el decorador registramos el perfil de usuario en admin de django
@admin.register(Profile)
# Creamos la clase para hacer todas las modificaciones que queramos
#en la parte de admin de django(url/admin)
class ProfileAdmin(admin.ModelAdmin):
    
    #Aqui pondremos como lista lo que queremos que nos muestre
    #sobre los usuarios que solo nu nombre, y no solo lo que quiero ver
    #sino en el orden en que lo quiero vor y/o mostrar
    list_display = ('pk', 'user', 'phone_number', 'website', 'picture')
    
    #Ahora esto es para decir los campos que queramos que
    #al oprimir click sobre ellos nos lleven al perfil del usuario
    list_display_links = ('pk', 'user')
    
    #Ahor con este parametro de admin(como los anteriores), podemos poner
    #que campos queremos que se editen en la vista sin tener que entrar
    #en el perfil para editarlo
    #Al ser una tupla "()" si tiene 1 solo elemento debe teneruna , antes del )
    list_editable = ('phone_number', 'website')
    
    #Para agregar una barra de busqueda en la vista de perfiles de usuario 
    #usamos el siguiente parametro y dentro pones los campos que vamos
    #a habilitar para que se busqeu por ellos, por ejemlo que se busque por los correo, o los numeros de telefono, etc
    """en este, debe tener siempre el __ (no entiendo porque no en el phone_number)"""
    #En esta barra de busqueda se pueden poner los camps que tiene 
    #tanto usuario como perfil de usuario pues estos 2 estan relacionados
    #ya que no puede haber 1 usuario con mas de un perfil, ni 1 perfil con
    #mas de un usuario
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone_number'
    )
    
    #Para tener una barra que filtra los perfiles con respecto a lo que queramos
    #para este caso sera: por si los usurios son activos o no, si son staff o no
    #(aun ni idea de que es staff pero viene con django), de cuando fueron creados
    #y de cuando fueron modificados por ultima vez
    '''Estos tambien tienen que tener el __'''
    list_filter = (
        'user__is_active',
        'user__is_staff',
        'created',
        'modified'
    )
    
    #Para no tener la informacion que va en users separada de la de profiel
    #sino que decidamos todo lo que queremos que se vea cuando ingresamos a ver un perfil,
    #osea definir todo lo que va a mostrar cuando entramos a un perfil a verlo
    #utilizamos este atributo:
    #Recordar que siempre en todos estos estamos trabajando con tuplas() y dicccionarios{}
    fieldsets = (
        ('Profile', 
            {'fields':(
                ('user', 'picture'),#asi van en la misma linea o seccion
                      )
            }
        ),
        # en este las comas (,) van asi afuera pues es una tupla que contiene solo 1 tupla y no 2
        # y ya sabemos que las tuplas deben tener al menos 2 elementons o sino dejar una ,
        
        
        ('Extra info',
            {'fields':(
                ('phone_number','website'),('biography')#la separacion de ),( indica que biography ira en otra linea o seccion
                      )
            }
        ),
        # aqui si hay mas de una tupla asi que no se necesita , despues del )

        #si no ponemos created y modified como readonly_fields no podemos ponerlos
        #aqui pues no nos deja poner campos que no pueden ser modificados (como estos 2)
        #asi que con el readonly_fields decimos que son solo de lectura y ya podemos ponerlos
        ('Metadata',
            {'fields':(
                ('created', 'modified'),
                      )
            }
        )
    )
    
    # Atributo para poder poner campos que no deben poderse editar para que sean solode lectura
    
    readonly_fields = ('created', 'modified')


"""Hasta el momemnto cuando creamos un usuario en la pagina nos toca despues crear el perfil
osea, tenemos que crear 2 veces la persona para tener todos los datos completos de la misma
pero acabemos con eso"""
#Vamos a crear esta clase para que cuando creamos un usuario se llenen tambien
#los datos de la creacion de perfil y se cree el perfil sin hacerlo en 2 pasos
# Esta clase se crea para que se vean los campos de perfil que se vana a llenar, al entrar 
# en crear nuevo usuario
class CreateUserProfile(admin.StackedInline):
    #esta clase por recibir de admin.StackedInline debe recibir los siguientes 3 atributos:
    
    #Lo primero que recibe es el modelo, el cual sera Profile (de models.py)
    model = Profile
    
    #lo segundo
    can_delete = False
    
    #lo tercero
    verbose_name_prural = 'profiles'#aqui pones el valor que queramos 'profiles o lo que sea xD'


# Luego tenemos que crear esta clase para que al darle guardar creando el usuario se guarde
# en la parte de perfil tambien
class UserAdmin(BaseUserAdmin):
    #esta clase debe recibir siempre: inlines
    inlines = (CreateUserProfile,)#la clase anterior; como es tupla se pone la ,
    
    #Como queremos que se nos listen los usuarios y lo que queremos que salga a la vista
    #sin tener que abrir ninguno en especifico
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )
    
# A diferencia de la primera clase esta no tenemos que registrarla con el decorador.
# Lo que se hace es desregistrarla lo que ya existe por default en django y luego registrar la nueva(UserAdmin)
admin.site.unregister(User)#este modelo lo importamos para usarlo aqui y es el que viene por defecto; lo desregistramos
admin.site.register(User, UserAdmin)#Aqui registramos el nuevo modelo
