#Importamos los forms de django
from django import forms

#importamos para usarlo en la clase SignupForm dentro de la def clean_username para 
#poder realizar un query que se hizo
from django.contrib.auth.models import User

#importamos el modelo para la creacion del usuario en la def que lo guarda
from users.models import Profile

"""forms.Form y forms.ModelForm tiene el mismo uso. Se diferencian en que forms.ModelForm utiliza los models como base para crear el formulario.

   forms.Form crea un formulario si no se tiene como base un modelo."""


"""PARA EL MODELO BASADO EN FUNCIONES PUES LA VISTA GENERICA DE UPDATEVIEW YA HACE EL FORM


#al importar forms la clase que creamos debe heredar forms.Form
class ProfileForm(forms.Form):
    #Ponemos los valores que queremos que se se tomen del formulario
    #en este proyecto seran los campos que pueda editar el usuario de su perfil
    #los campos deben coincidir con los de la base de datos(lo que seria el max length y si es requerido o no)
   website = forms.URLField(max_length=200, required=True)
    #en este caso website es requerido porque asi pusimos el middelware
    
   biography = forms.CharField(max_length=500, required=True)
   phone_number = forms.CharField(max_length=20, required=False)
   picture = forms.ImageField()
    """
    
class SignupForm(forms.Form):
       
   #Por default aqui todos los valores vienen required si queremos alguno que no lo sea le ponemos el required en false y ya
   username = forms.CharField(min_length=4, max_length=50)
   #el widget para las contraseñas y/o datos que no queremos que se muestren
   password = forms.CharField(max_length=70, widget=forms.PasswordInput)
   password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput)
   first_name = forms.CharField(min_length=2, max_length=50)
   last_name = forms.CharField(min_length=2, max_length=50)
   email = forms.CharField(min_length=6, max_length=70,widget=forms.EmailInput)
   
   
   #este metodo (clean_(aqui el cmapo que queremos validar) ) es para validar un campo
   #es de django por el mismo import de forms
   def clean_username(self):
      #self.cleaned_data['username'] es la forma de llamar al campo username que el usuario ingresa
      username = self.cleaned_data['username']
      
      #User.objects.filter(username=username) este ya es un query a la base de datos que nos trae los
      #usuarios que tienen ese username, como lo hacemos para ver si ya esta en uso o no  lo que hacemos 
      #es ponerle el .exists() para que traiga un booleano de si existe o no
      username_exist = User.objects.filter(username=username).exists()
      if username_exist:
            #Si existe, devolvemos esto con lo que django se encarga de enviar el mensaje que ponemos 
            raise forms.ValidationError('Username is alredy in use')
      #Si no sucede ps devolvemos el campo
      return username
      
      
   #con este metodo, vamos a validar la contraseña y la confirmacion 
   #de la contraseña
   def clean(self):#Este metodo lo estamos sobre-escribiendo de django por lo que el ya nos trae
                   #los datos limpios y no como en el meodo de arriba(clean_username)  que tenemos
                   #que accderlos limpiando la data con self.cleaned_data
      data = super().clean()
      
      password = data['password']
      password_confirmation = data['password_confirmation']
      #miramos si no son iguales y enviamos mensaje
      if password != password_confirmation:
         raise forms.ValidationError('Passwords do not match')
      #si son iguales solo devolvemos la data y ya esta bien
      return data
   
   
   #Creamos este metodo para el guardado de los datos en la base de datos
   def save(self):
      #self.cleaned_data[] es la forma de llamar al campo username que el usuario ingresa
      data = self.cleaned_data
      #como estamos guardando el usuario en la base de datos el passwor_confirmation no
      #nos sirve para nada asi que lo sacamos de la data
      data.pop('password_confirmation')
      
      #para crear el usuaro y como lo estamos ahciendo con django seria User.objects.create_user
      #y la info que le pasaremos sera todo el diccionario de data, pero para no poner
      #dato por dato(ej: email=data['email']) enviamos el diccionarioo completo con el **data
      user = User.objects.create_user(**data)
      
      #ahora creamos la parte dle perfil tambien para la base de datos
      profile = Profile(user = user)
      profile.save()