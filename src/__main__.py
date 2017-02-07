# -*- coding: utf-8 -*-
"""
1. Cargar el json preexistente (si existe)
2. Scrappear el AulaVirtual (sobrescribe el json anterior)
3. Comparar el diccionario recuperado del json con el Scrapeado
4. Mostrar por pantalla los cambios que ha habido
"""
# url_login = 'http://aulavirtual.juanxxiii.net/moodle/login/index.php'  # Url de la pagina de login
# url_start = 'http://aulavirtual.juanxxiii.net/moodle/my/'  # Url de apartado 'Área personal'

import aulavirtual_JuanXXIII

if __name__ == '__main__':
    aulavirtual_JuanXXIII.main()
