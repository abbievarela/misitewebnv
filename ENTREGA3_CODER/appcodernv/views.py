# Create your views here.
#def hello (request):
  #   return HttpResponse ("HOLA")

from typing import List

from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse
from appcodernv.models import Curso, Profesor, Avatar
from appcodernv.forms import CursoFormulario, ProfesorFormulario, UserRegisterForm,UserEditForm,AvatarFormulario

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User


#Para la prueba unitaria
import string
import random


#Para el login

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

#Decorador por defecto
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView


# Create your views here.

def curso(request):

      curso =  Curso(nombre="Desarrollo web Python django", camada="54145")
      curso.save()
      documentoDeTexto = f"--->Curso: {curso.nombre}   Camada: {curso.camada}"


      return HttpResponse(documentoDeTexto)

@login_required
def inicio(request):

      avatares = Avatar.objects.filter(user=request.user.id)
      
      return render(request, "appcodernv/inicio.html", {"url":avatares[0].imagen.url})



def estudiantes(request):

      return render(request, "appcodernv/estudiantes.html")


def entregables(request):

      return render(request, "appcodernv/entregables.html")


def cursos(request):

      if request.method == 'POST':

            miFormulario = CursoFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  curso = Curso (nombre=informacion['curso'], camada=informacion['camada']) 

                  curso.save()

                  return render(request, "appcodernv/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= CursoFormulario() #Formulario vacio para construir el html

      return render(request, "appcodernv/cursos.html", {"miFormulario":miFormulario})




def profesores(request):

      if request.method == 'POST':

            miFormulario = ProfesorFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data
                  """
                  #CASO DE PRUEBA
                  KEY_LEN = 20
                  keylistNombre = [random.choice((string.ascii_letters + string.digits)) for i in range(KEY_LEN)]
                  nombrePrueba = "".join(keylistNombre)

                  print(f"---->Pueba con: {nombrePrueba} ")
                  """
                  profesor = Profesor (nombre=informacion['nombre'], apellido=informacion['apellido'],
                   email=informacion['email'], profesion=informacion['profesion']) 

                  profesor.save()

                  return render(request, "appcodernv/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= ProfesorFormulario() #Formulario vacio para construir el html

      return render(request, "appcodernv/profesores.html", {"miFormulario":miFormulario})






def buscar(request):

      if  request.GET["camada"]:

	      #respuesta = f"Estoy buscando la camada nro: {request.GET['camada'] }" 
            camada = request.GET['camada'] 
            cursos = Curso.objects.filter(camada__icontains=camada)

            return render(request, "appcodernv/inicio.html", {"cursos":cursos, "camada":camada})

      #else: 

	    #respuesta = "No enviaste datos"
      # return render(request, "appcodernv/inicio.html", {"respuesta":respuesta})



def leerProfesores(request):

      profesores = Profesor.objects.all() #trae todos los profesores

      contexto= {"profesores":profesores} 

      return render(request, "appcodernv/leerProfesores.html",contexto)



def eliminarProfesor(request, profesor_nombre):

      profesor = Profesor.objects.get(nombre=profesor_nombre)
      profesor.delete()
      
      #vuelvo al menú
      profesores = Profesor.objects.all() #trae todos los profesores

      contexto= {"profesores":profesores} 

      return render(request, "appcodernv/leerProfesores.html",contexto)



def editarProfesor(request, profesor_nombre):

      #Recibe el nombre del profesor que vamos a modificar
      profesor = Profesor.objects.get(nombre=profesor_nombre)

      #Si es metodo POST hago lo mismo que el agregar
      if request.method == 'POST':

            miFormulario = ProfesorFormulario(request.POST) #aquí mellega toda la información del html

            print(miFormulario)

            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data

                  profesor.nombre = informacion['nombre']
                  profesor.apellido = informacion['apellido']
                  profesor.email = informacion['email']
                  profesor.profesion = informacion['profesion']

                  profesor.save()

                  return render(request, "appcodernv/inicio.html") #Vuelvo al inicio o a donde quieran
      #En caso que no sea post
      else: 
            #Creo el formulario con los datos que voy a modificar
            miFormulario= ProfesorFormulario(initial={'nombre': profesor.nombre, 'apellido':profesor.apellido , 
            'email':profesor.email, 'profesion':profesor.profesion}) 

      #Voy al html que me permite editar
      return render(request, "appcodernv/editarProfesor.html", {"miFormulario":miFormulario, "profesor_nombre":profesor_nombre})




class CursoList(ListView):

      model = Curso 
      template_name = "appcodernv/cursos_list.html"



class CursoDetalle(DetailView):

      model = Curso
      template_name = "appcodernv/curso_detalle.html"



class CursoCreacion(CreateView):

      model = Curso
      success_url = "/appcodernv/curso/list"
      fields = ['nombre', 'camada']


class CursoUpdate(UpdateView):

      model = Curso
      success_url = "/appcodernv/curso/list"
      fields  = ['nombre', 'camada']


class CursoDelete(DeleteView):

      model = Curso
      success_url = "/appcodernv/curso/list"




def logout_request(request):
      logout(request)
     
      return redirect("inicio")
     

def login_request(request):


      if request.method == "POST":
            form = AuthenticationForm(request, data = request.POST)

            if form.is_valid():
                  usuario = form.cleaned_data.get('username')
                  contra = form.cleaned_data.get('password')

                  user = authenticate(username=usuario, password=contra)

            
                  if user is not None:
                        login(request, user)
                       
                        return render(request,"appcodernv/inicio.html",  {"mensaje":f"Bienvenido {usuario}"} )
                  else:
                        
                        return render(request,"appcodernv/inicio.html", {"mensaje":"Error, datos incorrectos"} )

            else:
                        
                        return render(request,"appcodernv/inicio.html" ,  {"mensaje":"Error, formulario erroneo"})

      form = AuthenticationForm()

      return render(request,"appcodernv/login.html", {'form':form} )



def register(request):

      if request.method == 'POST':

            #form = UserCreationForm(request.POST)
            form = UserRegisterForm(request.POST)
            if form.is_valid():

                  username = form.cleaned_data['username']
                  form.save()
                  return render(request,"appcodernv/inicio.html" ,  {"mensaje":"Usuario Creado :)"})


      else:
            #form = UserCreationForm()       
            form = UserRegisterForm()     

      return render(request,"appcodernv/registro.html" ,  {"form":form})



@login_required
def editarPerfil(request):

      #Instancia del login
      usuario = request.user
     
      #Si es metodo POST hago lo mismo que el agregar
      if request.method == 'POST':
            miFormulario = UserEditForm(request.POST) 
            if miFormulario.is_valid:   #Si pasó la validación de Django

                  informacion = miFormulario.cleaned_data
            
                  #Datos que se modificarán
                  usuario.email = informacion['email']
                  usuario.password1 = informacion['password1']
                  usuario.password2 = informacion['password1']
                  usuario.save()

                  return render(request, "appcodernv/inicio.html") #Vuelvo al inicio o a donde quieran
      #En caso que no sea post
      else: 
            #Creo el formulario con los datos que voy a modificar
            miFormulario= UserEditForm(initial={ 'email':usuario.email}) 

      #Voy al html que me permite editar
      return render(request, "appcodernv/editarPerfil.html", {"miFormulario":miFormulario, "usuario":usuario})



@login_required
def agregarAvatar(request):
      if request.method == 'POST':

            miFormulario = AvatarFormulario(request.POST, request.FILES) #aquí mellega toda la información del html

            if miFormulario.is_valid:   #Si pasó la validación de Django


                  u = User.objects.get(username=request.user)
                
                  avatar = Avatar (user=u, imagen=miFormulario.cleaned_data['imagen']) 
      
                  avatar.save()

                  return render(request, "appcodernv/inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= AvatarFormulario() #Formulario vacio para construir el html

      return render(request, "appcodernv/agregarAvatar.html", {"miFormulario":miFormulario})


def urlImagen():

      return "/media/avatares/logo.png"