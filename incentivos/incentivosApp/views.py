from datetime import datetime
import datetime
from typing import Any
from django import http 
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Usuarios,Sesion,Operario,Referencia,Ordenes,Inventario,Programacion,Incentivos
import json,secrets,string
from .Validador import validacion
from datetime import datetime
from django.db.models import Sum, Count

def validarRol(sesion,rol):
    if sesion.usuario.rol not in rol:
        print("entra")
        print(sesion)
        raise Exception("El usuario no posee permisos")
    
def buscarRol(usuario):
    try:
        usuarioB= Usuarios.objects.get(usuario=usuario)
        return usuarioB.rol
    except Usuarios.DoesNotExist:
        return None    
    
class Logueo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)  
    def get(self, request,id=None):
        pass
    def put(self,request):
        pass
    def post(self,request):
        token=""
        message1=""
        try:
            body=json.loads(request.body)
            usuario=body["usuario"]
            password=body["password"]
            rol=buscarRol(usuario)
            if rol is None:
                raise Exception("Usuario no ncontrado")
            usuarios=Usuarios.objects.get(usuario=usuario,rol=rol,password=password)
            sesion=Sesion.objects.filter(usuario=usuarios)
            if sesion.exists():
                raise Exception("El usuario ya esta en sesion")
            caracteres = string.ascii_letters+string.digits
            token= "".join(secrets.choice(caracteres)for _ in range(128))
            sesion=Sesion(usuario=usuarios, token=token)
            sesion.save()
            message = "login exitoso"
            status= 200
        except Exception as error:
            message=str(error)
            status=400
        response={"message": message, "message1": message1,"token" : token, "rol": rol}
        return JsonResponse(response,status=status)

    def delete(self,request):
        try:
            token = request.META.get('HTTP_TOKEN')
            sesion=Sesion.objects.get(token=token)
            sesion.delete()
            message="se ha cerrado sesion"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message":message}
        return JsonResponse(response,status=status)   
    
class RegistroUsuario(View):
        @method_decorator(csrf_exempt)
        def dispatch(self,request, *args: Any, **kwargs: Any):
            return super().dispatch(request, *args, **kwargs)
        def get(self,request,id=None):
            personas=None
            try:
                token = request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["ADMIN"])
                if id:
                    personas=list(Usuarios.objects.filter(cedula=id).values())
                else:
                    personas=list(Usuarios.objects.values())
                if len(personas)>0:
                    message="Resgistro encontrado"
                else:
                    message="resgitro no encontrado"
                status=200
            except Exception as error:
                message=str(error)
                status=400
            response={"message":message, "persona":personas}
            return JsonResponse(response,status=status)                        
        def put(self, request):
            pass
        def post(self,request):
            print("usuarios")
            try:
                token = request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["ADMIN"])
                body=json.loads(request.body)
                cedula=body["cedula"]
                nombre=body["nombre"]
                rol=body["rol"]
                usuario=body["usuario"]
                password=body["password"]
                validacion.validarUsuario(nombre,cedula,usuario,password)
                persona=Usuarios.objects.filter(cedula=cedula)
                if persona.exists():
                    raise Exception("Ya hay una persona con esta cedula")
                persona=Usuarios.objects.filter(usuario=usuario)
                if persona.exists():
                    raise Exception("Ya exixte una persona con este ususario")
                persona=Usuarios(cedula=cedula,nombre=nombre,rol=rol,usuario=usuario,password=password)
                persona.save()
                message="Registro exitoso"
                status=200
            except Exception as error:
                message=str(error)
                status=400
            response={"message": message}
            return JsonResponse (response,status=status)
        def delete(self,request,id=None):
            try:
                token = request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["ADMIN"])
                body=json.loads(request.body)
                cedula=body["cedula"]
                persona=Usuarios.objects.get(cedula=cedula)
                persona.delete()
                message="Se ha eliminado la persona"
                status=200
            except Exception as error:
                message=str(error)
                status=400
            response={"message" :message}
            return JsonResponse(response,status=status)
        def patch(self,request,id=None):
            persona=None
            try: 
                token=request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["ADMIN"])
                body=json.loads(request.body)
                cedula=body.get("cedula")
                if cedula is not None:
                    persona=Usuarios.objects.get(cedula=cedula)                
                    if "nombre" in body:
                        persona.nombre = body["nombre"]
                    if "rol" in body:
                        persona.rol = body["rol"]
                    if "usuario" in body:
                        persona.usuario = body["usuario"]
                    if "password" in body:
                        persona.password = body["password"]
                    if "correoE" in body:
                        persona.correoE = body["correoE"]                                                                                
                    if "telefono" in body:
                        persona.telefono = body["telefono"]
                    if "fecha" in body:
                        persona.fecha = body["fecha"]
                    if "direccion" in body:
                        persona.direccion = body["direccion"]

                    persona.save()
                    message="Actualizacion exitosa"
                    status=200
                else:
                    message = "Se requiere el campo 'cedula' para la actualización."
                    status = 400
            except Usuarios.DoesNotExist:
               message = f"No se encontró ninguna persona con la cédula: {cedula}"
               status = 404
            except Exception as error:
                message = str(error)
                status(400)
            response={"message": message}
            return JsonResponse(response,status=status)     
        
