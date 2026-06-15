# -----------------------------------------------------------------------------
# TPI - Programacion 1 | UTN Tecnicatura Universitaria en Programacion
# Gestion de Datos de Paises en Python: Filtros, ordenamientos y estadisticas
# Autores: - Zaccardi, Leonel
#          - Schneider, Nicolas
# -----------------------------------------------------------------------------
# Conceptos aplicados:
#   - Listas y diccionarios
#   - Funciones (auxiliares y principales)
#   - Condicionales y bucles
#   - Manejo de archivos CSV
#   - Validaciones y manejo de errores con try/except
#   - Busquedas, filtros, ordenamientos y estadisticas basicas
# -----------------------------------------------------------------------------

import csv

# Nombre del archivo CSV que contiene el dataset de paises.
# Se define como constante para no repetirlo en cada funcion.
NOMBRE_ARCHIVO = "paises.csv"


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES - VALIDACION DE ENTRADAS
# Estas funciones no forman parte del menu principal. Su rol es garantizar
# que los datos ingresados por el usuario sean validos antes de procesarlos.
# Son reutilizadas por las funciones principales para evitar repetir codigo.
# -----------------------------------------------------------------------------

def normalizar_texto(texto):
    # Quita espacios al inicio/final y convierte el texto a minusculas.
    # Se usa para comparar nombres sin importar mayusculas ni espacios extra.
    return texto.strip().lower()

def pedir_opcion(mensaje, minimo, maximo):
    # Pide al usuario un numero entero dentro del rango [minimo, maximo].
    # Repite la solicitud hasta recibir un valor valido.
    while True:
        try:
            opcion = int(input(mensaje))

            if opcion < minimo or opcion > maximo:
                raise ValueError(f"La opcion debe estar entre {minimo} y {maximo}.")

            return opcion
        except ValueError as error:
            print(f"Error: {error}")

def pedir_texto_no_vacio(mensaje):
    # Pide un texto y verifica que no este vacio ni sea solo espacios.
    # Repite la solicitud hasta recibir un valor valido.
    while True:
        try:
            texto = input(mensaje).strip()

            if texto == "":
                raise ValueError("El campo no puede estar vacio.")

            return texto
        except ValueError as error:
            print(f"Error: {error}")

def pedir_entero_positivo(mensaje):
    # Pide un numero entero estrictamente mayor que cero.
    # Se usa para poblacion y superficie, que no pueden ser cero ni negativos.
    while True:
        try:
            numero = int(input(mensaje))

            if numero <= 0:
                raise ValueError("El numero debe ser entero y mayor que cero.")

            return numero
        except ValueError as error:
            print(f"Error: {error}")

def pedir_entero_no_negativo(mensaje):
    # Pide un numero entero mayor o igual a cero.
    # Se usa para los rangos de filtro, donde cero es un valor valido.
    while True:
        try:
            numero = int(input(mensaje))

            if numero < 0:
                raise ValueError("El numero no puede ser negativo.")

            return numero
        except ValueError as error:
            print(f"Error: {error}")

def pedir_rango(mensaje_minimo, mensaje_maximo):
    # Pide dos numeros y valida que el minimo no sea mayor al maximo.
    # Retorna una tupla (minimo, maximo) lista para usar en los filtros.
    while True:
        try:
            minimo = pedir_entero_no_negativo(mensaje_minimo)
            maximo = pedir_entero_no_negativo(mensaje_maximo)

            if minimo > maximo:
                raise ValueError("El valor minimo no puede ser mayor que el valor maximo.")

            return minimo, maximo
        except ValueError as error:
            print(f"Error: {error}")


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES - MANEJO DEL ARCHIVO CSV
# Estas funciones se encargan de leer y escribir el archivo CSV.
# Separan la logica de persistencia del resto del programa.
# -----------------------------------------------------------------------------

