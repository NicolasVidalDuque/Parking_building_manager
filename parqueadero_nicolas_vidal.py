import json
from copy import deepcopy

def tipo_de_acceso(carro):
    """
        Hace la correspondencia del lugar que puede ocupar el carro
        input:
            carro = int (1,2,3,4) el tipo de carro
        output:
            lista que contiene las posibles opciones correspondientes de parqueadero
    """
    opciones = [[1], [1,2], [3], [1,4]]
    #       [auto, electrico, Moto, discapa]
    return opciones[carro-1]


def organizar_matriz(matriz):
    """
        Organiza la matriz en un formato string para que se imprima mas entendible para el usuario
        Input:
            matriz = matriz a orfganizar
        Output:
            Matriz organizada en formato STRING
    """
    s = ''
    for i in range(len(matriz)-1, -1, -1):
        s += str(matriz[i]) + '\n'
    return s


def cupos_disponibles(distribucion, dic_edificio, categoria_carro):
    """
        Funcion que compara en el distribucion y el opciones (funcion que retorna lista con las el numero de la categoria correspondiente al carro) si esa es una posicion viable o no. 
        Se crea un diccionario con un elemento por piso y almacena las coordenadas [fila, col] en una matriz por piso de cada cupo disponible para el usuario
        input:
            distribucion = diccionario con las categorias numericas de distribucion del edificio
            dic_edificio = el diccionario conteniendo la informacion actual de edificio
            categoria_carro = la categoria int del carro
        output:
            cupos_totales = diccionario conteniendo una matriz con las coordenadas de cada cupo disponible
    """
    opciones = tipo_de_acceso(categoria_carro) #  Lista con las categorias posibles de parqueo
    cupos_totales = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}  # Formato = [ [fila, columna], [fila, columna] ] ---- tiene las casillas disponibles por piso.
    for piso in range(1, len(dic_edificio)+1):
        p = 'Piso' + str(piso)
        for fila in range(len(dic_edificio[p])):
            for columna in range(len(dic_edificio[p][fila])):
                if (distribucion[p][fila][columna] in opciones) and (dic_edificio[p][fila][columna] == 'O'):
                    cupos_totales[piso].append([fila, columna]) # se adiciona las coordenadas de una casilla disposible
    return cupos_totales


def eleccion_casilla(cupos_piso, matriz_piso):
    """
        Funcion que le muestra al usuario la matriz del piso que ha elejido. El usuario eloije una fila y una columna, se verifica que ese par de coordenadas [fila, col] esten contenidas es cupos_piso
        input:
            cupos_piso = lista de los cupos por coordenadas disponibles del piso que se elijio [fila, col]
            matriz_piso = copia de la matriz del piso del edificio actual
        output:
            [fila, columna] :  lista con las coordenadas elejidas por el usuario
    """
    for fila in range(len(matriz_piso)):
        for columna in range(len(matriz_piso[fila])):
            if not([fila, columna] in cupos_piso): 
            #  Si no esta en las opciones, se marca como X. Pero si si esta en las opciones no hay que hacer nada porque ya esta escrito si esta ocupado o no
                matriz_piso[fila][columna] = 'X'
    print('Distribucion del piso:\n(los espacios disponibles son representados por un O)\n'+ organizar_matriz(matriz_piso))
    fila = int(input('Ingrese la fila en donde quiere parquear:\n(Fila No. 1 es la de abajo)\n')) - 1
    columna = int(input('Ingrese la columna en donde quiere parquear:\n(columna No. 1 es la de la izquierda)\n')) - 1
    while not [fila, columna] in cupos_piso:
        print('Eleccion no disponible, vuelva a elejir.')
        fila = int(input('Ingrese la fila en donde quiere parquear:\n(Fila No. 1 es la de abajo)\n')) - 1
        columna = int(input('Ingrese la columna en donde quiere parquear:\n(columna No. 1 es la de la izquierda)\n')) - 1
    print('                     PUEDE PASAR')
    return [fila, columna]


