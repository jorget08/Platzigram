from django.shortcuts import render, redirect # ya viene render; redirect lo importamos para que redireccione
#al dejar entrar a un usuario

#importamos esto para la autenticacion del usuario
from django.contrib.auth import authenticate, login, logout

#importamos el decoradorpara que solo se pueda realizar al funcion de logout
#cuando la persona esta logeada
from django.contrib.auth.decorators import login_required

#importamos para hacer que una clase sea requerida, no con el decorador como es para las def
from django.contrib.auth.mixins import LoginRequiredMixin

#Importamos para usar el modelo de usuario en la class de mostrar el perfil
from django.contrib.auth.models import User

#importamos este modelo para pues actualizar el usuario(eL ProfileForm es para el basado en def) pues
#la UpdateView ya hace la magie del form
from users.forms import SignupForm #ProfileForm
#tambien importamos el modelo del signup para el signup
    
#importamos la vista generica que nos facilita django para el perfil de usuario
from django.views.generic import DetailView, FormView, UpdateView

#lo usamos para convertir la url despues de actualizar el perfil
from django.urls import reverse, reverse_lazy

#
from posts.models import Post

#
from users.models import Profile

#para login y demas
from django.contrib.auth import views

"""Para el login y logout vamos a usar las vistas de --> Authentication View(en la documentacion
de django) lo cual nos trar ya de porsi multiples vistas
This will include the following URL patterns:

accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']"""


"""ESTA ES LA FORMA BASADA EN FUNCIONES
def login_view(request):
    #El request extrae info pero con un metodo 'POST', este metodo lo generamos
    #en el login.html en el formulario asi: <form method="POST"--Ahi le estamos
    #diciendo que el formulario es un metodo 'POST' empezara a tomar info para el login
    if request.method == 'POST':
        #con estos 2 campos tomamos los datos que el usuario ingresa
        username = request.POST['username']
        password = request.POST['password']
        
        #Aqui compara si es usuario o no
        user = authenticate(username=username, password=password)
        #aqui si se valido que si es usuario lo deja entrar
        if user:
            login(request, user)
            return redirect('posts:home')
        #sino le manda la misma pantalla pero con un mensaje de error
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    
    #Este if lo ponemos para que alguien logeado, si intenta volver a la parte
    #de users/login lo redirecciones al inicio de posts pues ya se encuentra dentro y no ha cerrado al sesion 
    if request.method == 'GET':
            if request.user.is_authenticated:
                return redirect('posts:home')   
        
    return render(request, 'users/login.html')

"""
class LoginView(views.LoginView):
    #solo nos intereza edita el campo:
    template_name = 'users/login.html'
    
    #Tenemos que poner (LOGIN_REDIRECT_URL = '/') en setting.py para cambiar la direccion
    #que tiene por defecto el LoginView cuando se le da entrar para entrar; entre '' ponemos
    #La direccion a la que queremos que vaya, en este caso al home u inicio.


"""Basado en funciones
#Le ponemos el decoraro que indica que para que esta funcion/vista pueda
#llevarse a cabo tiene que estar logueado el usuario
@login_required
#Esta funcion/vista para le logout (son las 2 primeras lineas), ya la tercera
#linea es para redirigirlos a donde queramos
def logout_view(request):
    logout(request)
    return redirect('users:login')
"""

class LogoutView(LoginRequiredMixin, views.LogoutView):
    #solo definimos el template
    template_name = 'users/log_out.html'



"""Esto es de modelo basado en funciones

#Visa del signup
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    
    else:
        form = SignupForm()
    
    return render(request=request, template_name='users/signup.html', context={'form':form})

"""

class SignupView(FormView):
    template_name = 'users/signup.html'
    
    #Recibe el formulario que tendra (la clase de forms.py)
    form_class = SignupForm
    
    #Y recibe a donde lo vamos a redirigir
    #en lugar de un reverse normal este evalua el link, y solo lo usa cuando lo necesita
    #asi no esta en 2 plano y consume menos ram
    success_url = reverse_lazy('users:login')

    #SIEMPRE QUE USAMOS UN FORMVIE TENEMOS QUE SOBREESCRIBIR EL METODO: form_valid
    def form_valid(self, form):
        
        #guardamos el form para que le los datos se creen en la base de datos
        form.save()
        
        #ya viene cone l emtodo y es lo que se devuelve 
        return super().form_valid(form)