class Operarios(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,id=None):
        operario=None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["RH"])
            if id:
                operario=list(Operario.objects.filter(cedula=id).values())
            else:
                operario=list(Operario.objects.values())    
            if len(operario)>0:
                message="Registros encontrados"
            else:
                message="Registros no encontrados"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message":message, "operario":operario}
        return JsonResponse(response,status=status)
    def put(self, request):
        pass
    def post(self, request):
        print("operarios")
        try:
            print("operarios")
            token= request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["RH"])
            body=json.loads(request.body)
            cedula=body["cedula"]
            nombre=body["nombre"]
            modulo=body["modulo"]
            correoE=body["correoE"]
            telefono=body["telefono"]        
            fechaN=body["fechaN"]
            direccion=body["direccion"]
            validacion.validarOperario(nombre,cedula,modulo,correoE,telefono,fechaN,direccion)
            operario=Operario.objects.filter(cedula=cedula)
            if operario.exists():
                raise Exception("Ya exixte un operario con esta cedula")
            operario=Operario(cedula,nombre,modulo,correoE,telefono,fechaN,direccion)
            operario.save()
            message="Registro Exixtoso"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message": message}
        return JsonResponse (response,status=status)
    def delete(self,request,id=None):
            try:
                token = request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["RH"])
                body=json.loads(request.body)
                cedula=body["cedula"]
                operario=Operario.objects.filter(cedula=cedula)
                operario.delete()
                message="Se ha eliminado el paciente"
                status=200
            except Exception as error:
                message=str(error)
                status=400
            response={"message" :message}
            return JsonResponse(response,status=status) 
    def patch(self,request,id=None):
            paciente=None
            try: 
                token=request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["RH"])
                body=json.loads(request.body)
                cedula=body.get("cedula")
                if cedula is not None:
                    operario=Operario.objects.get(cedula=cedula)                
                    if "nombre" in body:
                        operario.nombre = body["nombre"]
                    if "modulo" in body:
                        operario.modulo = body["modulo"]    
                    if "fecha" in body:
                        operario.fecha = body["fecha"]
                    if "genero" in body:
                        operario.genero = body["genero"]
                    if "direccion" in body:
                        operario.direccion = body["direccion"]
                    if "telefono" in body:
                        operario.telefono = body["telefono"]                                                                                
                    if "correoE" in body:
                        operario.correoE = body["correoE"]
                    operario.save()
                    message="Actualizacion exitosa"
                    status=200
                else:
                    message = "Se requiere el campo 'cedula' para la actualización."
                    status = 400
            except Operario.DoesNotExist:
               message = f"No se encontró ninguna persona con la cédula: {cedula}"
               status = 404
            except Exception as error:
                message = str(error)
                status(400)
            response={"message": message}
            return JsonResponse(response,status=status)   
        