def cambiar_formato(usuario, tipo_cambio):
    """
        Funcion con dos opciones que cambia el formato de los datos de una lista
        opcion 1 :
            Convierte de int a str mediante el indice almacenado en usuario asignandole un valor contenido en las listas
        opcion 2:
            convierte str a int mediante la llave str de un diccionario que retorna el indice numerico correspondiente
        Input:
            usuario = lista con la informacion del usuario
            tipo_cambio = el modo de cambio de formato
        Output:
            usuario = lista con el formato cambiado 
    """
    if tipo_cambio == 1: #  numero a str
        carro = ['Automóvil', 'Automóvil Eléctrico', 'Motocicleta', 'Discapacitado']
        persona = ['Estudiante', 'Profesor', 'Personal Administrativo', 'Visitantes']
        pago = ['Mensualidad', 'Diario']
        usuario[2] = persona[usuario[2]-1]
        usuario[4] = carro[usuario[4]-1]
        usuario[5] = pago[usuario[5]-1]
    else: #  str a numero
        carro = {'Automóvil':1, 'Automóvil Eléctrico':2, 'Motocicleta':3, 'Discapacitado':4}
        persona = {'Estudiante':1, 'Profesor':2, 'Personal Administrativo':3, 'Visitantes':4}
        pago = {'Mensualidad':1, 'Diario':2}
        usuario[2] = persona[usuario[2]]
        usuario[4] = carro[usuario[4]]
        usuario[5] = pago[usuario[5]]
    return usuario


def registrar(usuarios_registrados):
    """
        Procedimiento que compruba si el usuario ya esta registrado en el sistema, de lo contrario le pide los datos, crea un lista ordenada con los datos, los convierte en la funcion cambiar_formato(usuario, 1) y MODIFICA EL ARCHIVO JSON DIRECTAMENTE adjuntandole la lista del usuario
        Input:
            usuarios_registrados = diccionario con la informacion de los usuarios registrados hasta el momento
    """
    usuario = []
    num_id = int(input('Ingrese su numero de identificacion:\n'))
    if usuario_duplicado(num_id, usuarios_registrados['usuarios']):   
        print('-----Usted ya tiene regstado un vehiculo-----')
    else:
        usuario.append(str(input('Ingrese su nombre y apellido:\n')))
        usuario.append(num_id)
        usuario.append(int(input('Ingrese que tipo de usuario es:\n    (Estudiante : 1)\n    (Profesor : 2)\n    (Personal Administrativo : 3)\n')))
        usuario.append(str(input('Ingrese su Placa:\n')).upper())
        usuario.append(int(input('Ingrese su tipo de vehiculo:\n   (Automóvil : 1)\n   (Automóvil Eléctrico : 2)\n   (Motocicleta : 3)\n   (Discapacitado : 4)\n')))
        usuario.append(int(input('Ingrese su Plan de pago:\n    (Mensualidad : 1)\n    (Diario : 2)\n')))
        usuario = cambiar_formato(usuario, 1)
        # se cambia el diccionario original en la funcion principal, se referencia el mismo objeto
        usuarios_registrados['usuarios'].append(usuario)  
        with open('usuarios.json', 'w', encoding='utf8') as usuarios_json:
            # https://stackoverflow.com/questions/59298985/converting-non-ascii-characters-and-write-them-in-a-json-file-in-python
            json.dump(usuarios_registrados, usuarios_json, ensure_ascii=False)
            usuarios_json.close()
        print('-------------Ha sido registrado correctamente-------------')
        # [nom, num_id, tipo_usuario, placa, tipo_vehiculo, pago]


def matriz():
    """
        Genera el diccionario representante al edifico. Cada piso es una matriz generada por comprension de listas (f, c)
        Los pisos 1-5 son de 10x10. El ultimo piso es de 10x5
        Input:
            None
        Output:
            dic_edificio = diccionario que contiene la estructura del edifio toda desocupada (solo O's)
    """
    dic_edificio = {}
    for piso in range(6):
        if piso != 5:
            dic_edificio['Piso' + str(piso+1)] = [['O' for columna in range(10)] for fila in range(10)]
        else:
            dic_edificio['Piso' + str(piso+1)] = [['O' for columna in range(10)] for fila in range(5)]
    return dic_edificio


def usuario_duplicado(num_id, usuarios_registrados):
    """
        funcion que verifica si el usuario ya existe en el diccionario de usuarios_registrados
        Input:
            num_id = numero de identificacion del usuario a comprobar
            usuarios_registrados = diccionario con la informacion de los usuarios registrados hasta el momento
        Output:
            True : si la persona YA ESTA REGISTRADA
            False : si la persona NO ESTA REGISTRADA
    """
    for usuario in usuarios_registrados:
        if usuario[1] == num_id:
            return True
    return False


