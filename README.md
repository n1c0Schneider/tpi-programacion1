# Gestión de Datos de Paises en Python

TPI - Programación 1 | UTN Tecnicatura Universitaria en Programación

---

# Descripcion

Sistema de gestion de informacion sobre paises desarrollado en Python 3. Permite cargar datos desde un archivo CSV y realizar busquedas, filtros, ordenamientos y estadisticas sobre el dataset.

---

# Integrantes

|       Nombre      |     GitHub     |
|-------------------|----------------|
| Schneider Nicolas | n1c0Schneider  |
| Leonel Zaccardi   | LeoZaccardi    |

---

# Requisitos

- Python 3.x instalado
- Archivo `paises.csv` en la misma carpeta que `main.py`

---

# Como ejecutar

Clonar el repositorio:

```bash
git clone https://github.com/n1c0Schneider/tpi-programacion1.git
cd tpi-programacion1
```

Ejecutar el programa:

```bash
python main.py
```

---

# Estructura del proyecto

```
tpi-programacion1/
    main.py              # Código fuente principal
    paises.csv           # Dataset con 55 países
    README.md            

```

---

# Menu principal

```
--------------- GESTION DE DATOS DE PAISES ----------------
1. Mostrar todos los paises
2. Agregar pais
3. Actualizar poblacion y superficie
4. Buscar pais por nombre
5. Filtrar paises
6. Ordenar paises
7. Mostrar estadisticas
8. Guardar datos en CSV
9. Salir
----------------------------------------------------------
```

---

# Ejemplos de uso

**Buscar un pais por nombre parcial**

```
Ingrese el nombre o parte del nombre del pais: arg
- Muestra: Argentina
```

**Filtrar por continente**

```
Ingrese el continente: America
-Muestra todos los países de América (15 resultados)
```

**Filtrar por rango de poblacion**

```
Poblacion minima: 1000000
Poblacion maxima: 10000000
- Muestra países con población entre 1M y 10M
```

**Ordenar por superficie descendente**

```
Seleccione el criterio: 3 (Superficie)
Seleccione la direccion: 2 (Descendente)
- Rusia, Canada, Estados Unidos, China...
```

**Estadisticas generales**

```
Pais con mayor poblacion: India (1.417.173.173)
Pais con menor poblacion: Fiji (896.444)
Promedio de poblacion: 117.306.080
Promedio de superficie: 1.796.115 km2
Paises por continente:
  America: 15
  Europa: 15
  Asia: 13
  Africa: 8
  Oceania: 4
```

---

## Dataset

El archivo `paises.csv` contiene 55 países con los siguientes campos:

| Campo | Tipo | Ejemplo |
|-------|------|---------|
| nombre | string | Argentina |
| poblacion | int | 45376763 |
| superficie | int | 2780400 |
| continente | string | America |

Fuentes de los datos: 
[Banco Mundial](https://data.worldbank.org) 
[CIA World Factbook](https://www.cia.gov/the-world-factbook)
[UN Data](https://data.un.org)
