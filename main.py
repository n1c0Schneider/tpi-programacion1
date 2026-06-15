# TPI Programacion 
# Gestion de Datos de paises en Python: Filtros, ordenamientos y estadisticas
# Autores:  - Zaccardi, Leonel
#           - Schneider Nicolas
# Conceptos Aplicados
# - Listas
# - Diccionarios
# - Funciones
# - Condicionales
# - Bucles
# - Manejo de archivos CSV
# - Validaciones y try/except
# - Busquedas, filtros, ordenamientos y estadisticas basicas

import csv

# VALIDACIONES GENERALES


def normalizar_texto(texto):
    "Quita espacios al inicio/final y pasa el texto a minusculas."
    return texto.strip().lower()

def pedir_opcion(mensaje, minimo, maximo):
    "Pide una opcion numerica dentro de un rango."
    while True:
        try:
            opcion = int(input(mensaje))
            
            if opcion < minimo or opcion > maximo:
                raise ValueError(f"La opcion debe estar entre {minimo} y {maximo}.")
            
            return opcion
        except ValueError as error:
            print(f"Error: {error}")

def pedir_texto_no_vacio(mensaje):
    "pide un texto y verifica que no este vacio."
    while True:
        try:
            texto = input(mensaje).strip()
            
            if texto == "":
                raise ValueError("El campo no puede estar vacio.")
            
            return texto
        
        except ValueError as error:
            print(f"Error: {error}")

def pedir_entero_positivo(mensaje):
    "Pide un numero entero positivo mayor que cero."
    while True:
        try:
            numero = int(input(mensaje))
            
            if numero <= 0:
                raise ValueError("El numero debe ser entero y mayor que cero.")
            
            return numero
        
        except ValueError as error:
            print(f"Error: {error}")

def  pedir_entero_no_negativo(mensaje):
    "Pide un numero entero mayor o igual que cero."
    while True:
        try:
            numero = int(input(mensaje))
            
            if numero < 0:
                raise ValueError("El numero no puede ser negativo.")
            
            return numero
        
        except ValueError as error:
            print(f"Error: {error}")

def pedir_rango(mensaje_minimo, mensaje_maximo):
    "Pide un rango numerico y valida que el minimo no se mayor al maximo."
    while True:
        try:
            minimo = pedir_entero_no_negativo(mensaje_minimo)
            maximo = pedir_entero_no_negativo(mensaje_maximo)
            
            if minimo > maximo:
                raise ValueError("El valor minimo no puede ser mayor que el valor maximo.")
            
            return minimo, maximo
        
        except ValueError as error:
            print(f"Error: {error}")


# MANEJO DE CSV

def validar_fila_csv(fila, numero_linea):
    "Valida una fila leida desde el CSV y la convierte a un diccionario correcto."
    campos_necesarios = ["nombre", "poblacion", "superficie", "continente"]
    
    for campo in campos_necesarios:
        if campo not in fila:
            raise ValueError(f"Linea {numero_linea}: falta la columna {campo}.")
        
        if fila[campo] is None or fila[campo].strip() == "":
            raise ValueError(f"Linea {numero_linea}: el campo {campo} esta vacio.")
    
    nombre = fila["nombre"].strip()
    continente = fila["continente"].strip()
    
    try: 
        poblacion = int(fila["poblacion"])
        superficie = int(fila["superficie"])
    except ValueError:
        raise ValueError(f"Linea {numero_linea}: poblacion o superficie no tienen formato numerico.")
    if poblacion <= 0:
        raise ValueError(f"Linea {numero_linea}: la poblacion debe ser mayor que cero.")
    if superficie <= 0:
        raise ValueError(f"Linea {numero_linea}: la superficie debe ser mayor que cero.")
    
    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    
    return pais

def cargar_paises_csv(nombre_archivo):
    "Lee el archivo CSV y develve una lista de diccionarios."
    paises = []
    
    try:
        with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            
            if lector.fieldnames is None:
                print("Error: el archivo CSV  esta vacio.")
                return paises
            
            numero_linea = 1
            
            for fila in lector:
                numero_linea += 1
            
                try:
                    pais = validar_fila_csv(fila, numero_linea)
                    paises.append(pais)
                except ValueError as error:
                    print(f"Advertencia: {error}. la fila fue omitida.")
        
        print(f"Archivo {nombre_archivo} cargado correctamente. Paises cargados: {len(paises)}")
    
    except FileNotFoundError:
        print(f"Error: no se encontro el archivo {nombre_archivo}.")
    except PermissionError:
        print(f"Error: no se tienen permisos para leer el archivo {nombre_archivo}.")
    except Exception as error:
        print(f"Error inesperado al leer el CSV: {error}")
    
    return paises

