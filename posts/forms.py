from django import forms

#importamos el modelo que tenemos de los post
from posts.models import Post

#hereda de los forms de django
class PostForm(forms.ModelForm):
    """forms.Form y forms.ModelForm tiene el mismo uso. Se diferencian en que forms.ModelForm utiliza los models como base para crear el formulario.
       forms.Form crea un formulario si no se tiene como base un modelo."""
    
    #se usa una clase mete para las configuraciones de la clase en general
    #segun indicaciones de la docuemntacion por el ModelForm ya que es otro tipo de form 
    #al que usamos en el de users
    class Meta:
        
        #el modelo del que armaremos el nuevo post
        model = Post
        
        #los campos que se van a usar
        fields = ('user', 'profile', 'title' , 'photo')