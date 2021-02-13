# Create your views here.
"""Esto es para el modelo basado en funciones
#Django
from django.shortcuts import render, redirect"""

"""Esto es para el modelo basado en funciones
#importamos el decorador ponerlo sobre la funcion que muestra esta vista
from django.contrib.auth.decorators import login_required"""

#importamos el metodo de formulario que tenemos en el forms.py
from posts.forms import PostForm

#importamos para usarlo en el list_post ya que este le da el modelo de como es un post para que la def lo muestre
from posts.models import Post

"""estos los importamos para el modelo vista basado en clases, aunque usamos el modelos Post"""
#importamos para hacer que una clase sea requerida, no con el decorador como es para las def
from django.contrib.auth.mixins import LoginRequiredMixin

#importamos la vista generica que nos facilita django
from django.views.generic import ListView, DetailView, CreateView

#
from users.models import Profile

#en lugar de un reverse normal este evalua el link, y solo lo usa cuando lo necesita
#asi no esta en 2 plano y consume menos ram
from django.urls import reverse_lazy

"""
Esto que esta comentado es la forma en que se hace el desarrollo basado en modelos
y funcioana exactamente igual que el sistema basado en clases, lo que pasa con el basado
en clases es que nos dan la capacidad de estructurar y reutilizar el código usando la 
programación orientada a objetos a nuestro favor. Con este método, al final, el código 
será lo más entendible y modularizado posible. 

#este decorador lo que hace es que no deja que se muestre nada de la funcion(
#que es todo), sin que un usuario se loguee
@login_required
def list_posts(request):#esta funcion es la que muestra los posts
    
    #tomamos el modelo importado (Post) y con al sintaxis que le sigue le estamos
    #diciendo que tariga todos los que hallan de cada uno de esos, osea post por post
    #y que los muestre en orden por la fecha de creacion. se le pone el - adelante para que lo traiga
    #del ultimo creado al primero, si queremso del primero al ultimo no le pones -
    posts = Post.objects.all().order_by('-created')
    
    
    #El render que importamos lo que hace es pedir el request y el template
    #de forma obligatoria y va directo a la carpeta templates que creamos y toma el que  llamemos
    #y recibe tambien un diccionario con los datos que tiene, el dic es opcional
    return render(request, 'posts/feed.html',{'posts':posts})
"""

"""Ahora lo haremos con vistas basadas en clases ya no en modelos(def)"""
class PostHomeView(LoginRequiredMixin, ListView):
    #se debe definr el template de la vista
    template_name = 'posts/feed.html'
    
    #definimos el modelo que tiene cada post
    model = Post
    
    #como se va a ordenar(de ultimo creado a primero)
    ordering = ('-created',)
    
    #ahora la paginacion, que es el numero de post que va a mostrar, ej si le ponemos 2 va a mostrar solo
    #2 post en la pagina y para seguir viendo los otros pues tenemos que darle a next pagey ahi
    #veremos los otros 2 y asi sucesivamente.
    #los botones para eso se ponen en pagination.html con boostrap
    paginate_by = 30
    
    #el objeto que recibe el template -osea lo html que tiene por ejemplo
    # estos campos- ({{ post.profile.picture.url }}, {{ post.photo.url }}, etc.)
    #el objeto que recibe el tamplate es el user de lo que esta entre ({{ }})
    #para definir que ese si es el objeto aqui tambien hacemos:
    context_object_name = 'posts'
    
"""
Esto que esta comentado es la forma en que se hace el desarrollo basado en modelos
y funcioana exactamente igual que el sistema basado en clases, lo que pasa con el basado
en clases es que nos dan la capacidad de estructurar y reutilizar el código usando la 
programación orientada a objetos a nuestro favor. Con este método, al final, el código 
será lo más entendible y modularizado posible. 

@login_required
def create_post(request):
    if request.method == 'POST':
        #decimos que el formulario traera datos, request.FILES dice que tambien traera imagenes
        form = PostForm(request.POST, request.FILES)
        #si carga todo bien en la pag
        if form.is_valid():
            #se guarda el post nuevo
            form.save()
            #y redirigimas al inicio
            return redirect('posts:home')

    else:
        form = PostForm()
    
    return render(request=request, template_name='posts/new.html', context={'form': form, 'user': request.user, 'profile': request.user.profile})

"""

"""Ahora lo haremos con vistas basadas en clases ya no en modelos(def)"""

class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'posts/new.html'
    
    #Recibe el formulario que tendra (la clase) de forms.py
    form_class = PostForm
    
    #Y recibe a donde lo vamo a redirigir
    #en lugar de un reverse normal este evalua el link, y solo lo usa cuando lo necesita
    #asi no esta en 2 plano y consume menos ram
    success_url = reverse_lazy('posts:home')

    #sobreescribimos este metodo que ya viene en django y lo que hace es añardir
    #datos al contexto
    def get_context_data(self, **kwargs):
        #taremos el contexto (crecordar que estamos sobreescribiendo el metodo)
        context = super().get_context_data(**kwargs)
        
        #Va a agregar una nueva llave que sera ['user']
        #self.request.user -> nos trae el usuario que esta creando el post
        #Va a agregar una nueva llave que sera ['profile']
        #self.request.user -> nos trae el perfil del usuario que esta creando el post
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context
        """El contexto, lo que hace darle el sentido a la vista sobre que cosas son las que se
        relacionan para la vista que estamos haciendo. Por ejemplo: en esta vista se relaciona el 
        formulario(form_class = PostForm) """
        
    


#El detalle de cada post
class DetailPostView(LoginRequiredMixin, DetailView):
    #debemos definir el template
    template_name = 'posts/detail.html'
    
    #querysetqueryset, es a partir de que conjunto de datos va a traer los datos y tenemos que definirlo
    #esto traera el Post(modelo) que queremos mostrar
    queryset = Post.objects.all()
    
    
    #el objeto que recibe el template (  {{ post.photo.url }}, {{ post.created }}, etc.)
    #el objeto que recibe el tamplate es el post de lo que esta entre ({{ }})
    #para definir que ese si es el objeto aqui tambien hacemos:
    context_object_name = 'post'