def validar_fila_csv(fila, numero_linea):
    # Valida que una fila del CSV tenga todos los campos necesarios y con
    # valores correctos. Si algo falla, lanza un ValueError con el numero
    # de linea para facilitar la identificacion del error.
    # Retorna un diccionario con los datos del pais si todo es valido.
    campos_necesarios = ["nombre", "poblacion", "superficie", "continente"]

    # Verificamos que existan todas las columnas y que no esten vacias
    for campo in campos_necesarios:
        if campo not in fila:
            raise ValueError(f"Linea {numero_linea}: falta la columna '{campo}'.")

        if fila[campo] is None or fila[campo].strip() == "":
            raise ValueError(f"Linea {numero_linea}: el campo '{campo}' esta vacio.")

    # Guardamos nombre y continente ya limpios de espacios
    nombre = fila["nombre"].strip()
    continente = fila["continente"].strip()

    # Intentamos convertir poblacion y superficie a entero
    # Si el CSV tiene texto en esos campos, esto lanzara un error
    try:
        poblacion = int(fila["poblacion"])
        superficie = int(fila["superficie"])
    except ValueError:
        raise ValueError(f"Linea {numero_linea}: poblacion o superficie no son numericos.")

    # Validamos que los valores numericos sean positivos
    if poblacion <= 0:
        raise ValueError(f"Linea {numero_linea}: la poblacion debe ser mayor que cero.")
    if superficie <= 0:
        raise ValueError(f"Linea {numero_linea}: la superficie debe ser mayor que cero.")

    # Armamos y retornamos el diccionario del pais
    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    return pais

def cargar_paises_csv(nombre_archivo):
    # Lee el archivo CSV y retorna una lista de diccionarios.
    # Cada diccionario representa un pais con sus cuatro campos.
    # Si una fila tiene errores, la omite y avisa sin detener el programa.
    paises = []

    try:
        with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Verificamos que el archivo no este completamente vacio
            if lector.fieldnames is None:
                print("Error: el archivo CSV esta vacio.")
                return paises

            # Empezamos en 1 porque la linea 1 es el encabezado del CSV
            numero_linea = 1

            for fila in lector:
                numero_linea += 1

                # Cada fila se valida por separado para no detener la carga
                # si una sola fila tiene un error
                try:
                    pais = validar_fila_csv(fila, numero_linea)
                    paises.append(pais)
                except ValueError as error:
                    print(f"Advertencia: {error}. La fila fue omitida.")

        print(f"Archivo '{nombre_archivo}' cargado. Paises cargados: {len(paises)}")

    except FileNotFoundError:
        print(f"Error: no se encontro el archivo '{nombre_archivo}'.")
    except PermissionError:
        print(f"Error: no se tienen permisos para leer '{nombre_archivo}'.")
    except Exception as error:
        print(f"Error inesperado al leer el CSV: {error}")

    return paises

def guardar_paises_csv(nombre_archivo, paises):
    # Guarda la lista de paises en el archivo CSV sobreescribiendo el contenido
    # anterior. Se llama automaticamente cada vez que se agrega o actualiza
    # un pais para mantener el archivo sincronizado con la lista en memoria.
    try:
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            # Escribe la primera fila con los nombres de las columnas
            escritor.writeheader()

            # Escribe cada pais como una fila del CSV
            for pais in paises:
                escritor.writerow(pais)

        print(f"Datos guardados correctamente en '{nombre_archivo}'.")
    except PermissionError:
        print(f"Error: no se tienen permisos para escribir en '{nombre_archivo}'.")
    except Exception as error:
        print(f"Error inesperado al guardar el CSV: {error}")


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES - BUSQUEDA Y PRESENTACION
# Estas funciones se encargan de buscar paises en la lista y de mostrarlos
# en pantalla. Son usadas por las funciones principales del menu.
# -----------------------------------------------------------------------------

def buscar_indice_por_nombre(paises, nombre):
    # Busca un pais por nombre exacto (ignorando mayusculas y espacios).
    # Retorna el indice en la lista si lo encuentra, o -1 si no existe.
    # Se usa en actualizar y agregar para verificar si el pais ya existe.
    nombre_normalizado = normalizar_texto(nombre)

    for i in range(len(paises)):
        if normalizar_texto(paises[i]["nombre"]) == nombre_normalizado:
            return i  # retorna la posicion del pais en la lista

    return -1  # -1 indica que no se encontro

def buscar_paises_por_nombre(paises, texto_buscado):
    # Busca paises cuyo nombre contenga el texto ingresado (coincidencia parcial).
    # Por ejemplo, buscar "ar" devuelve Argentina, Bulgaria, etc.
    # Retorna una lista con todos los paises que coincidan.
    resultados = []
    texto_buscado = normalizar_texto(texto_buscado)

    for pais in paises:
        if texto_buscado in normalizar_texto(pais["nombre"]):
            resultados.append(pais)

    return resultados