class Referencias(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,id=None):
        referenica=None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["PRODUCCION"])
            if id:
                referenica=list(Referencia.objects.filter(referencia=id).values())
            else:
                referenica=list(Referencia.objects.values())    
            if len(referenica)>0:
                message="Registros encontrados"
            else:
                message="Registros no encontrados"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message":message, "referenica":referenica}
        return JsonResponse(response,status=status)
    def put(self, request):
        pass
    def post(self, request):
        print("referencia")
        try:
            token= request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["PRODUCCION"])
            body=json.loads(request.body)
            referenciaC=body["referenciaC"]
            color=body["color"]
            talla=body["talla"]
            tipoPrenda=body["tipoPrenda"]
            SAM=body["SAM"]        
            validacion.validarReferencias(referenciaC,color,talla,tipoPrenda,SAM)
            referencia = Referencia.objects.filter(referencia=referenciaC, color=color, talla=talla)
            if referencia.exists():
                raise Exception("Ya exixte esta refencia")
            referencia=Referencia(referenciaC,color,talla,tipoPrenda,SAM)
            referencia.save()
            message="Registro Exixtoso"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message": message}
        return JsonResponse (response,status=status)
    def delete(self,request,id=None):
            try:
                token = request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["PRODUCCION"])
                body=json.loads(request.body)
                SKU=body["SKU"]
                referencia=Referencia.objects.filter(SKU=SKU)
                referencia.delete()
                message="Se ha eliminado la referencia con el sku "+ SKU
                status=200
            except Exception as error:
                message=str(error)
                status=400
            response={"message" :message}
            return JsonResponse(response,status=status) 
    def patch(self,request,id=None):
            referencia=None
            try: 
                token=request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["PRODUCCION"])
                body=json.loads(request.body)
                SKU=body.get("SKU")
                if SKU is not None:
                    referencia=Referencia.objects.get(SKU=SKU)                
                    if "referencia" in body:
                        referencia.referencia = body["referencia"]
                    if "color" in body:
                        referencia.color = body["color"]    
                    if "talla" in body:
                        referencia.talla = body["talla"]
                    if "tipoPrenda" in body:
                        referencia.tipoPrenda = body["tipoPrenda"]
                    if "SAM" in body:
                        referencia.SAM = body["SAM"]
                    referencia.save()
                    message="Actualizacion exitosa"
                    status=200
                else:
                    message = "Se requiere el campo 'sku' para la actualización."
                    status = 400
            except Operario.DoesNotExist:
               message = f"No se encontró ninguna referencia con el SKU: {SKU}"
               status = 404
            except Exception as error:
                message = str(error)
                status(400)
            response={"message": message}
            return JsonResponse(response,status=status)                 
        
