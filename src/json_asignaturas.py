# -*- coding: utf-8 -*-
import json


# Recibe una frase como entrada y devuelve solo las 3 primeras palabras
def max_3_palabras(frase):
    max = frase.split(" ")
    if len(max) < 4:
        return frase
    else:
        return " ".join(max[:3])


# Se hace entrega del diccionario y lo parsea a json
def tojson(datos):
    with open('Aulavirtual.json', 'w') as f:
        new_json = json.dumps(datos)
        f.write(new_json)
        f.close()


# Se recoge el json guardado en el fichero y lo devuelve (diccionario)
def from_json():
    with open("Aulavirtual.json") as r:
        oldjson = json.load(r)
        r.close()
    return oldjson


# Comprueba si hay datos nuevos, y en ese caso; cuales son y a que modulo pertenecen
def is_different(datos_nuevos):
    try:
        datos_fichero = from_json()
        if cmp(datos_nuevos, datos_fichero) == 0:
            print "\tNo hay publicaciones nuevas"
        else:
            # Desglose del json en clave, valor
            for key, valor in datos_nuevos.iteritems():
                # Se obtienen dos type<list> ordenados, con los archivos de cada asignatura
                lista_tareas_nuevas = sorted(valor.keys())
                lista_tareas_vieja = sorted(datos_fichero.get(key))
                # Se procede a comprobar cuales son las diferencias 1by1
                for val in lista_tareas_nuevas:
                    if val in lista_tareas_vieja:
                        pass
                    else:
                        # Si el val(nombre del archivo) no esta en la segunda lista se lanza la información
                        # key = nombre de la asignatura
                        # val = archvio o tarea subida
                        # tipo = (tarea, archivo, carpeta, foro...)
                        tipo = datos_nuevos.get(key, {}).get(val)
                        print max_3_palabras(key), " -> ", val, " : ", tipo

    # Excepción lanzada cuando el archivo 'Aulavirtual.json' no exite
    except IOError:
        print "Se ha creado el primer registro de la página"
        # En cualquier caso se guardan los nuevos datos en el archivo
    finally:
        tojson(datos_nuevos)