def mostrar_pais(pais):
    # Muestra los datos de un pais en formato legible por pantalla.
    print(f"  Nombre    : {pais['nombre']}")
    print(f"  Poblacion : {pais['poblacion']:,}")
    print(f"  Superficie: {pais['superficie']:,} km2")
    print(f"  Continente: {pais['continente']}")

def mostrar_lista_paises(paises):
    # Muestra todos los paises de una lista numerados.
    # Si la lista esta vacia, informa al usuario y no hace nada mas.
    if len(paises) == 0:
        print("No hay paises para mostrar.")
        return

    print(f"\n========== LISTADO DE PAISES ({len(paises)} resultados) ==========")

    for i in range(len(paises)):
        print(f"\nPais {i + 1}")
        print("  ----------")
        mostrar_pais(paises[i])

    print("=" * 54)


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES - CLAVES DE ORDENAMIENTO
# Estas funciones extraen un campo especifico de un diccionario de pais.
# Se pasan como parametro 'key' a sorted(), max() y min() para indicar
# por que campo ordenar o comparar. Reemplazan el uso de funciones lambda.
# -----------------------------------------------------------------------------

def obtener_nombre(pais):
    # Retorna el nombre del pais normalizado (sin tildes ni mayusculas).
    # Permite ordenar alfabeticamente de forma correcta.
    return normalizar_texto(pais["nombre"])

def obtener_poblacion(pais):
    # Retorna la poblacion del pais como numero entero.
    # Usada para ordenar, buscar el maximo y el minimo de poblacion.
    return pais["poblacion"]

def obtener_superficie(pais):
    # Retorna la superficie del pais como numero entero.
    # Usada para ordenar por superficie ascendente o descendente.
    return pais["superficie"]


# -----------------------------------------------------------------------------
# FUNCIONES PRINCIPALES - FUNCIONALIDADES DEL MENU
# Estas son las funciones que el usuario ejecuta desde el menu principal.
# Cada una representa una funcionalidad completa del sistema.
# Usan las funciones auxiliares para validar, buscar y mostrar datos.
# -----------------------------------------------------------------------------

def agregar_pais(paises, nombre_archivo):
    # Permite agregar un nuevo pais al dataset.
    # Valida que no exista un pais con el mismo nombre antes de agregarlo.
    # Guarda automaticamente los cambios en el CSV.
    print("\n--- Agregar pais ---")

    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ")

        # Verificamos que no exista ya un pais con ese nombre
        if buscar_indice_por_nombre(paises, nombre) != -1:
            raise ValueError("Ya existe un pais con ese nombre en el dataset.")

        poblacion  = pedir_entero_positivo("Ingrese la poblacion: ")
        superficie = pedir_entero_positivo("Ingrese la superficie en km2: ")
        continente = pedir_texto_no_vacio("Ingrese el continente: ")

        # Armamos el diccionario del nuevo pais con los cuatro campos requeridos
        pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        }

        # Agregamos a la lista en memoria y guardamos en el CSV
        paises.append(pais)
        guardar_paises_csv(nombre_archivo, paises)
        print("Pais agregado correctamente.")

    except ValueError as error:
        print(f"Error: {error}")

def actualizar_pais(paises, nombre_archivo):
    # Permite actualizar la poblacion y superficie de un pais existente.
    # Busca el pais por nombre exacto, muestra los datos actuales
    # y luego pide los nuevos valores. Guarda los cambios en el CSV.
    print("\n--- Actualizar pais ---")

    if len(paises) == 0:
        print("No hay paises cargados.")
        return

    nombre = pedir_texto_no_vacio("Ingrese el nombre exacto del pais a actualizar: ")
    indice = buscar_indice_por_nombre(paises, nombre)

    # Si retorna -1 significa que no se encontro el pais
    if indice == -1:
        print("No se encontro un pais con ese nombre.")
        return

    print("\nDatos actuales:")
    mostrar_pais(paises[indice])

    # Pedimos los nuevos valores y los guardamos directamente en el diccionario
    nueva_poblacion  = pedir_entero_positivo("Ingrese la nueva poblacion: ")
    nueva_superficie = pedir_entero_positivo("Ingrese la nueva superficie en km2: ")

    paises[indice]["poblacion"]  = nueva_poblacion
    paises[indice]["superficie"] = nueva_superficie

    guardar_paises_csv(nombre_archivo, paises)
    print("Pais actualizado correctamente.")