class Orden(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    def get(self,request,id=None):
        orden=None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["PRODUCCION"])
            if id:
                orden=list(Ordenes.objects.filter(orden=id).values())
            else:
                orden=list(Ordenes.objects.values())    
            if len(orden)>0:
                message="Registros encontrados"
            else:
                message="Registros no encontrados"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message":message, "orden":orden}
        return JsonResponse(response,status=status)
    def put(self, request):
        pass
    def post(self, request):
        try:
            token= request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["PRODUCCION"])
            body=json.loads(request.body)
            referencia=body["referencia"]
            color=body["color"]
            talla=body["talla"]
            cantidad=body["cantidad"]
            modulo=body["modulo"]    
            refBuscada= Referencia.objects.get(referencia=referencia,color=color, talla=talla)
            print("llego aca")
            sku= str(refBuscada.SKU)  
            validacion.validarOrden(referencia,color,talla,cantidad,modulo)
            orden = Ordenes(Referencia=referencia, color=color, talla=talla, modulo=modulo, SKU=sku, unidades=cantidad, unidadesLeidas=0)
            orden.save()
            message="Registro Exixtoso"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message": message}
        return JsonResponse (response,status=status)
    def delete(self,request,id=None):
            try:
                token = request.META.get("HTTP_TOKEN")
                sesion=Sesion.objects.get(token=token)
                validarRol(sesion,["PRODUCCION"])
                body=json.loads(request.body)
                orden=body["orden"]
                orden=Ordenes.objects.filter(orden=orden)
                orden.delete()
                message="Se ha eliminado la orden "
                status=200
            except Exception as error:
                message=str(error)
                status=400
            response={"message" :message}
            return JsonResponse(response,status=status) 
    def patch(self, request, id=None):
         orden = None
         try: 
             token = request.META.get("HTTP_TOKEN")
             sesion = Sesion.objects.get(token=token)
             validarRol(sesion,["PRODUCCION"])
             body = json.loads(request.body)
             orden_id = body.get("orden")
             if orden_id is not None:
                 orden = Ordenes.objects.get(orden=orden_id)
            
                 # Recuperar los datos anteriores de la orden
                 referencia_anterior = orden.Referencia
                 print(orden.Referencia)
                 talla_anterior = orden.talla
                 color_anterior = orden.color
            
                 if "referencia" in body and "color" in body and "talla" in body:
                     nueva_referencia = body["referencia"]
                     nuevo_color = body["color"]
                     nueva_talla = body["talla"]
                     # Verificar si la nueva referencia, color y talla existen en la base de datos
                     if Referencia.objects.filter(referencia=nueva_referencia, color=nuevo_color, talla=nueva_talla).exists():
                         orden.Referencia = nueva_referencia
                         orden.color = nuevo_color
                         orden.talla = nueva_talla
                     else:
                         raise Exception("La nueva referencia, color y talla no existen.")
            
                 elif "referencia" in body and "color" in body:
                     print("entro")
                     nueva_referencia = body["referencia"]
                     nuevo_color = body["color"]
                     # Verificar si la nueva referencia y color existen en la base de datos con la talla anterior
                     if Referencia.objects.filter(referencia=nueva_referencia, color=nuevo_color, talla=talla_anterior).exists():
                         orden.Referencia = nueva_referencia
                         orden.color = nuevo_color
                         
                     else:
                         raise Exception("La nueva referencia y color no existen con la talla anterior.")
            
                 elif "referencia" in body and "talla" in body:
                     nueva_referencia = body["referencia"]
                     nueva_talla = body["talla"]
                     # Verificar si la nueva referencia y talla existen en la base de datos con el color anterior
                     if Referencia.objects.filter(referencia=nueva_referencia, color=color_anterior, talla=nueva_talla).exists():
                         orden.Referencia = nueva_referencia
                         orden.talla = nueva_talla
                     else:
                         raise Exception("La nueva referencia y talla no existen con el color anterior.")
            
                 elif "color" in body and "talla" in body:
                     nuevo_color = body["color"]
                     nueva_talla = body["talla"]
                     # Verificar si el nuevo color y talla existen en la base de datos con la referencia anterior
                     if Referencia.objects.filter(referencia=referencia_anterior, color=nuevo_color, talla=nueva_talla).exists():
                         orden.color = nuevo_color
                         orden.talla = nueva_talla
                     else:
                         raise Exception("El nuevo color y talla no existen con la referencia anterior.")
            
                 elif "referencia" in body and "color" not in body and "talla" not in body:
                     nueva_referencia = body["referencia"]
                     # Verificar si la nueva referencia existe en la base de datos con el color y talla anteriores
                     if Referencia.objects.filter(referencia=nueva_referencia, color=color_anterior, talla=talla_anterior).exists():
                         orden.Referencia = nueva_referencia
                     else:
                         raise Exception("La nueva referencia no existe con el color y talla anteriores.")
            
                 elif "color" in body and "referencia" not in body and "talla" not in body:
                     nuevo_color = body["color"]
                     # Verificar si el nuevo color existe en la base de datos con la referencia y talla anteriores
                     if Referencia.objects.filter(referencia=referencia_anterior, color=nuevo_color, talla=talla_anterior).exists():
                         orden.color = nuevo_color
                     else:
                         raise Exception("El nuevo color no existe con la referencia y talla anteriores.")
            
                 elif "talla" in body and "referencia" not in body and "color" not in body:
                     nueva_talla = body["talla"]
                     # Verificar si la nueva talla existe en la base de datos con la referencia y color anteriores
                     if Referencia.objects.filter(referencia=referencia_anterior, color=color_anterior, talla=nueva_talla).exists():
                         orden.talla = nueva_talla
                     else:
                         raise Exception("La nueva talla no existe con la referencia y color anteriores.")
                 if "modulo" in body:
                     orden.modulo = body["modulo"]
                 if "unidades" in body:
                     orden.unidades = body["unidades"]
                 print(orden.Referencia)    
                 orden.save()
                 message = "Actualización exitosa"
                 status = 200
             else:
                 message = "Se requiere el campo 'orden' para la actualización."
                 status = 400
         except Operario.DoesNotExist:
             message = f"No se encontró ninguna orden: {orden_id}"
             status = 404
         except Exception as error:
             message = str(error)
             status = 400
    
         response = {"message": message}
         return JsonResponse(response, status=status)
