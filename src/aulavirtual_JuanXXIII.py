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


def adding_dictionary(modulo, tareas):
    bloqueo.acquire()
    novedades[modulo] = tareas
    bloqueo.release()


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


def main():
    url_login = 'http://aulavirtual.juanxxiii.net/moodle/login/index.php'
    url_start = 'http://aulavirtual.juanxxiii.net/moodle/my/'

    user = raw_input("Introduce tu usuario: ")
    pwd = keyring.get_password('system', user)
    if pwd is None:
        print "Usuario no registrado, se procede al registro..."
        config_pass(user)

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    br.open(url_login)
    # Select the second (index one) form (the first form is a search query box)
    br.select_form(nr=0)

    # User credentials
    br['username'] = user
    br['password'] = pwd
    # Login
    br.submit()

    # print(br.open('http://aulavirtual.juanxxiii.net/moodle/my/').read())

    # le indicamos al navegador que una vez registrados acceda a la pagina:
    br.open(url_start)

    # Iniciamos el soup a partir del navegador mechanize
    soup = BeautifulSoup(br.response().read(), 'html5lib', from_encoding='latin-1')

    links = {}
    process = []
    for asignaturas in soup.find('div', class_='content'):
        for tag in asignaturas.find_all('a'):
            # obtengo la informacion que exite dentro de <a> y le doy formato
            module = tag.string
            # obtengo los links en cada <a> y los guardo
            link = tag.get('href')
            # p.apply_async(archivos_internos, (link, str, br))

            # archivos_internos(str, link, br)
            links[module] = link

    for modulo, lnk in links.items():
        t = Thread(target=archivos_internos, args=(modulo, lnk, br))
        t.start()
        process.append(t)

    for t in process:
        t.join()
    json_asignaturas.is_different(novedades)


if __name__ == '__main__':
    main()