def buscar_pais(paises):
    # Busca paises cuyo nombre contenga el texto ingresado (parcial o exacto).
    # Muestra todos los resultados que coincidan.
    print("\n--- Buscar pais ---")

    if len(paises) == 0:
        print("No hay paises cargados.")
        return

    texto = pedir_texto_no_vacio("Ingrese el nombre o parte del nombre del pais: ")
    resultados = buscar_paises_por_nombre(paises, texto)

    if len(resultados) == 0:
        print("No se encontraron paises con ese criterio de busqueda.")
    else:
        mostrar_lista_paises(resultados)

def filtrar_por_continente(paises):
    # Filtra y muestra los paises que pertenecen al continente indicado.
    # La comparacion ignora mayusculas y espacios extra.
    continente = pedir_texto_no_vacio("Ingrese el continente: ")
    resultados = []

    for pais in paises:
        if normalizar_texto(pais["continente"]) == normalizar_texto(continente):
            resultados.append(pais)

    if len(resultados) == 0:
        print("No se encontraron paises para ese continente.")
    else:
        mostrar_lista_paises(resultados)

def filtrar_por_rango_poblacion(paises):
    # Filtra y muestra los paises cuya poblacion este dentro del rango indicado.
    minimo, maximo = pedir_rango("Poblacion minima: ", "Poblacion maxima: ")
    resultados = []

    for pais in paises:
        if pais["poblacion"] >= minimo and pais["poblacion"] <= maximo:
            resultados.append(pais)

    if len(resultados) == 0:
        print("No se encontraron paises dentro de ese rango de poblacion.")
    else:
        mostrar_lista_paises(resultados)

def filtrar_por_rango_superficie(paises):
    # Filtra y muestra los paises cuya superficie este dentro del rango indicado.
    minimo, maximo = pedir_rango("Superficie minima (km2): ", "Superficie maxima (km2): ")
    resultados = []

    for pais in paises:
        if pais["superficie"] >= minimo and pais["superficie"] <= maximo:
            resultados.append(pais)

    if len(resultados) == 0:
        print("No se encontraron paises dentro de ese rango de superficie.")
    else:
        mostrar_lista_paises(resultados)

def menu_filtros(paises):
    # Submenu que agrupa las tres opciones de filtrado.
    # Permanece activo hasta que el usuario elija volver al menu principal.
    if len(paises) == 0:
        print("No hay paises cargados.")
        return

    while True:
        print("\n--- Filtrar paises ---")
        print("1. Por continente")
        print("2. Por rango de poblacion")
        print("3. Por rango de superficie")
        print("4. Volver al menu principal")

        opcion = pedir_opcion("Seleccione una opcion: ", 1, 4)

        if opcion == 1:
            filtrar_por_continente(paises)
        elif opcion == 2:
            filtrar_por_rango_poblacion(paises)
        elif opcion == 3:
            filtrar_por_rango_superficie(paises)
        else:
            break  # opcion 4: volver al menu principal

def ordenar_paises(paises):
    # Ordena la lista de paises por nombre, poblacion o superficie,
    # en direccion ascendente o descendente segun elija el usuario.
    # No modifica la lista original, muestra el resultado ordenado.
    print("\n--- Ordenar paises ---")

    if len(paises) == 0:
        print("No hay paises cargados.")
        return

    print("Criterio de ordenamiento:")
    print("1. Nombre")
    print("2. Poblacion")
    print("3. Superficie")

    criterio = pedir_opcion("Seleccione el criterio: ", 1, 3)

    print("\nDireccion:")
    print("1. Ascendente (de menor a mayor)")
    print("2. Descendente (de mayor a menor)")

    direccion  = pedir_opcion("Seleccione la direccion: ", 1, 2)

    # True si el usuario eligio descendente, False si eligio ascendente
    descendente = direccion == 2

    # Ordenamos usando la funcion clave correspondiente al criterio elegido
    if criterio == 1:
        paises_ordenados = sorted(paises, key=obtener_nombre,      reverse=descendente)
    elif criterio == 2:
        paises_ordenados = sorted(paises, key=obtener_poblacion,   reverse=descendente)
    else:
        paises_ordenados = sorted(paises, key=obtener_superficie,  reverse=descendente)

    mostrar_lista_paises(paises_ordenados)