class ValidarOrden(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, orden, modulo):
        # Manejar solicitudes GET aquí si es necesario
        pass

    def post(self, request, orden, modulo):
        try:
            orden_obj = Ordenes.objects.get(orden=orden, modulo=modulo)
            sku = orden_obj.SKU
            unidades = orden_obj.unidades
            unidadesLeidas = orden_obj.unidadesLeidas
            referencia = orden_obj.Referencia
            color= orden_obj.color
            talla= orden_obj.talla
            try:
                ref = Referencia.objects.get(referencia=referencia,color=color,talla=talla)
                SAM = ref.SAM
            except Referencia.DoesNotExist:
                SAM = None  # Otra forma de manejar este caso
            message="Registro encontrado"   
            data= {
                'success': True,
                'orden': orden,
                'modulo': modulo,
                'sku': sku,
                'referencia': referencia,
                'color': color,
                'talla': talla,
                'unidades': unidades,
                'unidadesLeidas': unidadesLeidas,
                'sam': SAM
            } 
            status=200  
            response={"message":message, "Orden":data}
            return JsonResponse(response,status=status)
        except Ordenes.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Orden no encontrada',"status":404})

class Escaneo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, fecha=None):
        inventario = None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["PRODUCCION"])

            if fecha:
                # Convertir la fecha de cadena a objeto datetime
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                # Filtrar el inventario por la fecha proporcionada
                inventario = list(Inventario.objects.filter(fecha=fecha_obj).values())
            else:
                # Si no se proporciona una fecha, devolver todo el inventario
                inventario = list(Inventario.objects.values())    

            if len(inventario) > 0:
                message = "Registros encontrados"
                status = 200
            else:
                message = "Registros no encontrados"
                status = 404
        except Sesion.DoesNotExist:
            message = "Token de sesión no válido"
            status = 401
        except Exception as error:
            message = str(error)
            status = 400
        
        response = {"message": message, "inventario": inventario}
        return JsonResponse(response, status=status)
    
    def post(self, request):
        try:
            token= request.META.get("HTTP_TOKEN")
            sesion=Sesion.objects.get(token=token)
            validarRol(sesion,["PRODUCCION"])
            body=json.loads(request.body)
            print("Datos recibidos en el cuerpo:", body)
            referencia=body["referencia"]
            color=body["color"]
            talla=body["talla"]
            SKU=body["SKU"]
            unidadesLeidas=body["unidadesLeidas"]
            unidades=body["unidades"]
            SAM=body["SAM"]
            minutosProducidos=body["minutosProducidos"]  
            fecha = datetime.now().strftime("%Y-%m-%d")
            modulo=body["modulo"]
            orden=body["orden"]
            registro=Inventario(Referencia=referencia,color=color,talla=talla,SKU=SKU,unidades=unidades,SAM=SAM,minutosProducidos=minutosProducidos,fecha=fecha,modulo=modulo,orden=orden)
            registro.save()
            orden_obj = Ordenes.objects.get(orden=orden, modulo=modulo)
            orden_obj.unidadesLeidas = unidadesLeidas
            orden_obj.save()
            message="Registro Exixtoso"
            status=200
        except Exception as error:
            message=str(error)
            status=400
        response={"message": message}
        return JsonResponse(response, status=status)
    
