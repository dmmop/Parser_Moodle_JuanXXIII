# -*- coding: utf-8 -*-
import cookielib
from threading import Thread, RLock

import keyring
import mechanize
from bs4 import BeautifulSoup

import json_asignaturas

"""
Se le da a la función el link que debe analizar y el modulo sobre el que se esta analizando,
busca dentro de ese link, los datos subidos y conserva que tipo de datos es (archivo, tarea) con su nombre
"""

# Diccionario que contiene toda la página parseada
global novedades
# noinspection PyRedeclaration
novedades = {}
bloqueo = RLock()


# Añade al diccionario principal (novedades) los módulos (key) y los diccionarios con los archivos (values)
def adding_dictionary(modulo, tareas):
    bloqueo.acquire()  # bloqueo de hilo
    novedades[modulo] = tareas  # Append to novedades, key:value
    bloqueo.release()  # hilo libre


def archivos_internos(modulo, link, br):
    br.open(link)  # abrimos la página
    soupin = BeautifulSoup(br.response().read(), 'html5lib')  # le damos formato al soup
    # Cogemos unicamente la primera palabra de cada frase
    modulo = " ".join(modulo.split()[:1])
    # Creamos un diccionario donde vamos a almacenar cada tarea
    tareas = {}
    # Dentro de la pagina buscamos todas las etiquetas <span class="instancename></span>
    for archivos in soupin.find_all('span', class_='instancename'):
        # guardamos el texto que hay dentro de la etiqueta que será el que corresponda al elemento subido
        publicacion = archivos.get_text()
        # El tipo es la ultima palabra del String, la guardamos y la borramos
        tipo = " ".join(publicacion.split()[-1:])
        publicacion = " ".join(publicacion.split()[:-1])
        # Guardamos la tarea con su tipo en un diccionario
        tareas[publicacion] = tipo
    adding_dictionary(modulo, tareas)


# Guarda la contraseña para el usuario dado
def config_pass(user):
    pswd = raw_input("Introduce tu contraseña: ")
    keyring.set_password('system', user, pswd)


# Función principal del programa
def main():
    url_login = 'http://aulavirtual.juanxxiii.net/moodle/login/index.php'  # Url de la pagina de login
    url_start = 'http://aulavirtual.juanxxiii.net/moodle/my/'  # Url de apartado 'Área personal'

    # Le solicitamos al cliente su nombre de usuario
    user = raw_input("Introduce tu usuario: ")
    # Se intenta recuperar su contraseña almacenada en el sistema
    pwd = keyring.get_password('system', user)
    # Si el usuario no tiene contraseña asociada, se procede a generar una
    if pwd is None:
        print "Usuario no registrado, se procede al registro..."
        config_pass(user)
    # Se lanza el navegador artificial con su configuración
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-agent', 'Chrome')]

    # Abrimos la página de login
    br.open(url_login)
    # Formulario de la página de login (nr=0) el primer y único formulario
    br.select_form(nr=0)

    # User credentials
    br['username'] = user
    br['password'] = pwd
    # Login
    br.submit()

    # le indicamos al navegador que una vez registrados acceda a la pagina(url_start) par a iniciar el escaneo
    br.open(url_start)

    # Iniciamos el soup a partir del navegador mechanize
    soup = BeautifulSoup(br.response().read(), 'html5lib', from_encoding='latin-1')

    links = {}  # Links de las asignaturas
    process = []  # Procesos que se van a iniciar
    for asignaturas in soup.find('div', class_='content'):
        for tag in asignaturas.find_all('a'):
            # obtengo la información que existe dentro de <a> y le doy formato
            module = tag.string
            # obtengo los links en cada <a> y los guardo
            link = tag.get('href')
            # Se genera un diccionario con cada módulo y su link correspondiente
            links[module] = link
    # Se lanzan todos los hilos (1 por link)
    for modulo, lnk in links.items():
        # Archivos_internos es la función que realiza el escaneo
        t = Thread(target=archivos_internos, args=(modulo, lnk, br))
        t.start()
        process.append(t)
    # Indicamos que el hilo queda parado hasta que se haga el último escaneo
    for t in process:
        t.join()
    # Intentamos averiguar si hay cambios desde la última vez
    json_asignaturas.is_different(novedades)


if __name__ == '__main__':
    main()
