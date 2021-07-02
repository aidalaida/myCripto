# MyCripto: 

## Es una web de gestión de criptomonedas realizada con pyhton, el framework Flask y el gestor de plantillas Jinja. 

#### Instalación:

1. Instalar dependencias

    pip install -r requirements.txt, donde encontramos todas las librerias utilizadas y nos tendremos que bajar todas ellas. 

2. Crear variables de entorno:
    - Duplicar el fichero .env_template
    - Renombrar la copia a .env
    - Informar FLASK_ENV development

3. Crear fichero de configuración
    - Duplicar el fichero config_template.py
    - Renombrar la copia a config.py
    - Informar SECRET_KEY. Un buen sitio es: https://randomkeygen.com/
    - informar el fichero de base de datos. La ruta debe estar dentro del proyecto

4. Crear la base de datos:
    - Se puede hacer con un cliente gráfico o con sqlite3
    - Ejecutar lo siguiente

sqlite3 <ruta al fichero de datos puesto en config.py>
.read<ruta relativa a migration/initial.sql3>
.tables
.q


#### Ejecutar en local:
Escribir:
    Flask run 



