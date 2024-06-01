def validarUsuario (nombre, cedula,usuario,contraseña):
    if nombre==None or nombre == "":
        print("Nombre no valido")
        raise Exception ("nombre no valido")
    if cedula is None or cedula =="":
        print("cedula no valida")
        raise Exception ("Cedula no valida")
    if len(cedula) >10:
        print("cedula debe contener maximo 10 dijitos")
        raise Exception ("cedula  invalida")
    try:
        cedula = int(cedula)
    except ValueError:
        print("la cedula debe ser numerica")
        raise Exception ("cedula no valida")
    if usuario == None or usuario == "":
        print("usuario invalido")
        raise Exception ("Usuario no valido")
    if contraseña is None or contraseña == "":
        print ("Contraseña no valida")
        raise Exception("contraseña invalida")
def validarOperario (nombre, cedula,modulo,correo,telefono,fechaN,direccion):
    if nombre==None or nombre == "":
        print("Nombre no valido")
        raise Exception ("nombre no valido")
    if cedula is None or cedula =="":
        print("cedula no valida")
        raise Exception ("Cedula no valida")
    if len(cedula) >10:
        print("cedula debe contener minimo 10 dijitos")
        raise Exception ("cedula  invalida")
    try:
        cedula = int(cedula)
    except ValueError:
        print("la cedula debe ser numerica")
        raise Exception ("cedula no valida")
    if modulo == None or modulo == "":
        print("usuario invalido")
        raise Exception ("Usuario no valido")
    if correo is None or correo == "":
        print ("correo no valida")
        raise Exception("correo invalida")
    partes= correo.split("@")
    if len(partes)!=2:
        print("correo no valido")
        raise Exception("correo no valido")
    usuario,dominio=partes
    if not (usuario.isalnum() and dominio.count(".")==1 and all(c.isalnum()or c== "." for c in dominio)):
        print("correo no valido")
        raise Exception("correo no valido")
    if telefono is None or telefono == "":
        print("telefono no valido")
    if fechaN==None or fechaN =="":
        print("fecha no valida")
        raise Exception("Fecha no valida")
    if direccion == None or fechaN =="":
        raise Exception ("direccion no valida") 
def validarReferencias(referencia,color,talla,tipoPrenda,sam):
    if referencia == None or referencia =="":
        print("referncia no valida")      
        raise Exception("referencia no valida")     
    if color == None or color =="":
        print("color no valido")           
        raise Exception("color no valida")
    if talla == None or talla =="":
        print("talla no valida")          
        raise Exception("talla no valida") 
    if tipoPrenda == None or tipoPrenda =="":
        print("tipo de prenda no valida")
        raise Exception("tipo de prenda no valida")           
    if sam == None or sam =="":
        print("sam no validp")         
        raise Exception("SAM no valida")
def validarReferenciaUnica(lpg,refNueva, color, talla):
    for referencia in lpg.Referencias:
        if referencia.referencia==refNueva.referencia and referencia.color==color and referencia.talla==talla: 
           print("los datos estan duplicados")
           raise Exception ("Los datos estan duplicados")       
def validarPersonaUnica(lpg, nuevo):
    for usuario in lpg.Usuario:
        if (usuario.usuario==nuevo.usuario and usuario.usurio !=None) or usuario.cedula==nuevo.cedula:
            print("los datos estan duplicados")
            raise Exception ("Los datos estan duplicados")   
def validarOperarioUnicoa(lpg, nuevo):
    for operario in lpg.Operario:
        if operario.cedula==nuevo.cedula:
            print("los datos estan duplicados")
            raise Exception ("Los datos estan duplicados") 
def validarOrden (referenciaBuscada, color, talla, cantidad,modulo):
    if referenciaBuscada == None or referenciaBuscada =="":
        print("referncia no valida")      
        raise Exception("referencia no valida")
    if color == None or color == "":
        print("Color no valido")
        raise Exception ("Color no valido")
    if talla == None or talla == "":
        print("Talla no valida")
        raise Exception("talla no valida")
    if cantidad == None or cantidad == "":
        print("cantidad no valida")
        raise Exception("Cantidad no valida")
    try:
        cantidad = int(cantidad)
    except ValueError:
        print("la cantidad debe ser numerica")
        raise Exception ("cantidad no valida")
    if modulo   == None or modulo == "":
        print("modulo no valida")
        raise Exception ("Modulo no valido")                  
def buscarRef(lpg, referenciaBuscada, color, talla):
    for referencia in lpg.Referencias:
        if (referencia.referencia == referenciaBuscada and
                referencia.color == color and
                referencia.talla == talla):
            print("Se ha encontrado la referencia", referenciaBuscada)
            print("SKU de la referencia:", referencia.SKU)
            return referencia.SKU
    raise Exception("No se ha encontrado la referencia")
 
def buscarRefColTall(lpg, sku):
    for referencia in lpg.Referencias:
        if referencia.SKU == sku:
            return referencia.referencia, referencia.color, referencia.talla, referencia.SAM
    raise Exception("No se ha encontrado la referencia con el SKU proporcionado")
def buscarRefPorOrden(lpg, orden):
    for ordenes in lpg.Ordenes:
        if ordenes.ordenes == orden:
            return ordenes.unidades,ordenes.unidadesLeidas,ordenes.SKU,ordenes.modulo
    raise Exception("No se ha encontrado esta orden de producción")

   