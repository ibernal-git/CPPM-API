# Script para consulta de usuarios en CPPM

Este script permite que dado un listado de MACS sin delimitadores o ID de usuario ubicados en un archivo llamado "mac.txt" consulte si esos usuarios o endpoints existen en CPPM.

Los usuarios o endpoints no encontrados se mostrarán a través de pantalla.

## Requisitos

### Clearpass

Es necesario crear un **cliente de API** en Clearpass Guest de tipo Clearpass REST API. Con Grant Type escoger **Username and Password** además de marcar la opción de **Public client**. Para el perfil de operador es suficiente con uno de lectura.

Una vez creado el cliente de API es necesario crear un **servicio en CPPM para la autenticación OAuth2**, se puede configurar a través de 'Template & Wizards'.

Manual de configuración de API en Clearpass: <https://developer.arubanetworks.com/aruba-cppm/docs/clearpass-configuration>

**Para la funcionalidad de búsqueda de roles previamente es necesario guardar en la BBDD de endpoints un atributo con el rol asignado en el servicio (crear un enforcement profile de post-autenticación).**

### Archivos

- mac.txt - Para el funcionamiento del script es necesario crear un archivo con el listado de macs sin delimitadores.
- .env - También es necesario **especificar el servidor de CPPM** y el **Client ID** creado en Guest.

### Python

- Es necesario tener instalado Python v3.9 o superior
- Instalar pyclearpass (Librería para la API de CPPM)

```python
pip install pyclearpass
```
- Instalar dotenv_values

```python
pip install python-dotenv
```
- Instalar pandas y openpyxl para la exportación a excel

```python
pip install pandas
pip install openpyxl
```