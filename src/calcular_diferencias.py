# coding=utf-8
import gestor_ficheros
import gmail


# Comprueba si hay datos nuevos, y en ese caso; cuales son y a que modulo pertenecen
def is_different(datos_nuevos):
    mensaje = ""
    try:
        datos_fichero = gestor_ficheros.from_json()
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
                        # val = archivo o tarea subida
                        # tipo = (tarea, archivo, carpeta, foro...)
                        enlace = str(datos_nuevos.get(key, {}).get(val))
                        data = gestor_ficheros.max_3_palabras(key) + " -> " + val + " : " + enlace
                        mensaje += "\n" + str(data.encode('utf-8'))
        print mensaje
        gmail.main(mensaje)
    # Excepción lanzada cuando el archivo 'Aulavirtual.json' no exite
    except IOError:
        print "Se ha creado el primer registro de la página"
        # En cualquier caso se guardan los nuevos datos en el archivo
    finally:
        gestor_ficheros.tojson(datos_nuevos)
