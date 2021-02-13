"""middleware, creamos el archivo que es un .py y se usa por si necesitamos
que digamos un usuario llene cierta informacion antes de dejalor entrar 
a donde quiera ir.

En este proyecto se usa para que si alguien quiere entrar a ver los posts
debe tener una foto de perfil y una biography, si no los tiene aunque ingrese
a localhost:8000/posts la pagina lo redirige a actualizar esos datos y hasta 
que no lo haga no podra ir a posts. Pero es solo por ejemplo para saberlo"""

from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddle:
    
    #Empezamos con el constructor, como toda clase debe tener si va a 
    #tener funcionesy en este caso para el middleware debe recibir get_response
    def __init__(self, get_response):
        self.get_response = get_response
        
    
    #Ahora la funcion que va a realizar las validaciones para dejar ver los posts
    def __call__(self, request):
        #Primero verificamos que alguien este logueado
        if not request.user.is_anonymous:
            #Luego traemos el perfil que esta logueado
            profile = request.user.profile
            #Ahora le decimos que si no tiene los datos que queremos pues
            if not profile.picture or not profile.biography:
                #le decimos que no nos re-dirija si ya estamos en esa pagina ni tampoco
                #si hacemos logout, sino no podriamos desloguearnos nunca
                if request.path not in [reverse('users:update_profile'), reverse('users:logout')]:
                    #cuando cumple todo le decimos que nos dirija a llenar los datos
                    return redirect('users:update_profile')
        
        #si no es el caso sino que tiene ya todo lleno que siga
        response = self.get_response(request)
        return response
