from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse,response
import requests
import json
from .models import sesion
import random
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def login(request):
    try:
        api_url = "http://127.0.0.1:8000/logueo"
        print(request.GET)
        datos = {
            "usuario": request.GET["usuario"],
            "password": request.GET["password"]
        }
        respuesta = requests.post(api_url, json=datos)
        response = json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        if respuesta.status_code == 200:
            id = random.randint(100, 99999)
            ses = sesion(id=id, token=response["token"], rol=response['rol'])
            ses.save()
            redireccion = f"/{response['rol']}/{str(ses.id)}"
            return redirect(redireccion)
        else:
            return render(request, "error.html", {"mensaje": response["message"]})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def renderLogin(request):
    return render(request, "login.html")

def closeSesion(request, id):
    try:
        ses = sesion.objects.get(id=id)
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/logueo"
        respuesta = requests.delete(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(respuesta.text)
        print(response["message"])
        redireccion = reverse('renderLogin')
        return redirect(redireccion)
    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "La sesión no existe."})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
    
def renderRH(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/RH"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "RH":
            return render(request, "RH.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
    
def registraOperario(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "RH":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("Registeo de operario")
            api_url = "http://127.0.0.1:8000/RH"
            print(request.GET)
            datos = {
                "cedula": request.GET["cedula"],
                "nombre": request.GET["nombre"],
                "modulo": request.GET["modulo"],
                "correoE": request.GET["correoE"],
                "telefono": request.GET["telefono"],
                "fechaN": request.GET["fechaN"],
                "direccion": request.GET["direccion"],
            }
            print(datos)
            respuesta = requests.post(api_url, json=datos, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha registrado la persona")
                return render(request, "RH.html", {"id": id, "registro_exitoso": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})    
    
def renderEditarOperario(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/RH"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "RH":
            return render(request, "editOperarios.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
        
    
    
def buscarOperario(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "RH":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de operario")
            print(request.GET)
            cedula = request.GET.get("cedulaEditar")
            api_url = f"http://127.0.0.1:8000/RH/{cedula}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la persona")
                return render(request, "editOperarios.html", {"id": id, "operario": response.get("operario")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)}) 
    
    
def editarOperario(request, id):
    try:
        if request.method == 'POST':
            ses = sesion.objects.get(id=id)
            headers = {"token": str(ses.token)}
            cedula = request.GET.get("cedula")
            api_url = f"http://127.0.0.1:8000/RH/{cedula}"
            print("url: ",api_url)
            datos = {key: value for key, value in request.POST.items() if value != ''}
            respuesta = requests.patch(api_url, json=datos, headers=headers)
            response = json.loads(respuesta.text)
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha actualizado a la persona")
                return render(request, "RH.html", {"id": id,"edicion_exitosa": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return HttpResponseBadRequest("Método no permitido")
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def buscarTodosOperario(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "RH":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de operario")
            print(request.GET)
            api_url = f"http://127.0.0.1:8000/RH"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la persona")
                return render(request, "deleteOperario.html", {"id": id, "operario": response.get("operario")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
       
def renderEliminarOperario(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/RH"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "RH":
            return render(request, "deleteOperario.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})      

def eliminarOperario(request, id):
    print("entro")
    try:
        ses = sesion.objects.get(id=id)
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/RH"
        datos = {
            "cedula": request.GET["cedula"]
        }
        respuesta = requests.delete(api_url, json=datos, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        if respuesta.status_code == 200:
            messages.add_message(request, messages.SUCCESS, "Se ha elminado la persona")
            return render(request, "RH.html", {"id": id,"eliminacion_exitoso": True})
        else:
            return render(request, "error.html", {"mensaje": response["message"]})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
     
def renderADMIN(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/ADMIN"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "ADMIN":
            return render(request, "ADMIN.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
    
def registraUsuario(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "ADMIN":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("Registeo de usuario")
            api_url = "http://127.0.0.1:8000/ADMIN"
            print(request.GET)
            datos = {
                "cedula": request.GET["cedula"],
                "nombre": request.GET["nombre"],
                "rol": request.GET["rol"],
                "usuario": request.GET["usuario"],
                "password": request.GET["password"],
                }
            print(datos)
            respuesta = requests.post(api_url, json=datos, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha registrado el usuario")
                return render(request, "ADMIN.html", {"id": id, "registro_exitoso": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})    
    
def renderEditarUsuario(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/ADMIN"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "ADMIN":
            return render(request, "editUsuarios.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
        
    
    
def buscarUsuarios(request, id):
    try:
        print("entra usuarios")
        ses = sesion.objects.get(id=id)
        if ses.rol == "ADMIN":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de usuario")
            print(request.GET)
            cedula = request.GET.get("cedulaEditar")
            api_url = f"http://127.0.0.1:8000/ADMIN/{cedula}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la persona")
                return render(request, "editUsuarios.html", {"id": id, "persona": response.get("persona")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)}) 
    
    
def editarUsuario(request, id):
    try:
        if request.method == 'POST':
            ses = sesion.objects.get(id=id)
            headers = {"token": str(ses.token)}
            cedula = request.GET.get("cedula")
            api_url = f"http://127.0.0.1:8000/ADMIN/{cedula}"
            print("url: ",api_url)
            datos = {key: value for key, value in request.POST.items() if value != ''}
            respuesta = requests.patch(api_url, json=datos, headers=headers)
            response = json.loads(respuesta.text)
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha actualizado a la persona")
                return render(request, "ADMIN.html", {"id": id,"edicion_exitosa": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return HttpResponseBadRequest("Método no permitido")
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def buscarTodosUsuario(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "ADMIN":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de usuarios")
            print(request.GET)
            api_url = f"http://127.0.0.1:8000/ADMIN"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la persona")
                return render(request, "deleteUsuarios.html", {"id": id, "persona": response.get("persona")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
       
def renderEliminarUsuario(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/RH"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "ADMIN":
            return render(request, "deleteUsuarios.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})      

def eliminarUsuario(request, id):
    print("entro")
    try:
        ses = sesion.objects.get(id=id)
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/ADMIN"
        datos = {
            "cedula": request.GET["cedula"]
        }
        respuesta = requests.delete(api_url, json=datos, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        if respuesta.status_code == 200:
            messages.add_message(request, messages.SUCCESS, "Se ha elminado la persona")
            return render(request, "ADMIN.html", {"id": id,"eliminacion_exitoso": True})
        else:
            return render(request, "error.html", {"mensaje": response["message"]})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
    
def renderPR(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/REFERENCIA"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        if ses.rol == "PRODUCCION":
            return render(request, "PRODUCCION.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
    
def registraReferencia(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("Registeo de usuario")
            api_url = "http://127.0.0.1:8000/REFERENCIA"
            print(request.GET)
            datos = {
                "referenciaC": request.GET["referenciaC"],
                "color": request.GET["color"],
                "talla": request.GET["talla"],
                "tipoPrenda": request.GET["tipoPrenda"],
                "SAM": request.GET["SAM"],
                }
            print(datos)
            respuesta = requests.post(api_url, json=datos, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha registrado la referencia")
                return render(request, "PRODUCCION.html", {"id": id, "registro_exitoso": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})    
    
def renderEditarReferencia(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/REFERENCIA"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "PRODUCCION":
            return render(request, "editReferencias.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
        
    
    
def buscarReferencias(request, id):
    try:
        print("entra Referencias")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de referencias")
            print(request.GET)
            referencias = request.GET.get("referenciaEditar")
            api_url = f"http://127.0.0.1:8000/REFERENCIA/{referencias}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la referencia")
                return render(request, "editReferencias.html", {"id": id, "referenica": response.get("referenica")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)}) 
    
    
def editarReferencia(request, id):
    try:
        if request.method == 'POST':
            ses = sesion.objects.get(id=id)
            headers = {"token": str(ses.token)}
            SKU = request.GET.get("SKU")
            api_url = f"http://127.0.0.1:8000/REFERENCIA/{SKU}"
            print("url: ",api_url)
            datos = {key: value for key, value in request.POST.items() if value != ''}
            respuesta = requests.patch(api_url, json=datos, headers=headers)
            response = json.loads(respuesta.text)
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha actualizado la referencia")
                return render(request, "PRODUCCION.html", {"id": id,"edicion_exitosa": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return HttpResponseBadRequest("Método no permitido")
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def buscarTodosReferencias(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de REFERENCIAS")
            print(request.GET)
            api_url = f"http://127.0.0.1:8000/REFERENCIA"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la referencia")
                return render(request, "deleteReferencia.html", {"id": id, "referenica": response.get("referenica")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
       
def renderEliminarReferencia(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/REFERENCIA"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "PRODUCCION":
            return render(request, "deleteReferencia.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})      

def eliminarReferencia(request, id):
    print("entro")
    try:
        ses = sesion.objects.get(id=id)
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/REFERENCIA"
        datos = {
            "SKU": request.GET["SKU"]
        }
        respuesta = requests.delete(api_url, json=datos, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        if respuesta.status_code == 200:
            messages.add_message(request, messages.SUCCESS, "Se ha elminado la referencia")
            return render(request, "PRODUCCION.html", {"id": id,"eliminacion_exitoso": True})
        else:
            return render(request, "error.html", {"mensaje": response["message"]})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
              

def registraOrden(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print("Registeo de Op")
            api_url = "http://127.0.0.1:8000/ORDEN"
            print(request.GET)
            datos = {
                "referencia": request.GET["referencia"],
                "color": request.GET["color"],
                "talla": request.GET["talla"],
                "modulo": request.GET["modulo"],
                "cantidad": request.GET["cantidad"],
                }
            print(datos)
            respuesta = requests.post(api_url, json=datos, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha registrado la Orden")
                return render(request, "PRODUCCION.html", {"id": id, "registro_exitoso_op": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})    
    
def renderEditarOrden(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/ORDEN"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "PRODUCCION":
            return render(request, "editOrden.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
        
    
    
def buscarOrden(request, id):
    try:
        print("entra Orden")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de Orden")
            print(request.GET)
            orden = request.GET.get("ordenEditar")
            api_url = f"http://127.0.0.1:8000/ORDEN/{orden}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la orden")
                return render(request, "editOrden.html", {"id": id, "orden": response.get("orden")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)}) 
    
    
def editarOrden(request, id):
    try:
        if request.method == 'POST':
            ses = sesion.objects.get(id=id)
            headers = {"token": str(ses.token)}
            orden = request.GET.get("orden")
            api_url = f"http://127.0.0.1:8000/ORDEN/{orden}"
            print("url: ",api_url)
            datos = {key: value for key, value in request.POST.items() if value != ''}
            respuesta = requests.patch(api_url, json=datos, headers=headers)
            response = json.loads(respuesta.text)
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha actualizado la Orden")
                return render(request, "PRODUCCION.html", {"id": id,"edicion_exitosa_Op": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return HttpResponseBadRequest("Método no permitido")
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def buscarTodosOrden(request, id):
    try:
        print("entra")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("busca de Ordenes")
            print(request.GET)
            api_url = f"http://127.0.0.1:8000/ORDEN"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la orden")
                return render(request, "deleteOrden.html", {"id": id, "orden": response.get("orden")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
       
def renderEliminarOrden(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/ORDEN"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "PRODUCCION":
            return render(request, "deleteOrden.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})      

def eliminarOrden(request, id):
    print("entro")
    try:
        ses = sesion.objects.get(id=id)
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/ORDEN"
        datos = {
            "orden": request.GET["orden"]
        }
        respuesta = requests.delete(api_url, json=datos, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        if respuesta.status_code == 200:
            messages.add_message(request, messages.SUCCESS, "Se ha elminado la orden")
            return render(request, "PRODUCCION.html", {"id": id,"eliminacion_exitoso_Op": True})
        else:
            return render(request, "error.html", {"mensaje": response["message"]})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})
def renderEscaneo(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/validarOrden"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        if ses.rol == "PRODUCCION":
            return render(request, "escaneo.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})     
              
def validarOrden(request, id):
    try:
        print("entra validar Orden")
        ses = sesion.objects.get(id=id)
        if ses.rol == "PRODUCCION":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("validar de Orden")
            print(request.GET)
            orden = request.GET.get("ordenValidar")
            modulo = request.GET.get("moduloValidar")
            api_url = f"http://127.0.0.1:8000/ValidarOrden/{orden}/{modulo}/"
            print(api_url)
            respuesta = requests.post(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha encontrado la orden")
                return render(request, "escaneo.html", {"id": id, "orden_info": response["Orden"], "token":ses.token})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})                     
     
def registraInventario(request, id):
    try:
        print("entra")
        if request.method == "POST":
            print("entro")
            headers = {"token": request.POST.get("token", "")}
            print("Registeo de Op")
            api_url = "http://127.0.0.1:8000/ESCANEO"
            print("datos: ", request.POST)
            datos = {
                "referencia": request.POST.get("referencia", ""),
                "color": request.POST.get("color", ""),
                "talla": request.POST.get("talla", ""),
                "SKU": request.POST.get("sku", ""),
                "unidadesLeidas": request.POST.get("unidadesLeidas", ""),
                "unidades": request.POST.get("unidadesActuales", ""),
                "SAM": request.POST.get("sam", ""),
                "minutosProducidos": request.POST.get("minutosProducidos", ""),
                "modulo": request.POST.get("modulo", ""),
                "orden": request.POST.get("orden", ""),
            }
            print(datos)
            respuesta = requests.post(api_url, json=datos, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se ha registrado en el inventario")
                return render(request, "PRODUCCION.html", {"id": id, "registro_exitoso_inventario": True})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Método de solicitud no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})   
def renderSp(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/PROGRAMACION"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        
        if ses.rol == "SUPERVISIÓN":
            return render(request, "SUPERVISION.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})    

def buscarOperariosProgramacion(request, id):
    try:
        print("entra busqueda operarios")
        ses = sesion.objects.get(id=id)
        if ses.rol == "SUPERVISIÓN":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("usqueda operarios")
            print(request.GET)
            fecha = request.GET.get("fecha")
            modulo = request.GET.get("modulo")
            api_url = f"http://127.0.0.1:8000/BusquedaOperarios/{fecha}/{modulo}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se han encontrado los operarios")
                return render(request, "programacion.html", {"id": id, "registros": response.get("registros"),"fecha":response.get("fecha"),"token":ses.token})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})     
def renderprogramacion(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/PROGRAMACION"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        
        if ses.rol == "SUPERVISIÓN":
            return render(request, "programacion.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})  
    
def registraProgramacion(request, id):
    try:
        if request.method == "POST":
            print("entro")
            headers = {"token": request.POST.get("token", "")}
            print(headers)
            api_url = "http://127.0.0.1:8000/PROGRAMACION"
            print("datos: ", request.POST)

            cedulas = request.POST.getlist("cedula")
            nombres = request.POST.getlist("nombre")
            fechas = request.POST.getlist("fecha")
            modulos = request.POST.getlist("modulo")
            turnosReales = request.POST.getlist("turnoReal")
            turnosLaborados = request.POST.getlist("turnoLaborado")

            for i in range(len(cedulas)):
                datos = {
                    "fecha": fechas[i],
                    "nombre": nombres[i],
                    "cedula": cedulas[i],
                    "modulo": modulos[i],
                    "turnoReal": turnosReales[i],
                    "turnoLaborado": turnosLaborados[i],
                }
                print(datos)
                respuesta = requests.post(api_url, json=datos, headers=headers)
                print(respuesta)
                response = json.loads(respuesta.text)
                print(respuesta.text)
                if respuesta.status_code != 200:
                    return render(request, "error.html", {"mensaje": response["message"]})

            messages.add_message(request, messages.SUCCESS, "Se ha registrado en el inventario")
            return render(request, "SUPERVISION.html", {"id": id, "registro_exitoso_inventario": True})
        else:
            return render(request, "error.html", {"mensaje": "Método de solicitud no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def buscarOperariosProgramacionEdit(request, id):
    try:
        print("entra busqueda operarios")
        ses = sesion.objects.get(id=id)
        if ses.rol == "SUPERVISIÓN":
            print(ses.token)
            print("entro")
            headers = {"token": str(ses.token)}
            print(ses.token)
            print("usqueda operarios")
            print(request.GET)
            fecha = request.GET.get("fecha")
            modulo = request.GET.get("modulo")
            api_url = f"http://127.0.0.1:8000/PROGRAMACION/{fecha}/{modulo}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se han encontrado los operarios")
                return render(request, "editProgramacion.html", {"id": id, "registros": response.get("registros"),"fecha":response.get("fecha"),"token":ses.token})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})      
    
def renderProgramacionEdit(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/PROGRAMACION"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        
        if ses.rol == "SUPERVISIÓN":
            return render(request, "editProgramacion.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})         

def editarProgramacion(request, id):
    try:
        if request.method == "POST":
            print("entro")
            headers = {"token": request.POST.get("token", "")}
            print(headers)
            api_url = "http://127.0.0.1:8000/PROGRAMACION"
            print("datos: ", request.POST)

            ids = request.POST.getlist("id")
            cedulas = request.POST.getlist("cedula")
            nombres = request.POST.getlist("nombre")
            fechas = request.POST.getlist("fecha")
            modulos = request.POST.getlist("modulo")
            turnosReales = request.POST.getlist("turnoReal")
            turnosLaborados = request.POST.getlist("turnoLaborado")

            for i in range(len(ids)):
                datos = {
                    "id": ids[i],
                    "fecha": fechas[i],
                    "nombre": nombres[i],
                    "cedula": cedulas[i],
                    "modulo": modulos[i],
                    "turnoReal": turnosReales[i],
                    "turnoLaborado": turnosLaborados[i],
                }
                print(datos)
                respuesta = requests.patch(api_url, json=datos, headers=headers)
                print(respuesta)
                response = json.loads(respuesta.text)
                print(respuesta.text)
                if respuesta.status_code != 200:
                    return render(request, "error.html", {"mensaje": response["message"]})

            messages.add_message(request, messages.SUCCESS, "Se ha registrado en el inventario")
            return render(request, "SUPERVISION.html", {"id": id, "registro_exitoso_inventario": True})
        else:
            return render(request, "error.html", {"mensaje": "Método de solicitud no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})        
    
def renderIncentivos(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/INCENTIVOS"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        
        if ses.rol == "INCENTIVOS":
            return render(request, "incentivos.html", {"id": id,"token":ses.token})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})         

def renderLiquidacionIncentivos(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/INCENTIVOS"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        
        if ses.rol == "INCENTIVOS":
            return render(request, "liquidacionIncentivos.html", {"id": id})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})         
    

def renderPagoIncentivos(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/INCENTIVOS"
        respuesta = requests.get(api_url, headers=headers)
        response = json.loads(respuesta.text)
        print(response["message"])
        
        if ses.rol == "INCENTIVOS":
            return render(request, "pagoIncentivos.html", {"id": id,"token":ses.token})
        else:
            print("entra3")
            # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
            return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})

    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})   

          
def liquidarIncentivos(request, id):
    try:
        print("entra")
        if request.method == "POST":
            print("entro")
            headers = {"token": request.POST.get("token", "")}
            print("liquidacon de incentivos")
            api_url = "http://127.0.0.1:8000/INCENTIVOS"
            print("datos: ", request.POST)
            datos = {
                "fecha": request.POST.get("fecha", ""),
                "modulo": request.POST.get("modulo", ""),
            }
            print(datos)
            respuesta = requests.post(api_url, json=datos, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print(response["message"])
            if respuesta.status_code == 200:
                messages.add_message(request, messages.SUCCESS, "Se han liquidado los incentivos")
                return render(request, "liquidacionIncentivos.html", {"id": id, "liquidacion_incentivos": True,"incentivos":response.get("incentivos")})
            else:
                return render(request, "error.html", {"mensaje": response["message"]})
        else:
            return render(request, "error.html", {"mensaje": "Método de solicitud no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})       
    
def busquedaIncentivos(request, id):
    try:
        print("entra")
        if request.method == "POST":
            print("entro")
            headers = {"token": request.POST.get("token", "")}
            print("busqueda de incentivos")
            print("datos: ", request.POST)
            fechaInicial = request.POST.get("fechaInicial")
            fechaFinal = request.POST.get("fechaFinal")
            api_url = f"http://127.0.0.1:8000/PagoIncentivos/{fechaInicial}/{fechaFinal}"
            print(api_url)
            respuesta = requests.get(api_url, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            print("status: ", respuesta.status_code)
            if respuesta.status_code == 200:
                print("Se han encontrado los incentivos")
                incentivos_ids_list = response.get("incentivos_ids_list", [])
                data_list = response.get("data_list", [])
                return render(request, "pagoIncentivos.html", {"id": id, "registro_exitoso_inventario": True, "data_list": data_list, "incentivos_ids_list": incentivos_ids_list})
            else:
                mensaje_error = response.get("message", "Error desconocido")
                return render(request, "error.html", {"mensaje": mensaje_error})
        else:
            return render(request, "error.html", {"mensaje": "Método de solicitud no válido"})
    except Exception as error:
        print("Error:", error)
        return render(request, "error.html", {"mensaje": str(error)})

def pagoIncentivos(request, id):
    try:
        if request.method == "POST":
            print("entro")
            headers = {"token": request.POST.get("csrfmiddlewaretoken", "")}
            print(headers)
            api_url = "http://127.0.0.1:8000/PagoIncentivos"
            print("datos: ", request.POST)

            ids = request.POST.getlist("id")

            # Lista para almacenar todos los datos a enviar
            datos_lista = []

            # Recorrer cada ID y construir los datos a enviar
            for id_incentivo in ids:
                datos = {"id": id_incentivo}
                datos_lista.append(datos)

            # Enviar todos los datos juntos
            print("datos final: ",datos_lista)
            respuesta = requests.patch(api_url, json=datos_lista, headers=headers)
            print(respuesta)
            response = json.loads(respuesta.text)
            print(respuesta.text)
            if respuesta.status_code != 200:
                return render(request, "error.html", {"mensaje": response["message"]})

            messages.add_message(request, messages.SUCCESS, "Se ha registrado en el inventario")
            return render(request, "incentivos.html", {"id": id, "pago_incentivo": True})
        else:
            return render(request, "error.html", {"mensaje": "Método de solicitud no válido"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})

def renderDiasPagados(request, id):
    try:
        # Obtener la sesión
        ses = sesion.objects.get(id=id)

        # Validar el rol
        headers = {"token": str(ses.token)}
        api_url = "http://127.0.0.1:8000/DiasPagados"
        respuesta = requests.get(api_url, headers=headers)

        # Verificar el status de la respuesta HTTP
        if respuesta.status_code == 200:
            response = respuesta.json()
            print(response)
            print(response.get("message"))

            if ses.rol == "INCENTIVOS":
                return render(request, "diasPagados.html", {"id": id,"fechas_pagadas": response.get("fechas_pagadas"),})
            else:
                print("entra3")
                # Si el rol no es válido, puedes redirigir a otra página o mostrar un mensaje de error
                return render(request, "error.html", {"mensaje": "Acceso denegado: Rol no válido"})
        elif respuesta.status_code == 404:
            return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
        else:
            return render(request, "error.html", {"mensaje": "Error al procesar la solicitud"})
    except sesion.DoesNotExist:
        return render(request, "error.html", {"mensaje": "Sesión no encontrada"})
    except Exception as error:
        return render(request, "error.html", {"mensaje": str(error)})     