def calcular_promedio(paises, campo):
    # Calcula el promedio de un campo numerico (poblacion o superficie)
    # recorriendo toda la lista y acumulando el total.
    # Retorna 0 si la lista esta vacia para evitar division por cero.
    if len(paises) == 0:
        return 0

    total = 0

    for pais in paises:
        total += pais[campo]

    return total / len(paises)

def cantidad_por_continente(paises):
    # Cuenta cuantos paises hay en cada continente.
    # Usa un diccionario como contador: la clave es el nombre del continente
    # y el valor es la cantidad de paises de ese continente.
    conteo = {}

    for pais in paises:
        continente = pais["continente"]

        if continente in conteo:
            # Si el continente ya esta en el diccionario, sumamos 1
            conteo[continente] += 1
        else:
            # Si es la primera vez que aparece, lo inicializamos en 1
            conteo[continente] = 1

    return conteo

def mostrar_estadisticas(paises):
    # Muestra un resumen estadistico del dataset completo:
    # - Pais con mayor y menor poblacion
    # - Promedio de poblacion y superficie
    # - Cantidad de paises por continente
    print("\n--- Estadisticas generales ---")

    if len(paises) == 0:
        print("No hay paises cargados.")
        return

    # Buscamos el pais con mayor y menor poblacion usando las funciones clave
    pais_mayor_poblacion = max(paises, key=obtener_poblacion)
    pais_menor_poblacion = min(paises, key=obtener_poblacion)

    # Calculamos promedios reutilizando la funcion auxiliar
    promedio_poblacion  = calcular_promedio(paises, "poblacion")
    promedio_superficie = calcular_promedio(paises, "superficie")

    # Contamos paises agrupados por continente
    conteo_continentes = cantidad_por_continente(paises)

    print("\nPais con mayor poblacion:")
    mostrar_pais(pais_mayor_poblacion)

    print("\nPais con menor poblacion:")
    mostrar_pais(pais_menor_poblacion)

    # .2f muestra el numero con dos decimales
    print(f"\nPromedio de poblacion : {promedio_poblacion:,.2f}")
    print(f"Promedio de superficie: {promedio_superficie:,.2f} km2")

    print("\nCantidad de paises por continente:")
    for continente, cantidad in conteo_continentes.items():
        print(f"  {continente}: {cantidad}")


# -----------------------------------------------------------------------------
# MENU PRINCIPAL
# Punto de entrada del programa. Muestra el menu y coordina la ejecucion
# de cada funcionalidad segun la opcion elegida por el usuario.
# -----------------------------------------------------------------------------

def mostrar_menu():
    # Muestra las opciones disponibles en el menu principal.
    print("\n--------------- GESTION DE DATOS DE PAISES ---------------")
    print("1. Mostrar todos los paises")
    print("2. Agregar pais")
    print("3. Actualizar poblacion y superficie")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("8. Guardar datos en CSV")
    print("9. Salir")
    print("----------------------------------------------------------")

def main():
    # Funcion principal. Carga el dataset al inicio y mantiene el menu
    # activo en un bucle hasta que el usuario elija salir (opcion 9).
    nombre_archivo = NOMBRE_ARCHIVO
    paises = cargar_paises_csv(nombre_archivo)

    opcion = 0

    while opcion != 9:
        mostrar_menu()
        opcion = pedir_opcion("Seleccione una opcion: ", 1, 9)

        if opcion == 1:
            mostrar_lista_paises(paises)
        elif opcion == 2:
            agregar_pais(paises, nombre_archivo)
        elif opcion == 3:
            actualizar_pais(paises, nombre_archivo)
        elif opcion == 4:
            buscar_pais(paises)
        elif opcion == 5:
            menu_filtros(paises)
        elif opcion == 6:
            ordenar_paises(paises)
        elif opcion == 7:
            mostrar_estadisticas(paises)
        elif opcion == 8:
            guardar_paises_csv(nombre_archivo, paises)
        else:
            print("Saliendo del sistema.")

# Punto de entrada: solo ejecuta main() si este archivo se corre directamente.
# Si otro archivo lo importara, main() no se ejecutaria automaticamente.
if __name__ == "__main__":
    main()
