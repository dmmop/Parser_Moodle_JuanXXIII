# -*- coding: utf-8 -*-
import json


def tojson(datos):
    with open('Aulavirtual.json', 'w') as f:
        new_json = json.dumps(datos)
        f.write(new_json)
        f.close()


def from_json():
    with open("Aulavirtual.json") as r:
        oldjson = json.load(r)
        r.close()
    return oldjson


def is_different(datos_nuevos):
    try:
        datos_fichero = from_json()  # FIXME: función recurrente
        if cmp(datos_nuevos, datos_fichero) == 0:
            print "No hay publicaciones nuevas"
        else:
            for key, valor in datos_nuevos.iteritems():
                lista_tareas_nuevas = sorted(valor.keys())
                lista_tareas_vieja = sorted(datos_fichero.get(key))
                for val in lista_tareas_nuevas:
                    if val in lista_tareas_vieja:
                        pass
                    else:
                        print key, " -> ", val  # FIXME: Lanzar el tipo de dato encontrado
    except IOError:
        print "Se ha creado el primer registro de la página"
    finally:
        tojson(datos_nuevos)


"""
TODO: Esta funcion tiene que devolver un diccionario a partir del fichero leido ("Aulavirtual.json")
"""
