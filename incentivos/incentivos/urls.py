"""
URL configuration for incentivos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from incentivosApp.views import Logueo,RegistroUsuario,Operarios,Referencias,Orden,Escaneo,ValidarOrden,ProgramacionD,Incentivo,BusquedaOperarios,PagoIncentivos,DiasPagados
urlpatterns = [
    path("admin/", admin.site.urls),
    path('logueo',Logueo.as_view(),name="login"),
    path('logueo',Logueo.as_view(),name="login"),
    path('RH',Operarios.as_view(),name="modulo registrar"),
    path('RH/<id>',Operarios.as_view(),name="modulo registrar"),
    path('ADMIN',RegistroUsuario.as_view(),name="modulo registrar operarios"),
    path('ADMIN/<id>',RegistroUsuario.as_view(),name="modulo registrar operarios"),
    path('REFERENCIA',Referencias.as_view(),name="modulo registrar referencias"),
    path('REFERENCIA/<id>',Referencias.as_view(),name="modulo registrar referencias"),
    path('ORDEN',Orden.as_view(),name="modulo registrar Ordenes"),
    path('ORDEN/<id>',Orden.as_view(),name="modulo registrar Ordenes"),
    path('ESCANEO',Escaneo.as_view(),name="modulo registrar inventario"),
    path('ESCANEO/<fecha>',Escaneo.as_view(),name="modulo registrar inventario"),
    path('ValidarOrden/<orden>/<modulo>/', ValidarOrden.as_view(), name="validacion_de_op_para_escaneo"),
    path('PROGRAMACION',ProgramacionD.as_view(),name="modulo registrar programacion"),
    path('PROGRAMACION/<fecha>/<modulo>/',ProgramacionD.as_view(),name="modulo registrar programacion"),
    path('INCENTIVOS',Incentivo.as_view(),name="modulo registrar incentivos"),
    path('INCENTIVOS/<id>',Incentivo.as_view(),name="modulo registrar incentivos"),
    path('BusquedaOperarios/<fecha>/<modulo>/',BusquedaOperarios.as_view(),name="modulo registrar incentivos"),
    path('PagoIncentivos/<fechaInicial>/<fechaFinal>/',PagoIncentivos.as_view(),name="modulo buscar incentivos"),
    path('PagoIncentivos',PagoIncentivos.as_view(),name="modulo buscar incentivos"),
    path('DiasPagados',DiasPagados.as_view(),name="modulo DiasPagados"),
    
    
    

    
    
]