class BusquedaOperarios(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, fecha=None, modulo=None):
        registros = None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["SUPERVISIÓN"])

            if fecha:
                print(fecha)
                fecha_obj = fecha
                if Programacion.objects.filter(fecha=fecha_obj, modulo=modulo).exists():
                    message = "Ya hay programaciones para este día y módulo"
                    status = 404
                else:
                    registros = list(Operario.objects.filter(modulo=modulo).values())
                    if registros:
                        message = "Operarios encontrados para el módulo dado"
                        status = 200
                    else:
                        message = "No hay operarios para el módulo dado"
                        status = 404
            else:
                message = "Debe proporcionar una fecha"
                status = 400
        except Exception as error:
            message = str(error)
            status = 400

        response = {"message": message, "registros": registros, "fecha": fecha}
        return JsonResponse(response, status=status)

      
      
class ProgramacionD(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, fecha=None, modulo=None):
        registros = None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["SUPERVISIÓN"])

            if fecha:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                registros = list(Programacion.objects.filter(fecha=fecha_obj,modulo=modulo).values())
            else:
                registros = list(Programacion.objects.values())

            if len(registros) > 0:
                message = "Registros encontrados"
                status = 200
            else:
                message = "Registros no encontrados"
                status = 404
        except Exception as error:
            message = str(error)
            status = 400

        response = {"message": message, "registros": registros}
        return JsonResponse(response, status=status)

    def post(self, request):
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["SUPERVISIÓN"])
            body = json.loads(request.body)
            fecha = body["fecha"]
            nombre = body["nombre"]
            cedula = body["cedula"]
            modulo = body["modulo"]
            turnoReal = body["turnoReal"]
            turnoLaborado = body["turnoLaborado"]
            programacion = Programacion.objects.filter(fecha=fecha, cedula=cedula)
            if programacion.exists():
                raise Exception("Ya existe esta referencia")
            programacion = Programacion(fecha=fecha, nombre=nombre, cedula=cedula, modulo=modulo,
                                        turnoReal=turnoReal, turnoLaborado=turnoLaborado)
            programacion.save()
            message = "Registro Exitoso"
            status = 200
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message": message}
        return JsonResponse(response, status=status)

    def delete(self, request, id=None):
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["SUPERVISIÓN"])
            registro = Programacion.objects.get(id=id)
            registro.delete()
            message = f"Se ha eliminado la referencia con el id {id}"
            status = 200
        except Programacion.DoesNotExist:
            message = f"No se encontró ninguna referencia con el ID: {id}"
            status = 404
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message": message}
        return JsonResponse(response, status=status)

    def patch(self, request, id=None):
        registro = None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["SUPERVISIÓN"])
            body = json.loads(request.body)
            id = body.get("id")
            if id is not None:
                registro = Programacion.objects.get(id=id)
                if "fecha" in body:
                    registro.fecha = body["fecha"]
                if "nombre" in body:
                    registro.nombre = body["nombre"]
                if "cedula" in body:
                    registro.cedula = body["cedula"]
                if "modulo" in body:
                    registro.modulo = body["modulo"]
                if "turnoReal" in body:
                    registro.turnoReal = body["turnoReal"]
                if "turnoLaborado" in body:
                    registro.turnoLaborado = body["turnoLaborado"]
                registro.save()
                message = "Actualizacion exitosa"
                status = 200
            else:
                message = "Se requiere el campo 'sku' para la actualización."
                status = 400
        except Programacion.DoesNotExist:
            message = f"No se encontró ninguna referencia con el ID: {id}"
            status = 404
        except Exception as error:
            message = str(error)
            status = 400
        response = {"message": message}
        return JsonResponse(response, status=status)

from django.db.models import Sum

