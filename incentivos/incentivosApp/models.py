from django.db import models

# Create your models here.
class Usuarios(models.Model):
    cedula=models.IntegerField(primary_key=True,null=False)
    nombre=models.CharField(max_length=30, null=True)
    rol=models.CharField(max_length=30,null=True)
    usuario=models.CharField(max_length=30,null=True)
    password=models.CharField(max_length=30, null=True)
    
class Operario(models.Model):
    cedula=models.IntegerField(primary_key=True,null=False)
    nombre=models.CharField(max_length=30, null=True)
    modulo=models.CharField(max_length=30,null=False)
    correoE=models.EmailField(max_length=30,null=True)
    telefono=models.IntegerField(null=True)
    fechaN=models.DateField(null=True)
    direccion=models.CharField(max_length=30,null=True)
    
class Referencia(models.Model):
    referencia=models.CharField(max_length=30,null=False)
    color=models.CharField(max_length=30, null=True)
    talla=models.CharField(max_length=30, null=True)
    tipoPrenda=models.CharField(max_length=30, null=True)
    SAM=models.FloatField(null=False)
    SKU=models.AutoField(primary_key=True,null=False)
    
class Ordenes(models.Model):
    orden = models.AutoField(primary_key=True)
    Referencia = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30, null=True)
    talla = models.CharField(max_length=30, null=True) 
    modulo = models.CharField(max_length=30, null=False)
    SKU = models.CharField(max_length=30, null=False) 
    unidades = models.IntegerField(null=False)
    unidadesLeidas = models.IntegerField(null=False)
         
class Inventario(models.Model):
    Referencia = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30, null=True)
    talla = models.CharField(max_length=30, null=True) 
    SKU = models.CharField(max_length=30, null=False)
    unidades = models.IntegerField(null=False)
    SAM = models.FloatField(null=False)
    minutosProducidos = models.FloatField(null=False)
    fecha = models.DateField(null=True)
    modulo = models.CharField(max_length=30, null=False)
    orden = models.CharField(max_length=30, null=False)

class Programacion(models.Model):
    fecha=models.DateField(null=True)
    nombre=models.CharField(max_length=30, null=True)
    cedula=models.IntegerField(null=False)
    modulo=models.CharField(max_length=30,null=False)
    turnoReal=models.FloatField(null=False)
    turnoLaborado=models.FloatField(null=False)
    
class Incentivos(models.Model):
    cedula=models.IntegerField(null=False)
    nombre=models.CharField(max_length=30, null=True)
    modulo=models.CharField(max_length=30,null=False)
    eficiencia=models.CharField(max_length=30,null=False)
    turno=models.FloatField(null=False)
    fecha=models.DateField(null=True)
    incentivo=models.FloatField(null=False)
    estado=models.BooleanField(null=False)
    
class Sesion(models.Model):
    id=models.AutoField(primary_key=True,null=False)
    usuario=models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True)
    token=models.CharField(max_length=200,null=True,default="")
    
    