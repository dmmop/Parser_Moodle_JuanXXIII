# -*- coding: utf-8 -*-
import json
import logging
import os

URL_JSON = 'Aulavirtual.json'
TO = 'destinatarios.txt'


# Recibe una frase como entrada y devuelve solo las 3 primeras palabras
def destinatarios():
    if os.path.exists(TO):
        logging.info("Abierta lista de destinatarios")
        with open(TO, "r") as f:
            destino = f.readline()
            f.close()
    else:
        logging.error("No existe lista de destinatarios")
        with open(TO, "w") as f:
            print('Tntroduce los destinatarios (email@gmail.com, email@outlook.es,..)')
            destino = raw_input()
            f.write(destino)
    return destino


def max_3_palabras(frase):
    max = frase.split(" ")
    if len(max) < 4:
        return frase
    else:
        return " ".join(max[:3])


# Se hace entrega del diccionario y lo parsea a json
def tojson(datos):
    with open(URL_JSON, 'w') as f:
        new_json = json.dumps(datos)
        f.write(new_json)
        f.close()


# Se recoge el json guardado en el fichero y lo devuelve (diccionario)
def from_json():
    with open(URL_JSON) as r:
        oldjson = json.load(r)
        r.close()
    return oldjson