class Incentivo(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, fecha=None, modulo=None):
        registros = None
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["INCENTIVOS"])

            if fecha:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                registros = list(Incentivos.objects.filter(fecha=fecha_obj, modulo=modulo).values())
            else:
                registros = list(Programacion.objects.values())

            if len(registros) > 0:
                message = "Registros encontrados"
                status = 200
            else:
                message = "Registros no encontrados"
                status = 404
        except Exception as error:
            message = str(error)
            status = 400

        response = {"message": message, "registros": registros}
        return JsonResponse(response, status=status)

    def post(self, request):
        try:
            token = request.META.get("HTTP_TOKEN")
            sesion = Sesion.objects.get(token=token)
            validarRol(sesion, ["INCENTIVOS"])
            body = json.loads(request.body)

            fecha = body.get("fecha")
            modulo = body.get("modulo")

            # Verificar si ya existen registros en la tabla Incentivos para la fecha y el módulo dados
            if Incentivos.objects.filter(fecha=fecha, modulo=modulo).exists():
                message = "Ya existen registros para este módulo y fecha"
                status = 400
                response = {"message": message}
                return JsonResponse(response, status=status)

            # Obtener la suma de minutosProducidos
            total_minutos_producidos = Inventario.objects.filter(fecha=fecha, modulo=modulo).aggregate(total=Sum('minutosProducidos'))['total']
            if total_minutos_producidos is None:
                total_minutos_producidos = 0

            # Obtener la suma de turnoLaborado
            total_turno_laborado = Programacion.objects.filter(fecha=fecha, modulo=modulo).aggregate(total=Sum('turnoLaborado'))['total']
            if total_turno_laborado is None:
                total_turno_laborado = 0

            # Calcular la eficiencia
            if total_turno_laborado > 0:
                eficiencia = total_minutos_producidos / total_turno_laborado
            else:
                eficiencia = 0

            # Calcular el incentivo
            if eficiencia < 0.85:
                incentivo = 0
            else:
                eficiencia_inicial = 0.85
                puntos = (eficiencia - eficiencia_inicial) * 100
                valor = 1000 * puntos
                incentivo = min(valor, 30000)

            # Obtener los operarios de la programación
            operarios_programacion = Programacion.objects.filter(fecha=fecha, modulo=modulo)

            for operario in operarios_programacion:
                # Verificar si el turnoReal y el turnoLaborado son iguales
                if operario.turnoReal == operario.turnoLaborado:
                    incentivo_operario = incentivo
                else:
                    # Calcular porcentaje de turno laborado
                    porcentaje_turno_laborado = operario.turnoLaborado / operario.turnoReal
                    # Verificar si trabaja menos del 50%
                    if porcentaje_turno_laborado < 0.5:
                        incentivo_operario = 0
                    else:
                        incentivo_operario = incentivo * porcentaje_turno_laborado

                # Guardar los datos en la tabla Incentivos
                registro = Incentivos(
                    cedula=operario.cedula,
                    nombre=operario.nombre,
                    modulo=modulo,
                    eficiencia=eficiencia,
                    turno=operario.turnoLaborado,
                    fecha=fecha,
                    incentivo=incentivo_operario,
                    estado=False
                )
                registro.save()

            # Consultar los registros en la tabla Incentivos con la fecha dada
            incentivos_registrados = Incentivos.objects.filter(fecha=fecha, modulo=modulo)
            incentivos_list = []
            for incentivo in incentivos_registrados:
                if incentivo.estado==False:
                    estado="No pagado"
                print(incentivo.eficiencia)
                eficiencia_porcentaje = int(float(incentivo.eficiencia) * 100)
                incentivos_list.append({
                    "cedula": incentivo.cedula,
                    "nombre": incentivo.nombre,
                    "modulo": incentivo.modulo,
                    "eficiencia": eficiencia_porcentaje,
                    "turno": incentivo.turno,
                    "fecha": incentivo.fecha,
                    "incentivo": "${:,.2f}".format(incentivo.incentivo),
                    "estado": estado,
                })

            message = "Incentivos calculados correctamente y guardados en la base de datos"
            status = 200
            response = {"message": message, "incentivos": incentivos_list}
        except Sesion.DoesNotExist:
            message = "Token de sesión no válido"
            status = 401
            response = {"message": message}
        except Exception as error:
            message = str(error)
            status = 400
            response = {"message": message}

        return JsonResponse(response, status=status)
    