def menu_principal():
    """
        Procedimiento que muestra las opciones al usuario, recibe la informacion y comanda el resto de las funciones del programa
    """
    dic_edificio = matriz()
    with open('tiposParqueaderos.json', 'r') as distribucion_json:
        distribucion = json.load(distribucion_json)
        distribucion_json.close()
    carros_adentro = {} # Key = placa  ---  Value = [detalles]
    with open('usuarios.json', 'r', encoding='utf-8') as usuarios_json:
        usuarios_registrados = json.load(usuarios_json)
        usuarios_json.close() 

    print('------------------BIENVENIDO AL PARQUEADERO DE LA JAVERIANA------------------')

    cambio = 0 #  Esto mantiene registro sobre si se ha ingresado un nuevo usurio al diccionario. Si este es el caso se tiene que volver a leer el diccionario porque pues hubo un cambio en el archivo json.
    control = 0
    opcion = 1
    while opcion != 0:

        if cambio != control: 
            #  al ser diferentes significa que hubo un cambio, si no, todo esta igual. Cuando ya hubo cambio se vuelve a leer. Cuando se ingresa a la opcion de registrar usuario se le suma al cambio. Cuando se vuelve a leer el json se iguala cambio con control
            control = cambio
            with open('usuarios.json', 'r', encoding='utf-8') as usuarios_json:
                usuarios_registrados = json.load(usuarios_json)
                usuarios_json.close() 

        print('SELECCIONE EL NUMERO DE LA OPCION DESEADA:')
        opcion = int(input('    [SALIR DEL MENU : 0]\n    [INGRESAR AL PARQUEADERO : 1]\n    [RETIRAR VEHICULO : 2]\n    [REGISTRAR VEHICULO : 3]\n    [GENERAR ESTADISTICAS : 4]\n'))
        if opcion == 1:
            ingresar_parqueadero(distribucion, dic_edificio, carros_adentro, usuarios_registrados)
        elif opcion == 2:
            salida_parqueadero(dic_edificio, carros_adentro)
        elif opcion == 3:
            cambio += 1
            registrar(usuarios_registrados)
        elif opcion == 4:
            generar_estadisticas(carros_adentro)


def carro_registrado(placa, usuarios_registrados):
    """
        Funcion que verifica si el carro de encuentra registrado en la base de datos
        Input:
            placa = placa del carro
            usuarios_registrados = diccionario con la informacion de los usuarios registrados hasta el momento
        Output:
            Si esta registrado:
                usuario = lista con la informacion del usuario
            No esta registrado:
                False
    """
    for usuario in usuarios_registrados['usuarios']:
        if usuario[3] == placa:
            return usuario
    return False
        

def ingresar_parqueadero(distribucion, dic_edificio, carros_adentro, usuarios_registrados):
    """
        Procedimiento que toma la informacion del usuario que esta ingresando al parqueadero, verifica si se encuentra registrado, cambia dic_edificio y pone la casilla en donde el usuario va a parquear por una X, y adicional la informacion del carro al diccionario carros_adentro
        Input:
            usuarios_registrados = diccionario con la informacion de los usuarios registrados hasta el momento
            carros_adentro = diccionario que guarda la informacion de los carros que han ingresado al parqueadero (llave = placa)
            distribucion = diccionario con las categorias numericas de distribucion del edificio
            dic_edificio = el diccionario conteniendo la informacion actual de edificio
    """
    placa = input('Ingrese su placa por favor:\n')

    while placa in carros_adentro:
        print('Su carro ya se encuentra adentro')
        placa = input('Ingrese su placa por favor:\n')

    usuario_existente = carro_registrado(placa, usuarios_registrados) # devuelve lista o bool
    if usuario_existente != False:
        print('                 USUARIO ENCONTRADO DENTRO DE LA BASE DE DATOS.')
        #  La lista retornada esta en str, toca pasarlo a int
        usuario_int = cambiar_formato(usuario_existente, 2)
        tipo_carro = usuario_int[4] #  usuario_int rango de indices: (1,2,3,4)
        tipo_usuario = usuario_int[2]
        tipo_pago = usuario_int[5]
    else:
        tipo_carro = int(input('Ingrese su tipo de vehiculo:\n   (Automovil : 1)\n   (Automovil Electrico : 2)\n   (Moto : 3)\n   (Discapacitado : 4)\n'))
        tipo_usuario = 4
        tipo_pago = 2 

    cupos_totales = cupos_disponibles(distribucion, dic_edificio, tipo_carro)  # Tipo diccionario conteniendo listas de los cupos para parquear
    num_piso_elejido = eleccion_piso(cupos_totales, dic_edificio)
    casilla_elejida = eleccion_casilla(cupos_totales[num_piso_elejido], deepcopy(dic_edificio['Piso' + str(num_piso_elejido)])) #  Se le hace deep copy para no alterar el dic original
    fila = casilla_elejida[0]
    columna = casilla_elejida[1]
    #  No hace falta retornar debido a que se hace referencia a el objeto 'madre' entonces se cambia la variable 'global'
    dic_edificio['Piso' + str(num_piso_elejido)][fila][columna] = 'X'
    carros_adentro[str(placa)] = [num_piso_elejido, fila, columna, tipo_carro, tipo_usuario, tipo_pago]


