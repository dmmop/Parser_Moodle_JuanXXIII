# -*- coding: utf-8 -*-
import cookielib
import logging
import os
from ConfigParser import ConfigParser
from threading import Thread, RLock

import keyring
import mechanize
from bs4 import BeautifulSoup

import calcular_diferencias

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
    logging.info("Parseando links y tareas")
    br.open(link)  # abrimos la página
    soupin = BeautifulSoup(br.response().read(), 'html5lib')  # le damos formato al soup
    # Cogemos unicamente la primera palabra de cada frase
    # modulo = " ".join(modulo.split()[:1])
    # Creamos un diccionario donde vamos a almacenar cada tarea
    tareas = {}
    # Dentro de la pagina buscamos todas las etiquetas <span class="instancename></span>
    # TODO: <a class onclik> recuperar ['href']
    for archivos in soupin.find_all('span', class_='instancename'):
        # guardamos el texto que hay dentro de la etiqueta que será el que corresponda al elemento subido
        publicacion = archivos.get_text()
        # El tipo es la ultima palabra del String, la guardamos y la borramos
        tipo = " ".join(publicacion.split()[-1:])
        publicacion = " ".join(publicacion.split()[:-1])
        # Guardamos la tarea con su tipo en un diccionario
        tareas[publicacion] = tipo
    logging.info("Añadir %s a Novedades", modulo)
    adding_dictionary(modulo, tareas)


def archivos_link(modulo, link, br):
    logging.info("Parseando links y tareas")
    br.open(link)  # abrimos la página
    soupin = BeautifulSoup(br.response().read(), 'html5lib')  # le damos formato al soup
    # Cogemos unicamente la primera palabra de cada frase
    # modulo = " ".join(modulo.split()[:1])
    # Creamos un diccionario donde vamos a almacenar cada tarea
    tareas = {}
    # Dentro de la pagina buscamos todas las etiquetas <span class="instancename></span>
    # TODO: <a class onclik> recuperar ['href']
    for main in soupin.find_all('div', class_='row-fluid'):
        for archivos in main.find_all('a', onclick=True):  # se recupera el nombre
            # guardamos el texto que hay dentro de la etiqueta que será el que corresponda al elemento subido
            actividad = archivos.get_text()  # El tipo es la ultima palabra del String, la guardamos y la borramos
            actividad = " ".join(actividad.split()[:-1])
            descarga = archivos.get('href')
            # Guardamos la tarea con su descarga en un diccionario
            tareas[actividad] = descarga
    logging.info("Añadir %s a Novedades", modulo)
    adding_dictionary(modulo, tareas)


def configuracion(**kwargs):
    config = ConfigParser()
    if not config.read("url.cfg"):
        config.add_section("URLs")
        url_login = str(raw_input("Introduzca la URL de la página de login: "))
        config.set("URLs", "url_login", url_login)
        url_start = str(raw_input("Introduzca la URL del apartado 'Área Personal': "))
        config.set("URLs", "url_start", url_start)
        with open("url.cfg", "w") as f:
            config.write(f)
            f.close()
    else:
        logging.info("Recuperando URLs")
        url_login = config.get("URLs", "url_login")
        url_start = config.get("URLs", "url_start")
    return url_login, url_start


# Guarda la contraseña para el usuario dado
def config_pass(user):
    pswd = str(raw_input("Introduce tu contraseña: "))
    keyring.set_password('system', user, pswd)


# Función principal del programa
def main():
    # url_login = 'http://aulavirtual.juanxxiii.net/moodle/login/index.php'  # Url de la pagina de login
    # url_start = 'http://aulavirtual.juanxxiii.net/moodle/my/'  # Url de apartado 'Área personal'
    url_login, url_start = configuracion()
    # Le solicitamos al cliente su nombre de usuario
    user = str(raw_input("Introduce tu usuario: "))
    # Se intenta recuperar su contraseña almacenada en el sistema
    pwd = keyring.get_password('system', user)
    # Si el usuario no tiene contraseña asociada, se procede a generar una
    if pwd is None:
        logging.warning("EL usuario %s no existe", user)
        print "Usuario no registrado, se procede al registro..."
        config_pass(user)
        pwd = keyring.get_password('system', user)
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
    br['password'] = str(pwd)
    # Login
    br.submit()

    # le indicamos al navegador que una vez registrados acceda a la pagina(url_start) par a iniciar el escaneo
    br.open(url_start)
    # Iniciamos el soup a partir del navegador mechanize
    soup = BeautifulSoup(br.response().read(), 'html5lib', from_encoding='latin-1')

    links = {}  # Links de las asignaturas
    process = []  # Procesos que se van a iniciar
    # el primer for devuelve un TypeError: <none> not iterable, lo que significa que no ha podido registrarse
    try:
        logging.info("Iniciando rastreo de página...")
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
            t = Thread(target=archivos_link, args=(modulo, lnk, br))
            t.start()
            process.append(t)
        # Indicamos que el hilo queda parado hasta que se haga el último escaneo
        for t in process:
            t.join()
        # Intentamos averiguar si hay cambios desde la última vez
        logging.info("Finalizado rastreo de la página")
        calcular_diferencias.is_different(novedades)

    except TypeError:
        logging.error("Borrando usuario y Aulavirtual.json")
        print("Alguno de los datos introducidos no son correctos.")
        keyring.delete_password('system', user)
        if os.path.exists("./Aulavirtual.json"):
            os.remove("./Aulavirtual.json")
        main()


if __name__ == '__main__':
    main()