class PagoIncentivos(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, fechaInicial=None, fechaFinal=None):
        try:
            # Verificar si las fechas están presentes
            if not fechaInicial or not fechaFinal:
                return JsonResponse({"message": "Las fechas de inicio y final son necesarias."}, status=400)
            
            # Verificar si hay al menos un registro en el rango de fechas en la tabla Incentivos
            incentivos_list = Incentivos.objects.filter(fecha__range=[fechaInicial, fechaFinal])
            
            # Verificar si hay registros con estado=True en el rango de fechas proporcionado
            dias_pagados = incentivos_list.filter(estado=True).exists()
            if dias_pagados:
                message = "No se puede realizar la liquidación porque dentro de estas fechas ya hay días pagados. Selecciona otras fechas."
                return JsonResponse({"message": message}, status=400)

            if not incentivos_list.exists():
                message = "No hay registros de incentivos en el rango de fechas proporcionado."
                return JsonResponse({"message": message}, status=404)
            
            # Obtener la lista de cédulas únicas en el rango de fechas dado
            cedulas_unicas = incentivos_list.values_list('cedula', flat=True).distinct()
            
            # Crear una lista para almacenar los datos de cada persona junto con el incentivo total
            data_list = []
            for cedula in cedulas_unicas:
                incentivos_persona = incentivos_list.filter(cedula=cedula)
                incentivo_total = incentivos_persona.aggregate(total=Sum('incentivo'))['total']
                data_list.append({
                    "cedula": cedula,
                    "nombre": incentivos_persona.first().nombre,
                    "modulo": incentivos_persona.first().modulo,
                    "rango_fechas": f"{fechaInicial} - {fechaFinal}",
                    "incentivo_total": "${:,.2f}".format(incentivo_total)
                })
            
            # Crear una lista separada solo con los IDs de los incentivos
            incentivos_ids_list = list(incentivos_list.values_list('id', flat=True))

            # Retornar ambas listas en formato JSON con el status 200
            status = 200
            return JsonResponse({"data_list": data_list, "incentivos_ids_list": incentivos_ids_list}, status=status)

        except Exception as e:
            # Si ocurre algún error, retornar un mensaje de error con el status 400
            message = f"Error al procesar la solicitud: {str(e)}"
            return JsonResponse({"message": message}, status=400)
    def patch(self, request, *args, **kwargs):
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            
            # Obtener la lista de IDs de incentivos del diccionario de datos
            ids = [item['id'] for item in data]  # Acceder al valor del ID en cada diccionario
            print("IDs recibidos:", ids)
            
            # Verificar si se proporcionaron IDs
            if not ids:
                return JsonResponse({"message": "No se proporcionaron IDs para actualizar."}, status=400)
            
            # Iterar sobre cada ID de incentivo
            for incentivo_id in ids:
                # Obtener el incentivo con el ID proporcionado
                incentivo = Incentivos.objects.filter(id=incentivo_id).first()
                
                # Verificar si se encontró el incentivo
                if not incentivo:
                    return JsonResponse({"message": f"No se encontró ningún incentivo con el ID {incentivo_id}."}, status=404)
                
                # Actualizar el estado del incentivo
                incentivo.estado = True
                incentivo.save()
            
            # Retornar una respuesta exitosa
            return JsonResponse({"message": "Estado de los incentivos actualizado correctamente."}, status=200)
        
        except Exception as e:
            # Manejo de otros errores
            return JsonResponse({"message": f"Error al procesar la solicitud: {str(e)}"}, status=400)

class DiasPagados(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)    
    def get(self, request):
        try:
            # Buscar las fechas repetidas con el estado True
            fechas_pagadas = Incentivos.objects.filter(estado=True).values('fecha').annotate(total=Count('fecha')).filter(total__gt=1)
            
            # Obtener solo una fecha por cada fecha repetida
            fechas_unicas = []
            for fecha_info in fechas_pagadas:
                fecha = fecha_info['fecha']
                if fecha not in fechas_unicas:
                    fechas_unicas.append(fecha)
            
            # Retornar las fechas únicas encontradas
            return JsonResponse({"fechas_pagadas": fechas_unicas}, status=200)
        
        except Exception as e:
            # Si ocurre algún error, retornar un mensaje de error con el status 400
            message = f"Error al procesar la solicitud: {str(e)}"
            return JsonResponse({"message": message}, status=400)