def guardar_paises_csv(nombre_archivo, paises):
    "Guarda la lista de paises en el archivo CSV."
    try:
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            
            escritor.writeheader()
            
            for pais in paises:
                escritor.writerow(pais)
        
        print(f"Datos guardados correctamente en {nombre_archivo}.")
    except PermissionError:
        print(f"Error: no se tinen permisos para escribir en {nombre_archivo}.")
    except Exception as error:
        print(f"Error inesperado al guardar el CSV: {error}")

# FUNCIONES DE BUSQUEDA Y PRESENTACION

def buscar_indice_por_nombre(paises, nombre):
    "Busca un pais por nombre exacto ignorando mayusculas/minusculas."
    nombre_normalizado = normalizar_texto(nombre)
    
    for i in range(len(paises)):
        if normalizar_texto(paises[i]["nombre"]) == nombre_normalizado:
            return i
    return -1

def buscar_paises_por_nombre(paises, texto_buscado):
    "Busca paises por coincidencia parcial o exacto."
    resultados = []
    texto_buscado = normalizar_texto(texto_buscado)
    
    for pais in paises:
        if texto_buscado in normalizar_texto(pais["nombre"]):
            resultados.append(pais)
    return resultados

def mostrar_pais(pais):
    "Muestra los datos de un pais."
    print(f"Nombre: {pais['nombre']}")
    print(f"Poblacion: {pais['poblacion']}")
    print(f"Superficie: {pais['superficie']} km2")
    print(f"Continente: {pais['continente']}")

def mostrar_lista_paises(paises):
    "Muestra una lista de paises en formato simple."
    if len(paises) == 0:
        print("No hay paises para mostrar.")
        return 
    
    print("\n================== LISTADO DE PAISES ==================")
    
    for i in range(len(paises)):
        print(f"\nPais {i+1}")
        mostrar_pais(paises[i])
    print("=============================================================")


# FUNCIONALIDADES DEL MENU

def agregar_pais(paises, nombre_archivo):
    "Agrega un pais nuevo a la lista y guarda el CSV."
    print("\n--- Agregar pais ---")
    
    try:
        nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ")
        
        if buscar_indice_por_nombre(paises, nombre) != -1:
            raise ValueError("El pais ya existe en el dataset.")
        
        poblacion = pedir_entero_positivo("Ingrese la poblacion: ")
        superficie = pedir_entero_positivo("Ingrese la superficie en km2: ")
        continente = pedir_texto_no_vacio("Ingrese el continente: ")
        
        pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        }
        
        paises.append(pais)
        guardar_paises_csv(nombre_archivo, paises)
        print("Pais agregado correctamente.")
    except ValueError as error:
        print(f"Error: {error}")

def actualizar_pais(paises, nombre_archivo):
    "Actualiza poblacion y superficie de un pais existente."
    print("\n--- Actualizar pais ---")
    
    if len(paises) == 0:
        print("No hay paises cargados.")
        return
    
    nombre = pedir_texto_no_vacio("Ingrese el nombre exacto del pais a actualizar: ")
    indice = buscar_indice_por_nombre(paises, nombre)
    
    if indice == -1:
        print("No se encontro un pais con ese nombre exacto.")
        return
    print("Datos actuales: ")
    mostrar_pais(paises[indice])
    
    nueva_poblacion = pedir_entero_positivo("Ingrese la nueva poblacion: ")
    nueva_superficie = pedir_entero_positivo("Ingrese la nueva superficie en km2: ")
    
    paises[indice]["poblacion"] = nueva_poblacion
    paises[indice]["superficie"] = nueva_superficie
    
    guardar_paises_csv(nombre_archivo, paises)
    print("Pais actualizado correctamente.")

def buscar_pais(paises):
    "Busca paises por coincidencia parcial o exacta."
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
    continente = pedir_texto_no_vacio("Ingrese el continente: ")
    resultados = []
    
    for pais in paises:
        if normalizar_texto(pais["continente"]) == normalizar_texto(continente):
            resultados.append(pais)
    
    if len(resultados) == 0:
        print("No se encontraron paises para ese contiennte.")
    else:
        mostrar_lista_paises(resultados)

