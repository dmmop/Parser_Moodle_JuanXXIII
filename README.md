# Parser_Moodle_JuanXXIII

Es un Scrapper del moodle del JuanXXIII, simplemente compara si ha habido cambios entre ejecuciones.

El script lleva un gestor de usuarios y contraseñas, completamente transparente al usuario,
solo debe registrarse la primera vez. Las veces posteriores solo debe introducir su nombre de usuario (del moodle).

Hecho por David M. Martin el 05/02/2016

Para realizar la instalacion en un equipo externo:
    sudo python get-pip.py
    sudo python setup.py build
    sudo python setup.py install --user