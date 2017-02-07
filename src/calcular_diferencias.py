# coding=utf-8
import logging
import os
import sys

import gestor_ficheros
import gmail


# Comprueba si hay datos nuevos, y en ese caso; cuales son y a que modulo pertenecen
def is_different(datos_nuevos):
    logging.info("Buscando diferencias...")
    mensaje = ""
    if os.path.exists(gestor_ficheros.URL_JSON):
        datos_fichero = gestor_ficheros.from_json()
        if cmp(datos_nuevos, datos_fichero) == 0:
            logging.info("No se han encontrado novedades")
            print "\tNo hay publicaciones nuevas"
            sys.exit()
        else:
            logging.info("Buscando diferencias en ficheros")
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
                        # val = archivo o tarea subida
                        # tipo = (tarea, archivo, carpeta, foro...)
                        enlace = str(datos_nuevos.get(key, {}).get(val))
                        data = gestor_ficheros.max_3_palabras(key) + " -> " + val + " : " + enlace
                        mensaje += "\n" + str(data.encode('utf-8'))
        print mensaje
        logging.info("Se procede a enviar email")
        gmail.main(mensaje)
    # Excepción lanzada cuando el archivo 'Aulavirtual.json' no exite
    else:
        logging.warning("No existe registro anterior de la página")
        print "Se ha creado el primer registro de la página"
    # En cualquier caso se guardan los nuevos datos en el archivo
    gestor_ficheros.tojson(datos_nuevos)
    logging.info("Se ha actualizado/creado el registro de la página")