"""Basado en funciones:

@login_required
#Ahora crearemos la vista para cuando el usuario quiere actualizar los datos
def update_profile(request):
     #llamamos el perfil que esta en sesion para que lo muestre y llene los datos que queremos
    profile = request.user.profile
    
    #vanos a tomar los datos del formulario que el usuario va a meter implementando
    #esta vez los formularios de django
    if request.method == 'POST':
        #form sera una instancia del modelo ProfileForm(el que importamos)
        form = ProfileForm(request.POST, request.FILES)#request.FILES es para decirle que se van a enviar imagenes tambien
        #mis_valid para decirle que cuando envie todo cumpliendo con los campos haga esto:
        if form.is_valid():
            #guardamos los datos como: data; (form.cleaned_data -> esto es como viene internamente los datos que se pusieron)
            data = form.cleaned_data
            #ahora establecemos cada dato donde va
            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            #los guardamos ahora, para que queden ya guardados en la base de datos
            profile.save()
            
            #no podemos redirigir al url detail con redirecto por lo que la ruta recibe un dato
            # (osea por  route= '<str:username>/') asi que priumero debe convertirse asi:
            url = reverse('users:detail', kwargs={'username':request.user.username})
            
            #y ya ahora si redirigimos la url
            return redirect(url)
    else:
        form = ProfileForm()
    
    
    return render(request=request, template_name='users/update_profile.html', context={'profile': profile, 'user': request.user, 'form':form})
"""
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update_profile.html'
    
    #Definimos el modelo que va a usar
    model = Profile
    
    #Ahora decimos los campos que esta editanto
    fields = ['website', 'phone_number', 'biography', 'picture']

    #Vamos a sobreescribir este metodo para que haga el query y nos traiga el perfil
    #del usuario. Esta funcion Devuelve el objeto que muestra la vista.
    def get_object(self):
        #estamos regresando el perfil del usuario que se esta actualizando
        return self.request.user.profile
    
    #Con este metodo devolvemos la url que sucedera despues de enviada la actualizacion
    #del usuario
    def get_success_url(self):
        #Para eso primero traemos el 
        username = self.object.user.username
        return reverse_lazy('users:detail')




#pondermos para que sea requerido estar logueado para ver este perfil

#Para el perfil de usuario lo haremos por medio de una clase
#LoginRequiredMixin -> en lugar del decorador@login_required, se usa este cuando es una clase
class detail_user_view(LoginRequiredMixin, DetailView):
    #debemos definir el template
    template_name = 'users/detail.html'
    
    #queryset, es a partir de que conjunto de datos va a traer los datos y tenemos que definirlo
    #esto traera al usuario que queremos mostrar
    queryset = User.objects.all()
    
    #tenemos que definir tambien los 2 siguientes datos: slug_field y slug_url_kwarg
    
    #slug_field es un capo de texto unico, en este caso tenemos que nadie puede tener 
    #un nombre de usuario repetido ese seria nuestro slug, ya que es un string y es unico
    slug_field = 'username'
    
    #el slug_url_kwarg(keyword argument) debemos indicarlo y debe ser el lo mimso que pusimos
    #como la ruta que tiene en el path (route= '<str:username>/'), debe ser igual a lo que viene
    #despues del str:
    slug_url_kwarg = 'username'
    
    
    #el objeto que recibe el template (  {{ user.username }}, {{ user.profile.posts_count }}, etc.)
    #el objeto que recibe el tamplate es el user de lo que esta entre ({{ }})
    #para definir que ese si es el objeto aqui tambien hacemos:
    context_object_name = 'user'
    
    
    #sobreescribimos este metodo que ya viene en django y lo que hace es añardir
    #datos al contexto(context_object_name), en este caso lo que queremos agregar al contexto
    #son los posts que ha hecho el usuario asi cuando se mire el perfil del usuario
    #no esta solo la info sino que tambien sus posts
    def get_context_data(self, **kwargs):
        #taremos el contexto (crecordar que estamos sobreescribiendo el metodo)
        context = super().get_context_data(**kwargs)
        
        #le hace el query al objeto user(nos trae todo del user, info, posts, imagenes, todo)
        user = self.get_object()
        
        #añadimos al contesto la parte de posts; Post.objects.filter(user=user) -> con esto
        #estamos diciendo que filtre los posts que tiene el usuario(user azul) que fue el que 
        #definimos justo arriba (user = self.get_object()).
        #Luego solo lo ordenamos con el - para que sea del ultimo creoado al primero
        context["posts"] = Post.objects.filter(user=user).order_by('-created')
        return context
        #["posts"] es una nueva llave que se agrego al contexto
    