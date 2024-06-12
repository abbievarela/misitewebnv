from typing import List

from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse
from appcodernv.models import Curso, Profesor, Avatar
from appcodernv.forms import CursoFormulario, ProfesorFormulario, UserRegisterForm, UserEditForm, AvatarFormulario

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

import string
import random

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView

# Create your views here.

def curso(request):
    curso = Curso(nombre="Desarrollo web Python django", camada="54145")
    curso.save()
    documentoDeTexto = f"--->Curso: {curso.nombre}   Camada: {curso.camada}"
    return HttpResponse(documentoDeTexto)

@login_required
def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "appcodernv/inicio.html", {"url": avatares[0].imagen.url if avatares else None})

def estudiantes(request):
    return render(request, "appcodernv/estudiantes.html")

def entregables(request):
    return render(request, "appcodernv/entregables.html")

def cursos(request):
    if request.method == 'POST':
        miFormulario = CursoFormulario(request.POST)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            curso = Curso(nombre=informacion['curso'], camada=informacion['camada'])
            curso.save()
            return redirect('inicio')
    else:
        miFormulario = CursoFormulario()
    return render(request, "appcodernv/cursos.html", {"miFormulario": miFormulario})

def profesores(request):
    if request.method == 'POST':
        miFormulario = ProfesorFormulario(request.POST)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            profesor = Profesor(
                nombre=informacion['nombre'],
                apellido=informacion['apellido'],
                email=informacion['email'],
                profesion=informacion['profesion']
            )
            profesor.save()
            return redirect('inicio')
    else:
        miFormulario = ProfesorFormulario()
    return render(request, "appcodernv/profesores.html", {"miFormulario": miFormulario})

def buscar(request):
    if request.GET.get("camada"):
        camada = request.GET['camada']
        cursos = Curso.objects.filter(camada__icontains=camada)
        return render(request, "appcodernv/inicio.html", {"cursos": cursos, "camada": camada})
    else:
        return render(request, "appcodernv/inicio.html", {"respuesta": "No enviaste datos"})

def leerProfesores(request):
    profesores = Profesor.objects.all()
    contexto = {"profesores": profesores}
    return render(request, "appcodernv/leerProfesores.html", contexto)

def eliminarProfesor(request, profesor_nombre):
    profesor = Profesor.objects.get(nombre=profesor_nombre)
    profesor.delete()
    return redirect('leerProfesores')

def editarProfesor(request, profesor_nombre):
    profesor = Profesor.objects.get(nombre=profesor_nombre)
    if request.method == 'POST':
        miFormulario = ProfesorFormulario(request.POST)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            profesor.nombre = informacion['nombre']
            profesor.apellido = informacion['apellido']
            profesor.email = informacion['email']
            profesor.profesion = informacion['profesion']
            profesor.save()
            return redirect('inicio')
    else:
        miFormulario = ProfesorFormulario(initial={
            'nombre': profesor.nombre,
            'apellido': profesor.apellido,
            'email': profesor.email,
            'profesion': profesor.profesion
        })
    return render(request, "appcodernv/editarProfesor.html", {"miFormulario": miFormulario, "profesor_nombre": profesor_nombre})

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
    fields = ['nombre', 'camada']

class CursoDelete(DeleteView):
    model = Curso
    success_url = "/appcodernv/curso/list"

def logout_request(request):
    logout(request)
    return redirect("inicio")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contra)
            if user is not None:
                login(request, user)
                return render(request, "appcodernv/inicio.html", {"mensaje": f"Bienvenido {usuario}"})
            else:
                return render(request, "appcodernv/inicio.html", {"mensaje": "Error, datos incorrectos"})
        else:
            return render(request, "appcodernv/inicio.html", {"mensaje": "Error, formulario erroneo"})
    form = AuthenticationForm()
    return render(request, "appcodernv/login.html", {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "appcodernv/inicio.html", {"mensaje": "Usuario Creado :)"})
    else:
        form = UserRegisterForm()
    return render(request, "appcodernv/registro.html", {"form": form})

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            usuario.email = informacion['email']
            usuario.set_password(informacion['password1'])
            usuario.save()
            return redirect('inicio')
    else:
        miFormulario = UserEditForm(initial={'email': usuario.email})
    return render(request, "appcodernv/editarPerfil.html", {"miFormulario": miFormulario, "usuario": usuario})

@login_required
def agregarAvatar(request):
    if request.method == 'POST':
        miFormulario = AvatarFormulario(request.POST, request.FILES)
        if miFormulario.is_valid():
            u = User.objects.get(username=request.user)
            avatar = Avatar(user=u, imagen=miFormulario.cleaned_data['imagen'])
            avatar.save()
            return redirect('inicio')
    else:
        miFormulario = AvatarFormulario()
    return render(request, "appcodernv/agregarAvatar.html", {"miFormulario": miFormulario})

def urlImagen():
    return "/media/avatares/logo.png"