def eleccion_piso(cupos_totales, dic_edificio):
    """
        Funcion que le muestra al usuario la cantidad de cupos disponibles segun su carro en todo el edificio para que este elija en que piso desea parquear
        Input:
            cupos_totales = diccionario que contiene las coordenadas de las casillas disponibles por piso
            dic_edificio = el diccionario conteniendo la informacion actual de edificio
        Output:
            eleccion = El numero del piso que el usuario eligio
    """
    print('Cantidad de cupos disponibles por piso:\nPiso 1 : ' + str(len(cupos_totales[1])) + '\nPiso 2 : ' + str(len(cupos_totales[2])) + '\nPiso 3 : ' + str(len(cupos_totales[3])) + '\nPiso 4 : ' + str(len(cupos_totales[4])) + '\nPiso 5 : ' + str(len(cupos_totales[5])) + '\nPiso 6 : ' + str(len(cupos_totales[6])) + '\n')
    eleccion = int(input('Ingrese el NUMERO del piso en donde quiere parquear:\n'))
    while len(cupos_totales[eleccion]) == 0:
        print('Piso lleno')
        eleccion = int(input('Ingrese el numero del piso en donde quiere parquear:\n'))
    return eleccion


def salida_parqueadero(dic_edificio, carros_adentro):
    """
        Procedimiento que le pide la placa al usuario, verifica que si este adentro del paqueadero, toma los datos de carros_adentro, desocupa el cupo en el que carro estaba parqueado en dic_edificio, le muestra al usuario cuanto tiene que pagar y elimina el carro de carros_adentro
        Input:
            dic_edificio = el diccionario conteniendo la informacion actual de edificio
            carros_adentro = diccionario que guarda la informacion de los carros que han ingresado al parqueadero (llave = placa)
    """
    placa = input('Ingrese su placa por favor:\n')

    try:
        carros_adentro[placa]
    except KeyError: #  https://realpython.com/python-keyerror/
        print('El carro no ha ingresado')
        return None

    piso = carros_adentro[placa][0]
    fila = carros_adentro[placa][1]
    columna = carros_adentro[placa][2]
    tipo_usuario = carros_adentro[placa][4]
    tipo_pago = carros_adentro[placa][5]
    
    dic_edificio['Piso'+str(piso)][fila][columna] = 'O'
    horas = input('Ingrese las horas que permanecio dentro del parqueadero:\n    (Fracion cuenta como hora adicional)\n')
    print('Tiene que pagar: ' + str(calcular_cobro(horas, tipo_usuario, tipo_pago))) # falta sacar tipo persona y tipo pago
    del carros_adentro[placa]


def redondear_hora(hora):
    """
        funcion que redondea la cantidad de horas por fraccion. Si encuentra un putno en el numero pero formato str le suma 1 al entero
        input:
            hora = str(cantidad de horas)
        Output:
            nuemro redondeado
    """
    num = ''
    for letra in hora:
        if letra == '.' or letra == ',':
            break
        num += letra
    return int(num) + 1


def calcular_cobro(horas, tipo_persona, tipo_pago):
    """
        Funcion que calcula cuanto se tiene que pagar segun la cantidad de horas que se estuvo adentro del parqueadero
        Input:
            horas = float(cantidad de horas que estuvo dentro del parqueadero)
            tipo_persona = int(indice numerico correspondiente a la categoria de la persona)
            tipo_pago = int(indice numerico correspondiente a la categoria de pago)
    """
    horas = redondear_hora(horas)
    if tipo_pago == 1:
        return 0
    valores = [1000, 2000, 1500, 3000]
    return horas * valores[tipo_persona-1]


