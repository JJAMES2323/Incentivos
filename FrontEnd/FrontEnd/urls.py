"""
URL configuration for FrontEnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# En urls.py
from django.contrib import admin
from django.urls import path
from FrontEndApp.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', login),
    path("cerrarSesion/<id>/",closeSesion, name="cerrarSesion"),    
    path('', renderLogin, name='renderLogin'),
    path("RH/<id>/", renderRH), 
    path("RHe/<id>/", renderEditarOperario),
    path("registraOperario/<id>/", registraOperario, name="registraOperario"), 
    path("buscarOperario/<id>/",buscarOperario, name="buscarOperario"),
    path("editarOperario/<id>/",editarOperario, name="editarOperario"),
    path("buscarTodosOperario/<id>/",buscarTodosOperario, name="buscarTodosOperario"),
    path("RHd/<id>/", renderEliminarOperario),
    path("eliminarOperario/<id>/", eliminarOperario, name="eliminarOperario"),
    path("ADMIN/<id>/", renderADMIN), 
    path("ADMINe/<id>/", renderEditarUsuario),
    path("registraUsuario/<id>/", registraUsuario, name="registraUsuario"), 
    path("buscarUsuario/<id>/",buscarUsuarios, name="buscarUsuario"),
    path("editarUsuario/<id>/",editarUsuario, name="editarUsuario"),
    path("buscarTodosUsuarios/<id>/",buscarTodosUsuario, name="buscarTodosUsuarios"),
    path("ADMINd/<id>/", renderEliminarUsuario),
    path("eliminarUsuarios/<id>/", eliminarUsuario, name="eliminarUsuarios"),
    path("PRODUCCION/<id>/", renderPR), 
    path("PRODUCCIONe/<id>/", renderEditarReferencia),
    path("registraReferencia/<id>/", registraReferencia, name="registraReferencia"), 
    path("buscarReferencias/<id>/",buscarReferencias, name="buscarReferencias"),
    path("editarReferencia/<id>/",editarReferencia, name="editarReferencia"),
    path("buscarTodosReferencias/<id>/",buscarTodosReferencias, name="buscarTodosReferencias"),
    path("PRODUCCIONd/<id>/", renderEliminarReferencia),
    path("eliminarReferencia/<id>/", eliminarReferencia, name="eliminarReferencia"),
    path("PRODUCCIONeOP/<id>/", renderEditarOrden),
    path("registraOrden/<id>/", registraOrden, name="registraOrden"), 
    path("buscarOrden/<id>/",buscarOrden, name="buscarOrden"),
    path("editarOrden/<id>/",editarOrden, name="editarOrden"),
    path("buscarTodosOrden/<id>/",buscarTodosOrden, name="buscarTodosOrden"),
    path("PRODUCCIONdOP/<id>/", renderEliminarOrden),
    path("eliminarOrden/<id>/", eliminarOrden, name="eliminarOrden"),
    path("ESCANEO/<id>/", renderEscaneo),
    path("validarOrden/<id>/", validarOrden, name="validarOrden"),
    path("registraInventario/<id>/", registraInventario, name="registraInventario"),
    path("buscarOperariosProgramacion/<id>/", buscarOperariosProgramacion, name="buscarOperariosProgramacion"),
    path("registraProgramacion/<id>/", registraProgramacion, name="registraProgramacion"),
    path("buscarOperariosProgramacionEdit/<id>/", buscarOperariosProgramacionEdit, name="buscarOperariosProgramacionEdit"),
    path("editarProgramacion/<id>/", editarProgramacion, name="editarProgramacion"),
    path("SUPERVISIÓN/<id>/", renderSp), 
    path("SUPERVISIÓNp/<id>/", renderprogramacion), 
    path("SUPERVISIÓNe/<id>/", renderProgramacionEdit), 
    path("INCENTIVOS/<id>/", renderIncentivos), 
    path("INCENTIVOSl/<id>/", renderLiquidacionIncentivos), 
    path("INCENTIVOSNp/<id>/", renderPagoIncentivos),
    path("liquidarIncentivos/<id>/", liquidarIncentivos, name="liquidarIncentivos"),
    path("busquedaIncentivos/<id>/", busquedaIncentivos, name="busquedaIncentivos"),
    path("pagoIncentivos/<id>/", pagoIncentivos, name="pagoIncentivos"),
    path("DIASPAGADOS/<id>/", renderDiasPagados, name="DIASPAGADOS"),
]
