from pyclearpass import *
from dotenv import dotenv_values
import sys
import getpass

# Variables de entorno (.env)
config = dotenv_values(".env")
if config == {} or config["SERVER"] == "" or config["CLIENT_ID"] == "":
   print("Fichero .env no encontrado o incompleto")
   sys.exit()
SERVER = config['SERVER']
CLIENT_ID = config['CLIENT_ID']

# Nombre de archivo con las macs
FILE_NAME = 'mac.txt'

# Solicitud de credenciales
username = input("Ecribe el usuario: ")
try:
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)
    sys.exit()

# Constructor para el login en Clearpass
login = ClearPassAPILogin(server=SERVER,granttype="password",
username=username, password=password, clientid=CLIENT_ID, verify_ssl=True)

# Lectura de archivo con las macs
try:
  with open(FILE_NAME) as file:
    macs_array = file.read().splitlines()
except FileNotFoundError:
    print("Fichero de macs no encontrado <" + FILE_NAME + ">")
    sys.exit()

print("\nTotal MACs en Archivo<%s>: %d\n" % (FILE_NAME, len(macs_array)))

# Construccion de filtro para la consulta a Clearpass
macs_string = ",".join('"{0}"'.format(elem) for elem in macs_array)
filter = '{"user_id":[%s]}' % (macs_string)

# Consulta a Clearpass
users = ApiIdentities.get_local_user(login, filter, calculate_count='true', limit=1000)

# Funcion para obtener valores de diccionario
def get_val(i, dict):
   for key, value in dict.items():
      if i == key:
         return value

# Comprobacion de resultados y errores
if get_val('count', users) == None:
   print("No se han encontrado MACs en Clearpass\n")
   sys.exit()
if get_val('count', users) > 1000:
   print("Total MACs en CPPM: %s\n" % (get_val('count', users)))
   print("El numero de MACs en Clearpass supera los 1000, reduce el numero de MACs en el fichero\n")
   sys.exit()
if get_val('count', users):
   print("Total MACs en CPPM: %s\n" % (get_val('count', users)))

# Comprobacion de MACs encontradas en Clearpass
embedded = get_val('_embedded', users).get('items')
cppm_macs = []
for elem in embedded:
   cppm_macs.append(get_val('user_id', elem))
macs_not_found = []
for elem in macs_array:
    if elem in cppm_macs:
        print("MAC: "+elem+" encontrada en Clearpass")
        continue
    else:
        macs_not_found.append(elem)
        print("MAC: "+elem+" no encontrada en Clearpass")

# Resultados
print("\nTotal MACs no encontradas en CPPM: %s\n" % (len(macs_not_found)))
print("MACs no encontradas en CPPM: %s\n" % (macs_not_found))
sys.exit()