def generar_estadisticas(carros_adentro):
    """
        Procedimiento. Menu de ociones para generar estadisticas.
        Input:
            carros_adentro = diccionario que guarda la informacion de los carros que han ingresado al parqueadero (llave = placa)
    """
    print('           ELIJA EL TIPO DE REPORTE')
    op = 1
    while op != 0:
        op = int(input('    (Salir : 0)\n    (Cantidad de vehiculos segun tipo de usuarios : 1)\n    (cantidad de vehiculos estacionados segun tipo de vehiculo : 2)\n    (Porcentaje de ocupación del parqueadero : 3)\n'))
        if op == 1:
            reporte_tipo_usuarios(carros_adentro)
        elif op == 2:
            reporte_tipo_vehiculo(carros_adentro)
        elif op == 3:
            reporte_porcetaje_ocupacion(carros_adentro)


def reporte_tipo_usuarios(carros_adentro):
    """
        Procedimiento que genera el reporte sobre la cantidad de carros adentro del parqueadero segun categoria de la persona. Recorre el diccionario carros_adentro y suma de acuerdo a la categoria. El reporte se genera en un archivo txt
        Input:
            carros_adentro = diccionario que guarda la informacion de los carros que han ingresado al parqueadero (llave = placa)
    """
    persona = [0,0,0,0]
    for usuario in carros_adentro.values():
        persona[usuario[4]-1] += 1
    reporte = open('reporte_cantidad_tipo_usuario.txt', 'w', encoding='utf-8')
    reporte.write('Reporte con la cantidad de vehículos estacionados según el tipo de usuario\nNumero vehiculos de:\n    ESTUDIANTES: {}\n    PROFESORES: {}\n    ADMINISTRATIVOS: {}\n    VISITANTES: {}'.format(persona[0], persona[1], persona[2], persona[3]))
    reporte.close()


def reporte_tipo_vehiculo(carros_adentro):
    """
        Procedimiento que genera el reporte sobre la cantidad de carros adentro del parqueadero segun categoria del carro. Recorre el diccionario carros_adentro y suma de acuerdo a la categoria. El reporte se genera en un archivo txt
        Input:
            carros_adentro = diccionario que guarda la informacion de los carros que han ingresado al parqueadero (llave = placa)
    """
    persona = [0,0,0,0]
    for usuario in carros_adentro.values():
        persona[usuario[3]-1] += 1
    reporte = open('reporte_cantidad_tipo_vehiculo.txt', 'w', encoding='utf-8')
    reporte.write('Reporte con la cantidad de vehículos estacionados según el tipo de usuario\nNumero vehiculos de:\n    AUTOMOVIL: {}\n    AUTOMOVIL ELECTRICO: {}\n    MOTOCICLETA: {}\n    DISCAPACITADO: {}'.format(persona[0], persona[1], persona[2], persona[3]))
    reporte.close()


def reporte_porcetaje_ocupacion(carros_adentro):
    """
        Procedimiento que genera el reporte sobre el porcentaje de ocupacion por piso y el todo el edificio. Recorre cada carro que esta adentro e identifica en que piso esta. El reporte se genera en un archivo txt 
        Input:
            carros_adentro = diccionario que guarda la informacion de los carros que han ingresado al parqueadero (llave = placa)
    """
    ingresos = len(carros_adentro)
    total = (ingresos/550)*100
    l = [0,0,0,0,0,0]  # [piso1, piso2, piso3, piso4, piso5]
    for persona in carros_adentro.values():
        l[persona[0]-1] += 1  # person[0] devuelve el piso (1,2,3,4,5,6) pero la lista tiene indices 0,1,2,3,4,5. Por eso se le resta -1
    reporte = open('reporte_porcentaje_ocupacion.txt', 'w', encoding='utf-8')
    reporte.write('REPORTE DE OCUPACION DEL EDIFICIO\n    TOTAL: de 550 parqueaderos ' + str(ingresos) + ' estan ocupados. El ' + str(total) + ' porciento\n    OCUPACION POR PISO:\n        ocupado de piso 1 = '+str(l[0])+'%\n        ocupado de piso 2 = '+str(l[1])+'%\n        ocupado de piso 3 = '+str(l[2])+'%\n        ocupado de piso 4 = '+str(l[3])+'%\n        ocupado de piso 5 = '+str(l[4])+'%\n        ocupado de piso 6 = '+str(l[5]*2 )+'%')
    reporte.close()


menu_principal()