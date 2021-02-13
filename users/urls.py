#Importamos de nuestra app las vistas para poder mostrarlas
from users import views

#importmaos de django urls el path para manejar las urls
from django.urls import path


urlpatterns = [

    #ruta de login
    path(
        route = 'login',
        view = views.LoginView.as_view(),
        name = 'login'
    ),
    
    #ruta de logout
    path(
        route = 'logout/',
        view = views.LogoutView.as_view(),
        name = 'logout'
    ),
    
    #ruta de registro
    path(
        route = 'signup',
        view = views.SignupView.as_view(),
        name = 'signup'
    ),
    
    #ruta de actulizacion de perfil POR BASADO EN FUNCIONES
    #path(
    #    route = 'me/profile/',
    #    view = views.update_profile,
    #    name = 'update_profile'
    #),
    path(
        route = 'me/profile/',
        view = views.UpdateProfileView.as_view(),
        name = 'update_profile'
    ),
    
    #ruta de perfil del usuario
    #Importante ponerlo de ultimo pues al tener '<str:username>/'(sirve para que 
    #en la url aparezca el nombre dle usuario), al tenerlo puede tomar como usuario las rutasque estan abajo
    #asi que para que no interfiera mejro lo ponemos de ultimo
    #Como esta vista fue hecha como clase y no como funcion la vista cambia asi:
    path(
        route= '<str:username>/',
        #detail_user_view es una clase que creamos para la vista, y para qu ela clase se 
        #comporte como una vista le ponemos el .as_view()
        view = views.detail_user_view.as_view(),
        name = 'detail'
    )
]
