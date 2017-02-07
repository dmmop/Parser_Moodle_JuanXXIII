# -*- coding: utf-8 -*-
import json
import os

# Recibe una frase como entrada y devuelve solo las 3 primeras palabras
def destinatarios():
    to = 'destinatarios.txt'
    if os.path.exists(to):
        with open(to, "r") as f:
            destino = f.readline()
            f.close()
    else:
        with open(to, "w") as f:
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
