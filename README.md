# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Albert Blázquez Badenas

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

---

## Tratamiento de ficheros de notas

A continuación se detalla la solución para la lectura de expedientes académicos mediante expresiones regulares en Python. Se ha añadido la función `leeAlumnos(ficAlum)` al fichero `alumno.py` cumpliendo con los requisitos de análisis de cadenas y la integración del test unitario en formato `doctest`.

### Ejecución de los tests unitarios de `alumno.py`

A continuación se muestra la captura de pantalla con el resultado de la ejecución del fichero en modo verboso (`-v`), demostrando que se pasan con éxito todos los test unitarios normalizando los espacios en blanco:

![Resultado de los tests unitarios](captura_tests.png)

---

## Código desarrollado

### Fichero: `alumno.py`

```python
"""
Módulo para la gestión de alumnos y sus calificaciones.

Autor: Fulano Mengano Zutano
Descripción: Este módulo define la clase Alumno y proporciona funciones
para leer expedientes académicos desde archivos de texto usando
expresiones regulares.
"""

import re


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de los alumnos y devuelve un
    diccionario en el que la clave sea el nombre de cada alumno y su contenido
    el objeto Alumno correspondiente.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...      print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcell de Lara  4.9
    68      David Garcia Fuster     7.0
    """
    dicc_alumnos = {}
    
    # Expresión regular:
    # 1. ^(\d+)\s+       -> Grupo 1: Captura el ID numérico inicial.
    # 2. ([A-Za-z ]+?)\s+ -> Grupo 2: Captura el nombre de forma no codiciosa.
    # 3. ([\d.\s]+)$     -> Grupo 3: Captura el bloque final de notas y espacios.
    patron = re.compile(r'^(\d+)\s+([A-Za-z ]+?)\s+([\d.\s]+)$')

    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
                
            match = patron.match(linea)
            if match:
                num_id = int(match.group(1))
                nombre = match.group(2).strip()
                
                # Extraemos todas las notas individuales del bloque final
                notas_str = re.findall(r'\d+(?:\.\d+)?', match.group(3))
                notas = [float(n) for n in notas_str]
                
                dicc_alumnos[nombre] = Alumno(nombre, num_id, notas)
                
    return dicc_alumnos


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