def filtrar_por_rango_poblacion(paises):
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
    minimo, maximo = pedir_rango("Superficie minima: ", "Superficie maxima: ")
    resultados = []
    
    for pais in paises:
        if pais["superficie"] >= minimo and pais["superficie"] <= maximo:
            resultados.append(pais)
    
    if len(resultados) == 0:
        print("No se encontraron paises dentro de ese rango de superficie.")
    else:
        mostrar_lista_paises(resultados)

def menu_filtros(paises):
    #Submenu de filtros
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
            break

# ── Funciones clave para ordenamiento y estadisticas ──────────────────────────

def obtener_nombre(pais):
    # Retorna el nombre del pais normalizado para ordenar sin importar tildes.
    return normalizar_texto(pais["nombre"])

def obtener_poblacion(pais):
    # Retorna la poblacion del pais.
    return pais["poblacion"]

def obtener_superficie(pais):
    # Retorna la superficie del pais.
    return pais["superficie"]

# ──────────────────────────────────────────────────────────────────────────────

def ordenar_paises(paises):
    #Ordena paises por nombre, poblacion o superficie.
    print("\n--- Ordenar paises ---")
    
    if len(paises) == 0:
        print("No hay paises cargados.")
        return
    
    print("1. Nombre")
    print("2. Poblacion")
    print("3. Superficie")
    
    criterio = pedir_opcion("Seleccione el criterio de ordenamiento: ", 1, 3)
    
    print("1. Ascendente")
    print("2. Descendentes")
    
    direccion = pedir_opcion("Seleccione la direccion: ", 1, 2)
    descendente = direccion == 2
    
    if criterio == 1:
        paises_ordenados = sorted(paises, key=obtener_nombre, reverse=descendente)
    elif criterio == 2:
        paises_ordenados = sorted(paises, key=obtener_poblacion, reverse=descendente)
    else:
        paises_ordenados = sorted(paises, key=obtener_superficie, reverse=descendente)
    
    mostrar_lista_paises(paises_ordenados)

def calcular_promedio(paises, campo):
    #Calcula el promedio de un campo numerico.
    if len(paises) == 0:
        return 0
    
    total = 0
    
    for pais in paises:
        total += pais[campo]
    
    return total / len(paises)

def cantidad_por_continente(paises):
    # Devuelve un diccionario con la cantidad de paises por continente.
    conteo = {}
    
    for pais in paises:
        continente = pais["continente"]
        
        if continente in conteo:
            conteo[continente] += 1
        else:
            conteo[continente] = 1
    return conteo

def mostrar_estadisticas(paises):
    #Muestra estadisticas basicas del dataset.
    print("\n--- Estadisticas ---")
    
    if len(paises) == 0:
        print("No hay paises cargados.")
        return
    
    pais_mayor_poblacion = max(paises, key=obtener_poblacion)
    pais_menor_poblacion = min(paises, key=obtener_poblacion)
    promedio_poblacion = calcular_promedio(paises, "poblacion")
    promedio_superficie = calcular_promedio(paises, "superficie")
    conteo_continentes = cantidad_por_continente(paises)
    
    print("\nPais con mayor poblacion: ")
    mostrar_pais(pais_mayor_poblacion)
    
    print("\nPais con menor poblacion: ")
    mostrar_pais(pais_menor_poblacion)
    
    print(f"\nPromedio de poblacion: {promedio_poblacion:.2f}")
    print(f"Promedio de superficie: {promedio_superficie:.2f} km2")
    
    print("\nCantidad de paises por continente: ")
    
    for continente, cantidad in conteo_continentes.items():
        print(f"{continente}: {cantidad}")


# MENU PRINCIPAL

def mostrar_menu():
    print("\n--------------- GESTION DE DATOS DE PAISES ---------------")
    print("1. Mostrar todos los paises")
    print("2. Agregar pais")
    print("3. Actualizar poblacion y superficie")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("8. guardar datos en CSV")
    print("9. Salir")
    print("----------------------------------------------------------")

def main():
    nombre_archivo = "paises.csv"
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
            print("Saliendo del sistema")

if __name__ == "__main__":
    main()