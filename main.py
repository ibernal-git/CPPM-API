from pyclearpass import *
from dotenv import dotenv_values
from utils.constants import *
from utils.filter import get_filter
from utils.menu import show_menu
import sys
import getpass

# Variables de entorno (.env)
config = dotenv_values(".env")
if config == {} or config["SERVER"] == "" or config["CLIENT_ID"] == "":
   print("Fichero .env no encontrado o incompleto")
   sys.exit()
SERVER = config['SERVER']
CLIENT_ID = config['CLIENT_ID']

# Funcion para obtener valores de diccionario
def get_val(i, dict):
   for key, value in dict.items():
      if i == key:
         return value

def result_validation(result):
  # Comprobacion de resultados y errores
  if get_val('count', result) == None:
    print("No se han encontrado MACs en Clearpass\n")
    sys.exit()
  if get_val('count', result) > 1000:
    print("Total MACs en CPPM: %s\n" % (get_val('count', result)))
    print("El numero de MACs en Clearpass supera los 1000, reduce el numero de MACs en el fichero\n")
    sys.exit()
  if get_val('count', result):
    print("Total MACs en CPPM: %s\n" % (get_val('count', result)))

def check_results(result, filter):
  # Comprobacion de ID o MAC encontradas en Clearpass
  embedded = get_val('_embedded', result).get('items')
  
  cppm_macs = []
  for elem in embedded:
    cppm_macs.append(get_val(filter, elem))
  items_not_found = []
  for elem in macs_array:
      if elem in cppm_macs:
          print(elem+" encontrada en Clearpass")
          continue
      else:
          items_not_found.append(elem)
          print(elem+" <NO> encontrada en Clearpass")
      
  if filter == FILTER[LOCAL_USERS]:
      print("\nTotal de usuarios locales no encontrados en CPPM: %s\n" % (len(items_not_found)))
      print("USUARIOS no encontrados en CPPM: %s\n" % items_not_found)
  elif filter == FILTER[ENDPOINTS]:
    print("\nTotal de endpoints no encontrados en CPPM: %s\n" % (len(items_not_found)))
    print("ENDPOINTS no encontrados en CPPM: %s\n" % items_not_found)

def read_file():
  # Lectura de archivo con las macs
    try:
      with open(FILE_NAME) as file:
        return file.read().splitlines()
    except FileNotFoundError:
        print("Fichero de macs no encontrado <" + FILE_NAME + ">")
        sys.exit()



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


while True:

  menu_option = show_menu()
  print("\n<---------------------------------------------------->")

  # Consulta a Clearpass
  if menu_option == LOCAL_USERS:

    macs_array = read_file()
    print("\nTotal USUARIOS en Archivo<%s>: %d\n" % (FILE_NAME, len(macs_array)))

    print("Buscando usuarios locales...\n")
    CPPM_result = ApiIdentities.get_local_user(login, get_filter(macs_array, menu_option), calculate_count='true', limit=1000)

    result_validation(CPPM_result)
    check_results(CPPM_result, FILTER[menu_option])

  elif menu_option == ENDPOINTS:

    macs_array = read_file()
    print("\nTotal ENDPOINTS en Archivo<%s>: %d\n" % (FILE_NAME, len(macs_array)))

    print("Buscando endpoints...\n")
    CPPM_result = ApiIdentities.get_endpoint(login, get_filter(macs_array, menu_option), calculate_count='true', limit=1000)

    result_validation(CPPM_result)
    check_results(CPPM_result, FILTER[menu_option])

  elif menu_option == None:

    macs_array = read_file()
    print("\nTotal USUARIOS y ENDPOINTS en Archivo<%s>: %d\n" % (FILE_NAME, len(macs_array)))

    print("Buscando usuarios locales y endpoints...\n")
    
    CPPM_result = ApiIdentities.get_local_user(login, get_filter(macs_array, LOCAL_USERS), calculate_count='true', limit=1000)
    result_validation(CPPM_result)
    check_results(CPPM_result, FILTER[LOCAL_USERS])

    print("\n<---------------------------------------------------->\n")

    CPPM_result = ApiIdentities.get_endpoint(login, get_filter(macs_array, ENDPOINTS), calculate_count='true', limit=1000)
    result_validation(CPPM_result)
    check_results(CPPM_result, FILTER[ENDPOINTS])